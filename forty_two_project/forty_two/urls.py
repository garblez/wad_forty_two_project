from django.conf.urls import url

from .views import Index, ShowAnswer, AddSolution, About

urlpatterns = [
    url(
        r'^solutions/(?P<subject_slug>[\w\-]+)/(?P<solution_slug>[\w\-]+)/',
        ShowAnswer.as_view(),
        name="show_answer"
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
        r'^$',
        Index.as_view(),
        name="index"
    ),
]