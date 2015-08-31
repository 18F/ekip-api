echo '-----Starting APP ----------'
cd ekip
newrelic-admin run-program waitress-serve --port=$VCAP_APP_PORT ekip.config.wsgi:application
