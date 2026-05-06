from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MatchStat, PlayerProfile
from .ai_service import get_coaching_feedback

# We will just simulate a logged-in user for simplicity in this prototype.
def dashboard(request):
    # Dummy user logic if no user exists
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username='test_player')
    if created:
        user.set_password('password')
        user.save()
        PlayerProfile.objects.create(user=user, rank='Gold IV', current_points=1200)

    # Handle form submission for new stats
    if request.method == 'POST':
        kills = request.POST.get('kills', 0)
        deaths = request.POST.get('deaths', 0)
        assists = request.POST.get('assists', 0)
        weapon_accuracy = request.POST.get('weapon_accuracy', 0.0)
        win = request.POST.get('win') == 'on'
        
        MatchStat.objects.create(
            user=user,
            kills=kills,
            deaths=deaths,
            assists=assists,
            weapon_accuracy=weapon_accuracy,
            win=win
        )
        return redirect('dashboard')

    stats = MatchStat.objects.filter(user=user).order_by('-match_date')[:10]
    profile = PlayerProfile.objects.get(user=user)
    
    return render(request, 'analytics/dashboard.html', {
        'stats': stats,
        'profile': profile
    })

def ai_coach(request):
    from django.contrib.auth.models import User
    user = User.objects.first() # Get the dummy user
    
    feedback = None
    if request.method == 'POST':
        query = request.POST.get('query', 'How can I improve my current rank?')
        recent_stats = MatchStat.objects.filter(user=user).order_by('-match_date')[:5]
        
        stats_summary = ""
        for stat in recent_stats:
            stats_summary += f"K/D/A: {stat.kills}/{stat.deaths}/{stat.assists}, Win: {stat.win}, Accuracy: {stat.weapon_accuracy}%\n"
            
        if not stats_summary:
            stats_summary = "No recent matches played."
            
        feedback = get_coaching_feedback(stats_summary, query)
        
    return render(request, 'analytics/ai_coach.html', {
        'feedback': feedback
    })
