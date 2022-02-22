from django.db import models
from django.contrib.auth.models import User

# Signal to create a user profile when a user is created
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

gender_choices = (
    ('female', 'Female'),
    ('male', 'Male'),
    ('lgbtqia', 'LGBTQIA+'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=gender_choices, max_length=7, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    facebook = models.CharField(max_length=50, blank=True)
    instagram = models.CharField(max_length=50, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    website = models.URLField(max_length=200, blank=True)
    profile_pic = models.ImageField(upload_to='accounts/profile_pics', blank=True)

    def __str__(self):
        return self.user.username
    
    # === PS: Ignore should have 'self' as first argument warning ===
    # Create a user profile when a user is created
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    
    # Create a user profile when a user is saved
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.user_profile.save()
    
    def delete(self, *args, **kwargs):
        if self.profile_pic:
            self.profile_pic.delete()
            super().delete(*args, **kwargs)
    
    def get_full_name(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    def get_age(self):
        if self.dob:
            today = self.date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        else:
            return None
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'