from django.db import models
import random

MAX_LIVES = 5

def random_number():
    return random.randint(1, 100)

class Game(models.Model):
    player = models.CharField(max_length=20, default='Anonymous')
    secret = models.IntegerField(default=random_number)
    attempts = models.IntegerField(default=0)
    lives = models.IntegerField(default=MAX_LIVES)
    finished = models.BooleanField(default=False)
    won = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} - Game {self.id} ({'won' if self.won else 'lost' if self.finished else 'playing'})"