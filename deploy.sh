#!/bin/sh

REGION="hkg"

if ! command -v flyctl >/dev/null 2>&1; then
    printf '\e[33mCould not resolve command - flyctl. So, install flyctl first.\n\e[0m'
    curl -L https://fly.io/install.sh | FLYCTL_INSTALL=/usr/local sh
fi

if [ -z "${APP_NAME}" ]; then
    printf '\e[31mPlease set APP_NAME first.\n\e[0m' && exit 1
fi

flyctl info --app "${APP_NAME}" >/tmp/${APP_NAME} 2>&1;
if [ "$(cat /tmp/${APP_NAME} | grep -o "Could not resolve")" = "Could not resolve" ]; then
    printf '\e[33mCould not resolve app. Next, create the App.\n\e[0m'
    flyctl apps create "${APP_NAME}" >/dev/null 2>&1;

    flyctl info --app "${APP_NAME}" >/tmp/${APP_NAME} 2>&1;
    if [ "$(cat /tmp/${APP_NAME} | grep -o "Could not resolve")" != "Could not resolve" ]; then
        printf '\e[32mCreate app success.\n\e[0m'
    else
        printf '\e[31mCreate app failed.\n\e[0m' && exit 1
    fi
else
    printf '\e[33mThe app has been created.\n\e[0m'
fi

printf '\e[33mNext, create app config file - fly.toml.\n\e[0m'
cat <<EOF >./fly.toml
app = "$APP_NAME"
kill_signal = "SIGINT"
kill_timeout = 5
processes = []

[build]
  image = "yym68686/chatgpt:1.0"

[env]

[experimental]
  auto_rollback = true

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"
  script_checks = []
  [services.concurrency]
    hard_limit = 25
    soft_limit = 20
    type = "connections"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [[services.tcp_checks]]
    grace_period = "1s"
    interval = "15s"
    restart_limit = 0
    timeout = "2s"
EOF
printf '\e[32mCreate app config file success.\n\e[0m'
printf '\e[33mNext, set app secrets and regions.\n\e[0m'

flyctl secrets set WEB_HOOK=${WEB_HOOK} \
                   BOT_TOKEN=${BOT_TOKEN} \
                   NICK=${NICK} \
                   API=${API} \
                   COOKIES=${COOKIES}

flyctl regions set ${REGION}
printf '\e[32mApp secrets and regions set success. Next, deploy the app.\n\e[0m'
flyctl deploy --detach