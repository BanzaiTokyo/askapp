from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from registration.forms import RegistrationFormTermsOfService
from django import forms
from .models import Profile, Thread, Post


class RecaptchaRegistrationForm(RegistrationFormTermsOfService):
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


class NewThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('thread_type', 'link', 'title', 'text', 'image')


class AkibaClearableFileInput(forms.widgets.ClearableFileInput):
    template_with_initial = (
        '%(clear_template)s<br />%(input_text)s: %(input)s'
    )


class EditThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('link', 'title', 'text', 'image')
        widgets = {
            'image': AkibaClearableFileInput()
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', )
