FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      libreoffice-core libreoffice-writer libreoffice-calc libreoffice-impress \
      python3 python3-pip python3-uno \
      fonts-dejavu fonts-liberation

RUN pip3 install --break-system-packages unoserver fastapi "uvicorn[standard]" python-multipart

WORKDIR /app
COPY server.py /app/server.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV HOME=/tmp/lo-home
EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]