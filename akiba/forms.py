from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from registration.forms import RegistrationForm
from django import forms
from .models import Profile


class RecaptchaRegistrationForm(RegistrationForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())

form_control = {'class': 'form-control'}
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'country', 'city', 'about')
        widgets = {
            'country': forms.Select(attrs=form_control),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your city'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }