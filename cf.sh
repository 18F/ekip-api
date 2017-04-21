echo '-----Starting APP ----------'
cd ekip
newrelic-admin run-program gunicorn ekip.config.wsgi:application
