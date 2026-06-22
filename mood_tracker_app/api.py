from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from .models import MoodLog
from login_app.models import User

def mood_api(request):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    user = User.objects.get(id=request.session['user_id'])
    logs = MoodLog.objects.filter(user=user).order_by('-created_at')[:10]
    
    data = []
    for log in logs:
        data.append({
            'date': log.created_at.strftime('%Y-%m-%d'),
            'mood': log.mood,
            'mood_score': log.mood_score,
            'note': log.note or '',
        })
    
    return JsonResponse({'logs': data}, status=200)


@require_POST
def send_reminder_api(request):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    user = User.objects.get(id=request.session['user_id'])
    
    # آخر log
    last_log = MoodLog.objects.filter(user=user).order_by('-created_at').first()
    
    # جمل تحفيزية حسب المود
    mood_messages = {
        'Amazing': "You're on top of the world! 🌟 Keep riding that beautiful energy — you deserve every bit of it.",
        'Happy': "Your happiness is contagious! 😊 Cherish this feeling and share it with someone you love today.",
        'Relaxed': "Peace looks good on you 🌿 Stay in this gentle space and let yourself just be.",
        'Okay': "Okay is more than enough 🙂 You're showing up, and that takes courage. Keep going.",
        'Tired': "Rest is not giving up — it's recharging 😴 Be gentle with yourself today, you've earned it.",
        'Sad': "It's okay to feel sad 💙 Your feelings are valid. Take it one breath at a time.",
        'Anxious': "You are safe 🌀 Take a deep breath. This feeling will pass — you've gotten through hard days before.",
        'Angry': "Your feelings are valid 🔥 Take a moment to breathe. You have the strength to navigate this.",
    }
    
    if last_log:
        mood = last_log.mood
        message = mood_messages.get(mood, "Every day is a new chance to check in with yourself 💜")
        subject = f'🌸 SoulSpace — You felt {mood} last time'
        body = f'Hi {user.first_name},\n\nLast time you logged, you were feeling {mood}.\n\n"{message}"\n\nHow are you feeling today? Take a moment to check in:\nhttp://127.0.0.1:8000/mood/check-in/\n\nWith care,\nSoulSpace Team 💜'
    else:
        subject = '🌸 SoulSpace — Start your journey'
        body = f'Hi {user.first_name},\n\nYou haven\'t logged your mood yet.\n\n"The first step to understanding yourself is simply noticing how you feel."\n\nStart here:\nhttp://127.0.0.1:8000/mood/check-in/\n\nWith care,\nSoulSpace Team 💜'
    
    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    
    return JsonResponse({'message': 'Reminder sent successfully!'}, status=200)