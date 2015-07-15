from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import learn, student_pass, educator_passes, pass_exchange, fourth_grade_voucher

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(
        template_name="index.html"), name="main_landing"),
    url(r'get-your-pass/fourth-grader/voucher', fourth_grade_voucher, name="fourth_grade_voucher"),
    url(r'get-your-pass/fourth-grader', student_pass, name="student_pass"),
    url(r'get-your-pass/educator', educator_passes, name="educator_passes"),
    url(r'get-your-pass/', TemplateView.as_view(
        template_name="get-your-pass/index.html"), name="get_your_pass"),
    url(r'plan-your-trip/pass-exchange/', pass_exchange, name="pass_exchange"),
    url(r'plan-your-trip/', TemplateView.as_view(
        template_name="plan-your-trip/index.html"), name="plan_your_trip"),
    url(r'learn/', learn, name="learn"),
)
