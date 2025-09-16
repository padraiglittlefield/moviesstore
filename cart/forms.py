from django import forms
from .models import CheckoutFeedback

class CheckoutFeedbackForm(forms.ModelForm):
    class Meta:
        model = CheckoutFeedback
        fields = ['name', 'thoughts']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name (optional)'}),
            'thoughts': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'How was your checkout experience?'}),
        }
