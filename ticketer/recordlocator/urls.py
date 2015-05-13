from django.conf.urls import url

from . import views

urlpatterns = [
    url(regex=r'^locator/$', view=views.record_locators, name='locator'),
]
