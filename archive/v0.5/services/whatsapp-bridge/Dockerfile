FROM golang:1.25-bookworm AS builder

WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev && rm -rf /var/lib/apt/lists/*

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=1 GOOS=linux go build -o /whatsapp-bridge .

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates libsqlite3-0 wget && rm -rf /var/lib/apt/lists/*

COPY --from=builder /whatsapp-bridge /usr/local/bin/whatsapp-bridge

ENV WHATSAPP_BRIDGE_ADDR=:8020
ENV WHATSAPP_SESSION_PATH=/data/session/whatsapp.db
ENV BANKABLE_API_URL=http://bankable-api:8080

EXPOSE 8020

CMD ["whatsapp-bridge"]
