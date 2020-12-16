## Setting up

To created a `Flask` server using `uwsgi` everytime start my smart car, please follow this [tutorial](https://www.raspberrypi-spy.co.uk/2018/12/running-flask-under-nginx-raspberry-pi/).

## Important Notes
- In order to allow carema access to your server, change `chmod-socket = 664` to `chmod-socket = 777` in `uwsgi.ini`.
