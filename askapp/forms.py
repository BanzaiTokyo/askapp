from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from registration.forms import RegistrationFormTermsOfService
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Profile, Thread, Post


class RecaptchaRegistrationForm(RegistrationFormTermsOfService):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())

form_control = {'class': 'form-control'}
class ProfileForm(forms.ModelForm):
    is_active = forms.BooleanField(required=False)
    class Meta:
        model = Profile
        fields = ('avatar', 'country', 'city', 'about')
        widgets = {
            'country': forms.Select(attrs=form_control),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your city')}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AskappClearableFileInput(forms.widgets.ClearableFileInput):
    template_with_initial = (
        '%(clear_template)s<br />%(input_text)s: %(input)s'
    )


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('thread_type', 'link', 'title', 'text', 'tags', 'image')

        widgets = {
            'image': AskappClearableFileInput()
        }

    def __init__(self, user, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        if self.instance and not self.instance.id:
            self.instance.user = user
        elif not user.is_staff:
            self.fields.pop('thread_type')

    def clean(self):
        cleaned_data = super(ThreadForm, self).clean()
        link = cleaned_data.get("link")
        thread_type = cleaned_data.get("thread_type")

        #if thread_type and self.initial.get('thread_type', thread_type) != thread_type and not self.user.is_staff and not self.has_error('title'):
        #    self.add_error('title', 'You are not allowed to change the thread type')

        if thread_type in ['LL','YT'] and not link and not self.has_error('link'):
                msg = _("This field is required")
                self.add_error('link', msg)
        elif self.has_error('link') and thread_type not in ['LL','YT']:
            del self.errors['link']
        if thread_type == 'YT' and not self.has_error('link') and not Thread(link=link).parse_youtube_url():
            msg = _("This is not a Youtube URL")
            self.add_error('link', msg)


class ReplyForm(forms.ModelForm):
    is_answer = forms.BooleanField(required=False)
    class Meta:
        model = Post
        fields = ('text', 'is_answer')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
