## Setting up

To created a `Flask` server using `uwsgi` everytime start my smart car, please follow this [tutorial](https://www.raspberrypi-spy.co.uk/2018/12/running-flask-under-nginx-raspberry-pi/).

## Important Notes
- In order to allow carema access to your server, change `chmod-socket = 664` to `chmod-socket = 777` in `uwsgi.ini`.
- For `I2C` permission problem, please use `sudo usermod -aG i2c www-data` to give access to web server. More details can be found [here](https://lexruee.ch/setting-i2c-permissions-for-non-root-users.html).

## Common debugging commands
- Run uwsgi: `sudo systemctl {start|status|stop|enable} uwsgi.service`
- Debug: `uwsgi --socket 0.0.0.0:8000 --protocol=http -w <your_module_in_uwsgin.ini>` 
