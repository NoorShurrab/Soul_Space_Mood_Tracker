from django.db import models
from login_app.models import User

MOOD_SCORE = {
    'Amazing': 5,
    'Happy': 4,
    'Relaxed': 3,
    'Okay': 3,
    'Tired': 2,
    'Sad': 2,
    'Anxious': 1,
    'Angry': 1,
}

class MoodLog(models.Model):
    MOOD_CHOICES = [
        ('Amazing', 'Amazing'),
        ('Happy', 'Happy'),
        ('Relaxed', 'Relaxed'),
        ('Okay', 'Okay'),
        ('Tired', 'Tired'),
        ('Sad', 'Sad'),
        ('Anxious', 'Anxious'),
        ('Angry', 'Angry'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    mood_score = models.IntegerField(default=3)
    note = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True) 

    def get_mood_color(self):
        colors = {
            'Amazing': 'bg-green-500',
            'Happy': 'bg-yellow-400',
            'Relaxed': 'bg-teal-400',
            'Okay': 'bg-purple-400',
            'Tired': 'bg-blue-300',
            'Sad': 'bg-blue-600',
            'Anxious': 'bg-pink-400',
            'Angry': 'bg-red-500',
        }
        return colors.get(self.mood, 'bg-gray-200')

    def __str__(self):
        return f"{self.user.username} - {self.mood} - {self.created_at.strftime('%Y-%m-%d')}"

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class MoodLogTag(models.Model):
    mood_log = models.ForeignKey(MoodLog, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)