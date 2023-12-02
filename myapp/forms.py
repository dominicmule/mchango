from django import forms
from .models import Mchango, Contribution

class MchangoForm(forms.ModelForm):
    class Meta:
        model = Mchango
        fields = ['mchango_name', 'beneficiary_name', 'phone_number', 'start_date', 'end_date']

class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['contributor_name', 'phone_number', 'contribution_amount']