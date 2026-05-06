from django.db import models
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    # Just tying it to the user for now
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.CharField(max_length=50, default="Unranked")
    current_points = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.rank}"

class MatchStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match_date = models.DateTimeField(auto_now_add=True)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    weapon_accuracy = models.FloatField(help_text="Percentage of shots hit", default=0.0)
    win = models.BooleanField(default=True)
    game_mode = models.CharField(max_length=100, default="Ranked")
    
    @property
    def kd_ratio(self):
        if self.deaths == 0:
            return float(self.kills)
        return round(self.kills / self.deaths, 2)
        
    def __str__(self):
        return f"Match on {self.match_date.strftime('%Y-%m-%d')} - {'Win' if self.win else 'Loss'} (K/D: {self.kd_ratio})"

class StrategyDocument(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # We will use Chroma for vector embeddings rather than pgvector locally
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
