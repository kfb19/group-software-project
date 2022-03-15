from ..models import Category, Challenges, Responses, WeeklyChallenge
from ..forms import ChallengeForm
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
"""
    Authors: Michael Hills
    Description: View for the main homepage
"""
def home(request):
    categories = Category.objects.all()

    all_challenges = Challenges.objects.all()

    if (len(all_challenges.exclude(Q(is_weekly_challenge=False))) == 0):
        print("No weekly challenges! Generating...")
        generate_weekly_challenges(all_challenges)

    # Get the filter from the ?q= in the URL
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    # Get all challenges, not done by the current user
    if request.user.is_authenticated:
        responses = Responses.objects.filter(user=request.user).values_list('challenge_id')

        challenges = all_challenges.exclude(id__in=responses).filter(
            Q(category__name__icontains=q),
            Q(expires_on__gt=timezone.now()) # This makes sure expired aren'trendered
            ).order_by('-created')

        
    else:
        challenges = all_challenges.filter(
            Q(category__name__icontains=q), 
            Q(expires_on__gt=timezone.now()) # This makes sure expired aren'trendered
            ).order_by('-created')
        # add locations to map

        # Variables to pass to the database
        

    context = {'categories': categories, 'challenges': challenges}

    return render(request, 'base/home.html', context)

def generate_weekly_challenges(challenges):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    points = models.IntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField(default="2025-01-01")
    is_weekly_challenge = models.BooleanField(default=False)
    lat = models.FloatField(default=0)
    long = models.FloatField(default=0)
    form = ChallengeForm(
        )