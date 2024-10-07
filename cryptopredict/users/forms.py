from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={
                'rows': 1,  # Reduce the number of visible rows
                'style': 'height: 2.5rem; width: 100%; resize: none;',  # Apply inline CSS for resizing
            }),
        }