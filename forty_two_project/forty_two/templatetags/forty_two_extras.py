from django import template
from django.template.defaultfilters import slugify

from forty_two.models import Solution, Subject, Comment


register = template.Library()

@register.inclusion_tag('tags/relevant_sols.html')
def get_solutions(subject, search_text=''):
    if search_text == '':
        return {
            'solutions': Solution.objects.filter(subject=subject)
        }
    else:
        return {
            'solutions': Solution.objects.filter(
                subject=subject, tags__in=search_text, cause__contains=search_text
            ),
            'subject': subject
        }

@register.filter()
def count_comments(solution):
    return len(Comment.objects.filter(parent_solution=solution))