from django.conf.urls import url

from forty_two.views import Index

urlpatterns = [
    url(r'^$', Index.as_view(), name="index"),
]