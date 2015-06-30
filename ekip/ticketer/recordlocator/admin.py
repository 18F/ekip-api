from django.contrib import admin

from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    fields = ('record_locator', 'zip_code')

admin.site.register(Ticket, TicketAdmin)
