from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'first/one$', TemplateView.as_view(
        template_name='first-game/start.html'), name='first_game_start'),
    url(r'first/two$', TemplateView.as_view(
        template_name='first-game/infographic.html'),
        name='first_game_infographic'),
    url(r'first/three$', TemplateView.as_view(
        template_name='first-game/endangered.html'),
        name='first_game_endangered'),
    url(r'first/four$', TemplateView.as_view(
        template_name='first-game/lands_map.html'),
        name='first_game_lands_map'),
)
