from django import forms


class AddLocationForm(forms.Form):
    team_name = forms.CharField(label="Team Name", max_length=100)
    latitude = forms.FloatField(min_value=40.40, max_value=40.50)
    longitude = forms.FloatField(min_value=-80.10, max_value=-79.90)
