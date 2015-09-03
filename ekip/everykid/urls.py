from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from .views import (
    student_pass, pass_exchange, educator_vouchers,
    EducatorFormPreview, fourth_grade_voucher, game_success, field_trip,
    field_trip_details, planyourtrip)

from .forms import EducatorForm

urlpatterns = patterns(
    '',
    url(r'^$', cache_page(60*60)(TemplateView.as_view(
        template_name="index.html")), name="main_landing"),

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
    url(r'get-your-pass/', cache_page(60*60)(TemplateView.as_view(
        template_name="get-your-pass/index.html")), name="get_your_pass"),

    # PLAN YOUR TRIP
    url(r'planyourtrip', planyourtrip, name='redirect_planner'),
    url(
        r'plan-your-trip/field-trip/(?P<slug>[-\w]+)/$',
        cache_page(60*60)(field_trip_details), name="field_trip_details"),
    url(r'plan-your-trip/field-trip/', cache_page(60*60)(field_trip), name="field_trip"),
    url(r'plan-your-trip/pass-exchange/', cache_page(60*60)(pass_exchange), name="pass_exchange"),
    url(r'plan-your-trip/', cache_page(60*60)(TemplateView.as_view(
        template_name="plan-your-trip/index.html")), name="plan_your_trip"),

    # HOW IT WORKS
    url(r'how-it-works/$', cache_page(60*60)(TemplateView.as_view(
        template_name="how-it-works/index.html")), name="how_it_works"),


    # ABOUT
    url(r'about/$', cache_page(60*60)(TemplateView.as_view(
        template_name="about.html")), name="about_ekip"),

    # LEGAL
    url(r'privacy-policy/$', cache_page(60*60)(TemplateView.as_view(
        template_name="legal/privacy.html")), name="privacy_policy"),
)
