# Is Alive Bot

Telegram bot for checking if a port is open is a host.

The program expect a file `config.yml` but you can pass -f and a config file.
Config file must be like this:

```yaml

servers:
    - name: "pluto"
      host: "10.22.33.44"
      port: 8080

    - name: "donald"
      host: "55.44.33.22"
      port: 80

token: "123456789:ABCDEFGHI_JKLMNOPQRSTUVWXY-Zabc-def"

notify_ids: [111111111, 2222222222]

time_lapse: 30

```

# Docker

Isalivebot support using `Docker` and `docker-compose`.
