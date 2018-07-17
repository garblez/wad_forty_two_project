from django import forms
from datetime import datetime

from .models import Solution, Subject


class SolutionForm(forms.ModelForm):
    subject_choice = forms.CharField(
        widget=forms.Select(choices=tuple(
            (sub.title, sub.title.capitalize()) for sub in Subject.objects.all()),
            attrs={'class': 'col s4 indigo ',
                   'id': 'sol-subject-choice'}
        ),
        initial=("computing science", 'Computing science'),
        label="Subject choice"
    )

    title = forms.CharField(
        max_length=144, widget=forms.TextInput(attrs={
            'class': 'input-field col s8 validate',
            'id': 'sol-title',
            'data-length': '144'
        }),
        label="Title"
    )
    cause = forms.CharField(
        max_length=256, widget=forms.Textarea(attrs={
            'class': 'input-field col s12 materialize-textarea validate',
            'id': 'sol-cause'
        }),
        label="Cause"

    )
    description = forms.CharField(
        max_length=2048, widget=forms.Textarea(attrs={
            'class': 'input-field col s12 materialize-textarea validate',
            'id': 'sol-description',
            'data-length': '2048'
        }), label="Description"
    )

    post_time = forms.DateTimeField(
        widget=forms.HiddenInput(), initial=datetime.now()
    )


    class Meta:
        model = Solution
        fields = ("title", 'cause', 'description', 'subject_choice')
        help_texts = {
            'title': 'Give your solution a title',
            'subject_choice': 'Choose subject',
            'cause': 'Cause',
            'description': 'Description'
        }
        labels = help_texts
