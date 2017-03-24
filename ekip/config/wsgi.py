"""
WSGI config for ticketer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

from cfenv import AppEnv
import newrelic.agent
import os

from django.core.wsgi import get_wsgi_application

env = AppEnv()
# Initialize New Relic monitoring if on Cloud Foundry
ekip_creds = env.get_service(name='ekip-newrelic')
if ekip_creds is not None:
    new_relic_license = ekip_creds.credentials['NEW_RELIC_LICENSE_KEY']
    new_relic_app_name = os.environ.get('NEW_RELIC_APP_NAME')
    if new_relic_license and new_relic_app_name:
        new_relic_settings = newrelic.agent.global_settings()
        new_relic_settings.license_key = new_relic_license
        new_relic_settings.app_name = new_relic_app_name
        print('Initializing New Relic monitoring')
        newrelic.agent.initialize()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
application = get_wsgi_application()
