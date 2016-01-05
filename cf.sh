echo '-----Starting APP ----------'
cd ekip
waitress-serve --port=$VCAP_APP_PORT ekip.config.wsgi:application