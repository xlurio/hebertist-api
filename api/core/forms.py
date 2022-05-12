from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    """Form to create new users. Includes all required fields, plus a
    repeated password"""
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'date_of_birth']

    def clean_password2(self):
        """Checks if the password and the repeated password are equals"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save provided password in hashed format"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating user. Includes all fields but replace the
    password with admin's disabled password hash display field"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'date_of_birth',
                  'is_staff', 'is_active']
