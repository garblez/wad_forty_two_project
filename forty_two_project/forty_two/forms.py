from django import forms
from datetime import datetime

from .models import Solution, Subject


class SolutionForm(forms.ModelForm):
    title = forms.CharField(
        max_length=144, widget=forms.TextInput(attrs={'class': 'input-field'}),
        help_text="Give your solution a title."
    )
    cause = forms.CharField(
        max_length=256, widget=forms.Textarea(attrs={'class': 'input-field materialize-textarea'}),
        help_text="How did you find the answer?"
    )
    description = forms.CharField(
        max_length=2048, widget=forms.Textarea(attrs={'class': 'input-field materialize-textarea'}),
        help_text="Description"
    )

    subject_choice = forms.CharField(
        widget=forms.Select(choices=tuple(
            (sub.title, sub.title.capitalize()) for sub in Subject.objects.all()),
        ),
        help_text="Subject", initial=("computing science", 'Computing science')

    )


    post_time = forms.DateTimeField(
        widget=forms.HiddenInput(), initial=datetime.now()
    )

    # DEBUG
    author = forms.CharField(
        max_length=50,
        initial='mak',
        widget=forms.HiddenInput()
    )


    class Meta:
        model = Solution
        fields = ("title", 'cause', 'description', 'subject_choice')
