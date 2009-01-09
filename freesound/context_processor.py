from django.conf import settings
from datetime import datetime
from django.core.cache import cache
from accounts.models import Profile

def get_last_action_time(user):
    now = datetime.now()
    
    if not user.is_authenticated():
        return now

    cache_key = "get_last_action_time_%d" % user.id
    last_action_time = cache.get(cache_key)
    
    if not last_action_time:
        # get from DB!
        try:
            profile = Profile.objects.get(user=user)
            last_action_time = profile.last_action_time
            if last_action_time == None:
                last_action_time = now
        except Profile.DoesNotExist:
            profile = None
            last_action_time = now
            
        if profile:
            profile.last_action_time = now
            profile.save()
        
        # give the user 10 minutes to read all threads before marking them
        cache.set(cache_key, now, 5*60)
    
    return last_action_time
            
def context_extra(request):
    
    return {'media_url': settings.MEDIA_URL, 'request': request, 'last_action_time': get_last_action_time(request.user)}