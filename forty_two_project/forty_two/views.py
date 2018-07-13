from django.shortcuts import render
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User


from .models import Solution, Subject, Comment
from .forms import SolutionForm


class Index(View):

    def get(self, request, *args, **kwargs):
        return render(request, "index.html", {
            'form': SolutionForm() # Empty form for the `answer` tab to be POSTed
        })

    # TODO: Add a more appropriate post method to handle post requests to the index
    def post(self, request, *args, **kwargs):
        return Http404()


class AddSolution(View):
    # TODO: Add a more appropriate get method to handle get requests to this url
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('')

    def post(self, request, *args, **kwargs):
        form = SolutionForm(request.POST)

        if form.is_valid():

            form.save(commit=True)  # Enter the form data into the database (title_slug is handled by save())

            if Solution.objects.get(title=request.POST['title']) is not None:
                solution = Solution.objects.get(title=request.POST['title'], description=request.POST['description'])
                solution.subject = Subject.objects.get(title=request.POST['subject_choice'])
                solution.save()
            else:
                return render(request, 'page_not_found.html', {}) # Page with given title alerady exists
            return HttpResponseRedirect(solution.subject.title_slug+"/"+solution.title_slug)

        else:
            print(form.errors)




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


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html', {})