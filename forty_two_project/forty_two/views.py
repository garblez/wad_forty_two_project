from django.shortcuts import render
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import User


from .models import Solution, Subject, Comment, UserProfile
from .forms import SolutionForm


class Index(View):

    def get(self, request, *args, **kwargs):
        return render(request, "index.html", {
            'form': SolutionForm(),  # Empty form for the `answer` tab to be POSTed
            'subjects': Subject.objects.all()
        })

    # TODO: Add a more appropriate post method to handle post requests to the index
    def post(self, request, *args, **kwargs):
        return Http404()


class AddSolution(View):
    # If we receive a GET to the solution/new/ then show a 404. Also for handling invalid forms (for now at least)
    def get(self, request, *args, **kwargs):
        return render(request, 'page_not_found.html', {})

    def post(self, request, *args, **kwargs):
        form = SolutionForm(request.POST)

        if form.is_valid():
            print("Form was valid!")  # DEBUG

            form.save(commit=True)  # Enter the form data into the database (title_slug is handled by save())

            if Solution.objects.get(title=request.POST['title']) is not None:
                solution = Solution.objects.get(title=request.POST['title'], description=request.POST['description'])
                solution.subject = Subject.objects.get(title=request.POST['subject_choice'])
                solution.author = request.user
                print(request.user)
                solution.save()
                return HttpResponseRedirect(solution.subject.title_slug + "/" + solution.title_slug)
            else:
                return render(request, 'page_not_found.html', {}) # Page with given title already exists
        else:
            print("Form was not valid!")  # DEBUG
            print(form.errors)
            return HttpResponseRedirect('')  # Call this View's get() to show page_not_found


class ShowAnswer(View):
    # Display a solution's page.
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
            user_object = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse("The requested user does not exist. Sorry!")  # Display the error to the user for now.

        # We requested a valid user who should have a valid profile to display. If not (for whatever reason)
        # we necessarily generate a profile to display as one does not already exist.
        profile_object, just_created = UserProfile.objects.get_or_create(user=user_object)

        context = {
            'profile': profile_object
        }

        return render(request, 'profile.html', {'profile': profile_object})





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
