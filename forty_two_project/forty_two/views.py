from django.shortcuts import render
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse

from .models import Solution, Subject, Comment


class Index(View):

    def get(self, request, *args, **kwargs):
        return render(request, "index.html", {})


class ShowAnswer(View):

    def get(self, request, subject_slug, solution_slug, *args, **kwargs):

        not_found_context = {}

        try:
            subject = Subject.objects.get(title_slug=subject_slug)
        except ObjectDoesNotExist:
            not_found_context['page'] = {
                'name': subject_slug,
                'type': 'subject'
            }
            return render(request, 'page_not_found.html', not_found_context)

        try:
            solution = Solution.objects.get(title_slug=solution_slug)
        except ObjectDoesNotExist:
            not_found_context['page'] = {
                'name': solution_slug,
                'type': 'solution'
            }
            return render(request, 'page_not_found.html', not_found_context)

        context = {
            'subject': subject,
            'solution': solution,
            'author': solution.author,
            'comments': Comment.objects.filter(solution=solution)
        }

        return render(request, 'solution.html', context)
