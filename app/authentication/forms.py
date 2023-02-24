from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=False)
    nordigen_user_id = forms.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email',
                  'nordigen_user_id', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control my-1'
        self.fields['username'].widget.attrs['placeholder'] = '#'
        self.fields['email'].widget.attrs['class'] = 'form-control my-1'
        self.fields['email'].widget.attrs['placeholder'] = '#'
        self.fields['nordigen_user_id'].widget.attrs['class'] = 'form-control my-1'
        self.fields['nordigen_user_id'].widget.attrs['placeholder'] = '#'
        self.fields['password1'].widget.attrs['class'] = 'form-control my-1'
        self.fields['password1'].widget.attrs['placeholder'] = 'form-control my-1'
        self.fields['password2'].widget.attrs['class'] = 'form-control my-1'
        self.fields['password2'].widget.attrs['placeholder'] = 'form-control my-1'


class LoginUserForm(AuthenticationForm):
    # class Meta:
    #     model = get_user_model()
    #     fields = ('username', 'password')
    #     widgets = {
    #         'username': forms.TextInput(attrs={'class': 'form-control my-1'}),
    #         'password': forms.PasswordInput(attrs={'class': 'form-control my-1'}),
    #     }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control my-1'
        self.fields['username'].widget.attrs['placeholder'] = '#'
        self.fields['password'].widget.attrs['class'] = 'form-control my-1'
        self.fields['password'].widget.attrs['placeholder'] = 'form-control my-1'
