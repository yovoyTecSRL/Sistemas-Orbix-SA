FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install flask gunicorn

RUN apt-get update && apt-get install -y curl gnupg \
  && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs \
  && npm install

EXPOSE 80

CMD ["bash", "levantarserver.sh"]
