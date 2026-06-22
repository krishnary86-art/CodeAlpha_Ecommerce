from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your full shipping address'}),
        label='Shipping Address',
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number'}),
        label='Phone Number',
    )
