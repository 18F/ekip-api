from django.contrib import admin

from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    fields = (
        'record_locator', 'zip_code', 'redemption_entry', 'recreation_site')

admin.site.register(Ticket, TicketAdmin)
