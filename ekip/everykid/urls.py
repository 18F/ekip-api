from django.conf.urls import patterns, include, url

from .views import main_landing

urlpatterns = patterns(
    '',
    url(r'^$', main_landing),
)
