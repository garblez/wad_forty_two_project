from django import template
from django.template.defaultfilters import slugify

from forty_two.models import Solution, Subject, Comment


register = template.Library()

@register.inclusion_tag('tags/relevant_sols.html')
def get_subject_solutions(subject):
    return {
        'solutions': Solution.objects.all().filter(subject=subject),
        'subject': subject
    }

@register.filter()
def count_comments(solution):
    return len(Comment.objects.filter(parent_solution=solution))