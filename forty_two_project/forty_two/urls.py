from django.conf.urls import url

from .views import Index, ShowAnswer, AddSolution, About, Profile, SubjectSolutions, Settings

urlpatterns = [
    url(
        r'^solutions/(?P<subject_slug>[\w\-]+)/(?P<solution_slug>[\w\-]+)/',
        ShowAnswer.as_view(),
        name="show_answer"
    ),

    url(
        r'^solutions/(?P<subject_slug>[\w\-]+)/$',
        SubjectSolutions.as_view(),
        name="show_subject"
    ),

    # This is used purely to process a new solution post by a user: they will be redirected to the solution page
    # only once the form has been process and such a solution created.
    url(
        r'^solutions/new$',
        AddSolution.as_view(),
        name="add_solution"
    ),
    url(
        r'^about/$',
        About.as_view(),
        name='about'
    ),
    url(
        r'^$|^home/$',
        Index.as_view(),
        name="index"
    ),
    url(
        r'^profile/(?P<username>[\w\-]+)/$',
        Profile.as_view(),
        name='profile'
    ),
    url('^profile/(?P<username_slug>[\w\-]+)/settings',
        Settings.as_view(),
        name='settings'
    )

]