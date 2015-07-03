from django.conf.urls import patterns, include, url
from redemption.views import redeem_confirm, redeem_for_site, sites_for_state
from redemption.views import get_passes_state

urlpatterns = patterns(
    '', 
    url(r'location/(?P<slug>[-\w]+)/$', redeem_for_site),
    url(r'done/(?P<slug>[-\w]+)/$', redeem_confirm),
    url(r'sites/', sites_for_state),
    url(r'^$', get_passes_state),
)
