from django import forms

from hotel.models import Location


class SearchForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all(),
                                      empty_label="Where are you going?")
    location.widget.attrs.update({'class': 'form-control mw-100'})
    # Arrival date.
    arrival = forms.DateField(required=True, input_formats='%Y-%M-%D', )
    arrival.widget.attrs.update(
        {'class': 'form-control', 'placeholder': 'YYYY-MM-DD'})

    departure = forms.DateField(required=True)
    departure.widget.attrs.update(
        {'class': 'form-control', 'placeholder': 'YYYY-MM-DD'})
