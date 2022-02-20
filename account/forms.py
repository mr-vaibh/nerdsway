from django.forms import DateInput, ModelForm, NumberInput

from .models import UserProfile

class UserProfileEditForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

        labels = {
            'location': 'Your location, where are you from?',
            'phone': 'Phone Number',
            'dob': 'Date of Birth (mind the format 😬)',
            'bio': 'Write something about you',
            'facebook': 'Facebook username',
            'instagram': 'Instagram username',
            'twitter': 'Twitter username',
            'website': 'Website URL',
            'profile_pic': 'Upload a nice Profile Picture',
        }

        widgets = {
            'phone': NumberInput(),
            'dob': DateInput(format=('%d/%m/%Y'), attrs={'type':'date'}),
        }