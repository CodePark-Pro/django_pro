from django import forms
from PIL import Image
from django.contrib.auth import get_user_model

class RegistrationForm(forms.Form):
    username = forms.CharField(label='ユーザー名')
    password = forms.CharField(label='パスワード')
    email = forms.EmailField(label='メールアドレス')

class LoginForm(forms.Form):
    username = forms.CharField(label='ユーザー名')
    password = forms.CharField(label='パスワード')


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'icon', 'introduction')
        widgets = {
            'introduction': forms.Textarea(
                attrs={'rows': 3, 'cols': 50}
            ),
        }
