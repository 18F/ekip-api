from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (
    nature_walk, nature_walk_end, time_travel, time_travel_end, swimming,
    swimming_end, game_start, choose_adventure_type)

urlpatterns = [
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

    url(r'adventure/start', game_start, name='adventure_start'),
    url(r'adventure/choose-adventure', choose_adventure_type, name='choose_adventure_type'),

    # Choose your own adventure.

    url(r'adventure/nature-walk/end', nature_walk_end, name='nature_walk_end'),
    url(r'adventure/nature-walk', nature_walk, name='adventure_nature_walk'),

    url(r'adventure/time-travel/end', time_travel_end, name='time_travel_end'),
    url(r'adventure/time-travel', time_travel, name='adventure_time_travel'),

    url(r'adventure/swimming/end', swimming_end, name='swimming_end'),
    url(r'adventure/swimming', swimming, name='adventure_swimming'),
]
