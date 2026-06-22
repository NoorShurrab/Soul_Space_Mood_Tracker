from django.shortcuts import render, redirect
from .models import MoodLog
from django.db.models import Avg, Count
import calendar
from datetime import datetime
from datetime import date, timedelta
from mood_tracker_app.models import MoodLog, Tag, MoodLogTag
from login_app.models import User
from django.utils.timezone import localtime
def about_us(request):
    return render(request, 'about.html')

def calculate_streak(user_logs):
    streak = 0
    check_date = date.today()
    logged_dates = set(user_logs.values_list('created_at__date', flat=True))
    
    while check_date in logged_dates:
        streak += 1
        check_date -= timedelta(days=1)
    
    return streak

def dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    

    user = User.objects.get(id=request.session['user_id'])
    
    now = datetime.now()
    user_logs = MoodLog.objects.filter(user=user)
    current_month_logs = user_logs.filter(created_at__month=now.month)
    
    avg_mood = user_logs.aggregate(Avg('mood_score'))['mood_score__avg']
    avg_mood_rounded = round(avg_mood, 1) if avg_mood else 0.0
    
    most_felt = user_logs.values('mood').annotate(count=Count('mood')).order_by('-count').first()
    most_felt_mood = most_felt['mood'] if most_felt else "None"
    
    current_streak = calculate_streak(user_logs)
    
    mood_map = {str(localtime(log.created_at).day): log.get_mood_color() for log in current_month_logs}
    
    cal = calendar.Calendar()
    days = list(cal.itermonthdays(now.year, now.month))
    
    context = {
        'days': days,
        'mood_map': mood_map,
        'username': user.first_name,
        'total_logs': user_logs.count(),
        'avg_mood': avg_mood_rounded,
        'current_streak': current_streak,
        'most_felt': most_felt_mood,
        'current_month': now.strftime('%B'),  # June
        'current_year': now.year, #2026
        'today': datetime.now().strftime('%A, %B %d'),  # Sunday, June 21
    }
    return render(request, 'dashboard.html', context)

def check_in_view(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    
    if request.method == 'POST':
        mood = request.POST.get('mood')
        note = request.POST.get('note')
        tags_input = request.POST.get('tags', '')
        
        from login_app.models import User
        user = User.objects.get(id=request.session['user_id'])
        
        MOOD_SCORE = {
            'Amazing': 5, 'Happy': 4, 'Relaxed': 3,
            'Okay': 3, 'Tired': 2, 'Sad': 2,
            'Anxious': 1, 'Angry': 1,
        }
        
        log = MoodLog.objects.create(
            user=user,
            mood=mood,
            mood_score=MOOD_SCORE.get(mood, 3),
            note=note,
        )
        
        if tags_input:
            tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                MoodLogTag.objects.create(mood_log=log, tag=tag)
        
        return redirect('/mood/dashboard/')
    
    return render(request, 'check.html')

def history_view(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    
    user = User.objects.get(id=request.session['user_id'])
    logs = MoodLog.objects.filter(user=user).order_by('-created_at')
    
    
    mood_filter = request.GET.get('mood', '')
    if mood_filter:
        logs = logs.filter(mood=mood_filter)
    
    search = request.GET.get('search', '')
    if search:
        logs = logs.filter(note__icontains=search)
    
    # Stats
    all_logs = MoodLog.objects.filter(user=user)
    avg_mood = all_logs.aggregate(Avg('mood_score'))['mood_score__avg']
    avg_mood_rounded = round(avg_mood, 1) if avg_mood else 0.0
    logs_with_notes = all_logs.filter(note__isnull=False).exclude(note='').count()
    
    
    logs_with_tags = []
    for log in logs:
        tags = MoodLogTag.objects.filter(mood_log=log).select_related('tag')
        logs_with_tags.append({
            'log': log,
            'tags': [mt.tag.name for mt in tags],
        })
    
    context = {
        'logs_with_tags': logs_with_tags,
        'total_logs': all_logs.count(),
        'avg_mood': avg_mood_rounded,
        'logs_with_notes': logs_with_notes,
        'mood_filter': mood_filter,
        'search': search,
        'total_filtered': logs.count(),
        'mood_choices': MoodLog.MOOD_CHOICES,
    }
    return render(request, 'history.html', context)