#!/usr/bin/env bash
set -e
mkdir -p "$HOME"
unoserver --interface 127.0.0.1 --port 2003 --uno-port 2002 &
until unoping --host 127.0.0.1 --port 2003 >/dev/null 2>&1; do sleep 0.5; done
exec uvicorn server:app --host 0.0.0.0 --port 8080