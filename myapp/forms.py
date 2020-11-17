from django import forms
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
                                    label="Preferred course duration:", required=False)
    max_price = forms.IntegerField(label="Maximum Price", validators=[validate_max_price])

