from django import forms
from django.contrib.auth.forms import UserCreationForm

from myapp.models import Order, Review, Student
from django.core.exceptions import ValidationError


def validate_max_price(value):
    if value < 0:
        raise ValidationError("Max Price cannot be < 0")


class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8, '8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks'),
    ]
    name = forms.CharField(max_length=100, required=False, label="Student Name:")
    length = forms.TypedChoiceField(widget=forms.RadioSelect, choices=LENGTH_CHOICES, coerce=int,
                                    label="Preferred course duration:", required=False, empty_value=0)
    max_price = forms.IntegerField(label="Maximum Price", validators=[validate_max_price])

class loginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'student', 'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(), 'order_type':forms.RadioSelect}
        labels = {'student': u'Student Name', }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'course', 'comments', 'rating']
        widgets = {'course': forms.RadioSelect()}
        labels = {'reviewer': "Please enter a valid email",
                  'rating': "Rating: An integer between 1 (worst) and 5 (best)", }


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=50)

class RegisterForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username', 'email', 'level', 'address', 'province', 'registered_courses',
                  'interested_in']

