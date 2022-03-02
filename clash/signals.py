from .models import Player
def create_profile(sender,instance,created,**kwargs):
    if created:
        Player.objects.create(user=instance)
        print('Player Created')
