from django.conf.urls import patterns, include, url
from django.contrib import admin

from nationalparks.api import FederalSiteResource
from redemption.views import get_passes_state, sites_for_state
from redemption.views import redeem_for_site, redeem_confirm

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^ticket/',
        include("ticketer.recordlocator.urls", namespace="recordlocator")),
    url(r'api/passes/', include(FederalSiteResource.urls())),
    url(r'^redeem/', include('redemption.urls')),
)
