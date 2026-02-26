from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from config.constants import UserRank

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rank = models.CharField(
        max_length=20,
        choices=UserRank.choices,
        default=UserRank.NEWT,
    )
    following = models.ManyToManyField(
        'self',
        through='Relationship',
        related_name='followers',
        symmetrical=False
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Biography"
    )
    avatar_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    
    # Social Networks
    twitch = models.CharField(max_length=150, blank=True)
    instagram = models.CharField(max_length=150, blank=True)
    tiktok = models.URLField(max_length=150, blank=True)
    facebook = models.URLField(max_length=150, blank=True)
    other = models.URLField(max_length=150, blank=True)
    
    # Statistics
    total_matches = models.PositiveIntegerField(default=0)
    total_wins = models.PositiveIntegerField(default=0)
    
    @property
    def winrate(self):
        if self.total_matches == 0:
            return 0
        return round((self.total_wins / self.total_matches) * 100, 2)
    
    @property
    def deck_limit(self):
        tier_limits = {
            UserRank.GERM: 0,
            UserRank.NEWT: 5,
            UserRank.MINION: 20,
            UserRank.SLEEPER: 50,
            UserRank.OVERLORD: float('inf'),
            UserRank.PREAETOR: float('inf'), 
        }
        return tier_limits.get(self.rank, 0)
    
    
class Relationship(models.Model):
    """Modelo intermedio para gestionar el grafo social."""
    from_profile = models.ForeignKey(Profile, related_name='rel_from', on_delete=models.CASCADE)
    to_profile = models.ForeignKey(Profile, related_name='rel_to', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_profile', 'to_profile')
        verbose_name = 'Relation'
        verbose_name_plural = 'Relationships'
        indexes = [
            models.Index(fields=['from_profile', 'to_profile'])
        ]

    def __str__(self):
        return f"{self.from_profile.user.username} follows {self.to_profile.user.username}"
    
    
# Señales para que cada que crees un User, se cree su Profile automáticamente
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)