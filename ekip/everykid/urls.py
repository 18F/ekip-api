from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import (
    learn, student_pass, pass_exchange, educator_vouchers, EducatorFormPreview,
    fourth_grade_voucher, game_success)

from .forms import EducatorForm

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(
        template_name="index.html"), name="main_landing"),

    # GET YOUR PASS
    url(
        r'get-your-pass/fourth-grader/game-end',
        game_success,
        name="game_success"),
    url(
        r'get-your-pass/fourth-grader/voucher',
        fourth_grade_voucher,
        name="fourth_grade_voucher"),
    url(r'get-your-pass/fourth-grader', student_pass, name="student_pass"),
    url(
        r'get-your-pass/educator/vouchers/', educator_vouchers,
        name="educator_vouchers"),
    url(
        r'get-your-pass/educator', EducatorFormPreview(EducatorForm),
        name="educator_passes"),
    url(r'get-your-pass/', TemplateView.as_view(
        template_name="get-your-pass/index.html"), name="get_your_pass"),

    # PLAN YOUR TRIP
    url(r'plan-your-trip/pass-exchange/', pass_exchange, name="pass_exchange"),
    url(r'plan-your-trip/', TemplateView.as_view(
        template_name="plan-your-trip/index.html"), name="plan_your_trip"),

    # LEARN
    url(r'learn/', learn, name="learn"),
)
