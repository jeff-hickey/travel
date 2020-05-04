import datetime
from datetime import timedelta

from django import forms
from django.utils import timezone

from hotel.models import Location


class CheckOutForm(forms.Form):
    first_name = forms.CharField(max_length=32, required=True)
    first_name.widget.attrs.update(
        {'class': 'form-control'})

    last_name = forms.CharField(max_length=32, required=True)
    last_name.widget.attrs.update(
        {'class': 'form-control'})

    phone = forms.CharField(max_length=64, required=True)
    phone.widget.attrs.update(
        {'class': 'form-control'})

    username = forms.CharField(max_length=64, required=False, disabled=True)
    username.widget.attrs.update(
        {'class': 'form-control'})

    email = forms.EmailField(max_length=128, required=False, disabled=True)
    email.widget.attrs.update(
        {'class': 'form-control'})

    def full_name(self):
        cleaned_data = super().clean()
        first = cleaned_data.get("first_name")
        last = cleaned_data.get("last_name")
        return f"${first} ${last}"


class SearchForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all(),
                                      empty_label="Where are you going?")
    location.widget.attrs.update(
        {'class': 'form-control form-control-sm mw-100'})
    # Arrival date.
    arrival = forms.DateField(widget=forms.DateInput(), initial=timezone.now(),
                              required=False)
    arrival.widget.attrs.update(
        {'class': 'form-control form-control-sm', 'type': 'date',
         'autocomplete': 'off'})

    departure = forms.DateField(widget=forms.DateInput(),
                                initial=timezone.now() + timedelta(days=1),
                                required=False)
    departure.widget.attrs.update(
        {'class': 'form-control form-control-sm', 'type': 'date',
         'autocomplete': 'off'})

    def clean(self):
        cleaned_data = super().clean()
        arrival = cleaned_data.get("arrival")
        departure = cleaned_data.get("departure")
        if arrival and departure:
            if arrival > departure:
                raise forms.ValidationError(
                    "Arrival date is after departure.", code='invalid_dates'
                )
            # TODO: validate against user date.
            if arrival < datetime.date.today():
                raise forms.ValidationError(
                    "Arrival date should be today or a date in the future.",
                    code='arrival_before_today'
                )
