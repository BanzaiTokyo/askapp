from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from registration.forms import RegistrationFormUniqueEmail
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Profile, Thread, Post


class RecaptchaRegistrationForm(RegistrationFormUniqueEmail):
    tos = forms.BooleanField(widget=forms.CheckboxInput,
                             label=_('I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})
    captcha = ReCaptchaField(widget=ReCaptchaWidget())


class ProfileForm(forms.ModelForm):
    is_active = forms.BooleanField(required=False)
    class Meta:
        model = Profile
        fields = ('avatar', 'country', 'city', 'about')
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
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
        fields = ('thread_type', 'original', 'link', 'title', 'text', 'tags', 'image')
        widgets = {
            'original': forms.TextInput(),
            'image': AskappClearableFileInput()
        }
        error_messages = {
            'original': {
                'invalid_choice': _('This thread is not found'),
            },
        }

    def __init__(self, user, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        if self.instance and not self.instance.id:
            self.instance.user = user
            if not user.is_staff:
                self.fields['thread_type'].choices = (
                    tt for tt in Thread.TYPES_OF_THREAD
                    if tt[0] not in [Thread.DUPLICATE, Thread.VIDEOSTREAM]
                )
        elif not user.is_staff:
            self.fields.pop('thread_type')

    def clean_original(self):
        if self.instance and self.instance == self.cleaned_data.get('original'):
            raise forms.fields.ValidationError('Cannot reference itself as a duplicate')
        return self.cleaned_data.get('original')

    def clean(self):
        cleaned_data = super(ThreadForm, self).clean()
        link = cleaned_data.get("link")
        thread_type = cleaned_data.get("thread_type")

        #if thread_type and self.initial.get('thread_type', thread_type) != thread_type and not self.user.is_staff and not self.has_error('title'):
        #    self.add_error('title', 'You are not allowed to change the thread type')
        if thread_type in Thread.TYPES_WITH_LINK and not self.has_error('link'):
            if not link:
                msg = _("This field is required")
                self.add_error('link', msg)
            else:
                youtube_info = Thread(link=link).parse_youtube_url()
                if youtube_info:
                    exists = Thread.objects.filter(link__contains=youtube_info['id']).exclude(id=self.instance.id)
                    if len(exists):
                        msg = _("Sorry, someone has already posted this video")
                        self.add_error('link', msg)
                elif thread_type == Thread.YOUTUBE:
                    msg = _("This is not a Youtube URL")
                    self.add_error('link', msg)
        elif self.has_error('link') and thread_type not in Thread.TYPES_WITH_LINK:
            del self.errors['link']


class ReplyForm(forms.ModelForm):
    is_answer = forms.BooleanField(required=False)
    class Meta:
        model = Post
        fields = ('text', 'is_answer')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
