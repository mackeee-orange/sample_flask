FROM python:3.6.7

# Env
ENV PYTHONUNBUFFERED 1


RUN mkdir -p /var/www/app
WORKDIR /var/www/app

# 必要なpipパッケージはここに追加していく
RUN pip install --upgrade pip \
    && pip install -r flask Flask-Migrate Flask-SQLAlchemy python-dotenv gunicorn ipython

COPY . .
