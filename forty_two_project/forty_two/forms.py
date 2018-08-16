from django import forms
from django.utils.datetime_safe import datetime
from taggit.forms import TagField, TagWidget
from .models import Solution, Subject, Comment, UserProfile



class UserProfileForm(forms.ModelForm):
    description = forms.CharField(
        max_length=256,
        widget=forms.Textarea(attrs={
            'data-length': '256',
            'id': 'profile_description',
            'class': 'input-field materialize-textarea',
            'placeholder': 'Profile description',
        }), empty_value='',
        required=False
    )

    photo = forms.FileField(required=False)

    class Meta:
        model = UserProfile
        fields = ('description', 'photo')


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        max_length=256,
        widget=forms.Textarea(attrs={
            'data-length': '256',
            'id': 'comment_content',
            'class': 'input-field materialize-textarea validate',
        }), empty_value='Enter your comment here...'
    )

    parent_solution_title = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ('content', 'parent_solution_title')


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
        max_length=40, widget=forms.TextInput(attrs={
            'class': 'input-field col s8 validate',
            'id': 'sol-title',
            'data-length': '40'
        }),
        label="Title"
    )

    cause = forms.CharField(
        max_length=80, widget=forms.Textarea(attrs={
            'class': 'input-field col s12 materialize-textarea validate',
            'id': 'sol-cause',
            'data-length': '80'
        }),
        label="Cause"
    )

    description = forms.CharField(
        max_length=512, widget=forms.Textarea(attrs={
            'class': 'input-field col s12 materialize-textarea validate',
            'id': 'sol-description',
            'data-length': '512'
        }), label="Description"
    )

    post_time = forms.DateTimeField(
        widget=forms.HiddenInput(), initial=datetime.now()
    )

    tags = TagField(widget=TagWidget(attrs={
        'placeholder': 'python, programming, django,..'
    }), label="Tags")

    class Meta:
        model = Solution
        fields = ("title", 'cause', 'description', 'tags', 'subject_choice')
        help_texts = {
            'title': 'Give your solution a title',
            'subject_choice': 'Choose subject',
            'cause': 'Cause',
            'description': 'Description',
            'tags': 'Tags'
        }
        labels = help_texts
