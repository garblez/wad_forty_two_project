from django import template
from forty_two.models import Solution, Subject

register = template.Library()

@register.inclusion_tag('tags/relevant_sols.html')
def get_subject_solutions(subject):
    return {
        'solutions': Solution.objects.all().filter(subject=subject),
        'subject': subject
    }
