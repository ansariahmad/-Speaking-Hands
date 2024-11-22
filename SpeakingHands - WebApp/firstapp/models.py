
from django.db import models

from django.contrib.auth.models import User


class LoginAttempts(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    login_attempts = models.IntegerField()
    
    def __str__(self):
        return (f"{self.id} - {self.user_id} - {self.login_attempts}")
    
class LoginDateTime(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.CharField(max_length=10)
    login_time = models.CharField(max_length=10)
    
    def __str__(self):
        return (f"{self.id} - {self.user_id} - {self.login_date}")
    
class DashBoard(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    c_date = models.CharField(max_length=10)
    c_time = models.CharField(max_length=10)
    button_pressed = models.IntegerField()
    total_predictions = models.IntegerField()
    correct_predictions = models.IntegerField()
    incorrect_predictions = models.IntegerField()
    accuracy = models.FloatField()

    def __str__(self):
        
        return (f"{self.id} - {self.c_date} - {self.c_time} - {self.button_pressed} - {self.total_predictions}  - {self.correct_predictions} - {self.incorrect_predictions} - {self.accuracy}")

# class Feedback(models.Model):
#     pass
