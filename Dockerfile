FROM python:3.11-alpine
LABEL org.opencontainers.image.source="https://github.com/retch/shareabike-omni-lock-adapter"

ENV PYTHONUNBUFFERED 1

ENV BACKEND_HOST_URL http://127.0.0.1
ENV BACKEND_USERNAME "adapter"
ENV BACKEND_PASSWORD "password"
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY main.py /app/
COPY src/helper_types.py src/omni_packet.py src/receive_packets.py src/backend_http_connector.py /app/src/
EXPOSE 9679
EXPOSE 8079
CMD ["python", "main.py"]
STOPSIGNAL SIGKILL
