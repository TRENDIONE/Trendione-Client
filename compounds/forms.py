from django import forms
from .models import Compound

class CompoundForm(forms.ModelForm):
    class Meta:
        model = Compound
        fields = ['name', 'category', 'description', 'identity_status', 'is_peptide_or_biologic', 'notes']
        widgets = {'description': forms.Textarea(attrs={'rows': 3}), 'notes': forms.Textarea(attrs={'rows': 4})}
