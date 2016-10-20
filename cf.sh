echo '-----Starting APP ----------'
cd ekip
newrelic-admin run-program waitress-serve --port=$PORT ekip.config.wsgi:application
