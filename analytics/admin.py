from django.contrib import admin
from .models import PlayerProfile, MatchStat, StrategyDocument

admin.site.register(PlayerProfile)
admin.site.register(MatchStat)
admin.site.register(StrategyDocument)
