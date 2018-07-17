from django.shortcuts import render
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User


from .models import Solution, Subject, Comment
from .forms import SolutionForm


class Index(View):

    def get(self, request, *args, **kwargs):
        print(request.user)
        return render(request, "index.html", {
            'form': SolutionForm(),  # Empty form for the `answer` tab to be POSTed
            'subjects': Subject.objects.all()
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
                solution.author = request.user
                solution.save()
                return HttpResponseRedirect(solution.subject.title_slug + "/" + solution.title_slug)
            else:
                return render(request, 'page_not_found.html', {}) # Page with given title already exists



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

# View for showing a user's profile page. If it's the user's own profile page, add in extra features (such as settings,
# profile edit.
class Profile(View):
    def get(self, request, username, *args, **kwargs):
        try:
            user_arg = User.objects.get(username=username)
            context = {
                'profile':
                    {
                        'username': user_arg.username,
                        'email': user_arg.email
                    }
            }
            return render(request, 'profile.html', context)

        except ObjectDoesNotExist:
            print("Could not find user.")
            return Http404()


class SubjectSolutions(View):
    def get(self, request, subject_slug, *args, **kwargs):
        try:
            subject = Subject.objects.get(title_slug=subject_slug)

            return render(request, 'subject_solutions.html', {
                'page': {'subject': subject},
                'subjects': Subject.objects.all()
            })
        except ObjectDoesNotExist:
            return Http404()
