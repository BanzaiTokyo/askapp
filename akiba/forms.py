from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from registration.forms import RegistrationForm


class RecaptchaRegistrationForm(RegistrationForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
