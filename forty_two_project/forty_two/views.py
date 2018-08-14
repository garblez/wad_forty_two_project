from django.shortcuts import render
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from django.core.files.storage import FileSystemStorage

from .models import Solution, Subject, Comment, UserProfile
from .forms import SolutionForm, CommentForm, UserProfileForm


def base_context(request):
    if request.user and request.user.is_authenticated():
        return {'user_photo': UserProfile.objects.get(user=request.user).photo}
    return {}


class Index(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': SolutionForm(),  # Empty form for the `answer` modal to be POSTed
            'subjects': Subject.objects.all()
        }

        context.update(base_context(request))

        return render(request, "index.html", context)

    # TODO: Add a more appropriate post method to handle post requests to the index
    def post(self, request, *args, **kwargs):
        return Http404()


class AddSolution(View):
    # If we receive a GET to the solution/new/ then show a 404. Also for handling invalid forms (for now at least)
    def get(self, request, *args, **kwargs):
        return render(request, 'page_not_found.html', {})

    def post(self, request, *args, **kwargs):
        # The POSTed form was implicitly inherited from Index.get() (the add solution form's action leads here)
        form = SolutionForm(request.POST)

        if form.is_valid():
            print("Form was valid!")  # DEBUG

            form.save(commit=True)  # Enter the form data into the database (title_slug is handled by save())

            if Solution.objects.get(title=request.POST['title']) is not None:
                solution = Solution.objects.get(title=request.POST['title'])
                solution.subject = Subject.objects.get(title=request.POST['subject_choice'])
                solution.author = request.user
                print(request.user)
                solution.save()
                return HttpResponseRedirect(solution.subject.title_slug + "/" + solution.title_slug)
            else:
                return render(request, 'page_not_found.html', {})  # Page with given title already exists
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
            'comments': Comment.objects.filter(parent_solution=solution),
            'form': CommentForm()
        }

        context.update(base_context(request))

        return render(request, 'solution.html', context)

    # We want to add a new comment
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)

        if form.is_valid():
            print("New comment form is valid!")

            solution = Solution.objects.get(title_slug=request.POST['parent_solution_title'])

            comment = Comment.objects.create(
                author=request.user,
                content=request.POST['content'],
                parent_solution=solution
            )

            comment.save()
            return self.get(request, solution.subject.title_slug, solution.title_slug)



# Serve the about page
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html', base_context(request))



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
            'profile': profile_object,
            'comments': Comment.objects.filter(author=user_object),
        }

        context.update(base_context(request))

        return render(request, 'profile.html', context)


# Remove: superfluous
class SubjectSolutions(View):
    def get(self, request, subject_slug, *args, **kwargs):
        try:
            subject = Subject.objects.get(title_slug=subject_slug)

            return render(request, 'subject_solutions.html', {
                'page': {'subject': subject},
                'subjects': Subject.objects.all()
            }.update(base_context(request)))
        except ObjectDoesNotExist:
            return Http404()



class Settings(View):
    def get(self, request, username_slug, *args, **kwargs):
        if slugify(request.user.username) != username_slug:
            return HttpResponseForbidden("You cannot access this page unless you are signed in as that user.")
        context = {
            'profile_form': UserProfileForm(),
            'user_profile': UserProfile.objects.get(user=request.user)
        }

        context.update(base_context(request))

        return render(request, 'settings.html', context)

    def post(self, request, *args, **kwargs):
        user_profile_form = UserProfileForm(request.POST, request.FILES)
        if user_profile_form.is_valid():
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)

            # Change the user's photo only if we supply it in POST
            if user_profile_form.cleaned_data['photo']:
                user_profile.photo = user_profile_form.cleaned_data['photo']

            # Only change the profile description if we've POSTed any changes.
            if user_profile_form.cleaned_data['description']:
                user_profile.description = user_profile_form.cleaned_data['description']

            user_profile.save()
            return HttpResponseRedirect('../'+slugify(request.user.username))

