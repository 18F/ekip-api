from django.conf.urls import patterns, include, url

from .views import (
    main_landing, get_your_pass, plan_your_trip, learn, student_pass,
    educator_passes)

urlpatterns = patterns(
    '',
    url(r'^$', main_landing, name="main_landing"),
    url(r'get-your-pass/fourth-grader', student_pass, name="student_pass"),
    url(r'get-your-pass/educator', educator_passes, name="educator_passes"),
    url(r'get-your-pass/', get_your_pass, name="get_your_pass"),
    url(r'plan-your-trip/', plan_your_trip, name="plan_your_trip"),
    url(r'learn/', learn, name="learn"),
)
