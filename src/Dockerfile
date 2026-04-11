FROM caddy:2.11.2-alpine

# Install packages and update system
RUN apk update && apk upgrade --no-cache

# allow binding to 80/443 as non-root
RUN apk add --no-cache libcap \
  && setcap 'cap_net_bind_service=+ep' /usr/bin/caddy

# create caddy user if missing (idempotent)
RUN addgroup -S caddy || true \
  && adduser -S -D -H -G caddy caddy || true

# set permissions for caddy user
RUN chown -R caddy:caddy /data /config

# running rootless
USER caddy