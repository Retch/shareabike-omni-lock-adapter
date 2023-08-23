FROM python:3.11-alpine
LABEL org.opencontainers.image.source="https://github.com/retch/shareabike-omni-lock-adapter"

ENV PYTHONUNBUFFERED 1

ENV BACKEND_HOST_URL http://127.0.0.1
WORKDIR /app
COPY helper_types.py omni_packet.py receive_packets.py main.py requirements.txt /app/
RUN pip install -r requirements.txt
EXPOSE 9679
EXPOSE 8079
CMD ["python", "main.py"]
