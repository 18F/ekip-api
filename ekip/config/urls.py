from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from nationalparks.api import FederalSiteResource
from ticketer.recordlocator.views import TicketResource

urlpatterns = patterns(
    '',
    url(r'', include('everykid.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('api/tickets/', include(TicketResource.urls())),
    url(r'api/passes/', include(FederalSiteResource.urls())),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/logout/$', auth_views.logout),
    url(r'^redeem/', include('redemption.urls')),
)
