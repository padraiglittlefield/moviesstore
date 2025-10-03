from django import forms
from .models import CheckoutFeedback

class CheckoutFeedbackForm(forms.ModelForm):
    class Meta:
        model = CheckoutFeedback
        fields = ['name', 'statement']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional)'
            }),
            'statement': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about your checkout experience...',
                'rows': 4
            })
        }