from django.conf.urls import url

from .views import Index, ShowAnswer

urlpatterns = [
    url(
        r'^solutions/(?P<subject_slug>[\w\-]+)/(?P<solution_slug>[\w\-]+)/',
        ShowAnswer.as_view(),
        name="show_answer"
    ),
    url(
        r'^$',
        Index.as_view(),
        name="index"
    ),
]