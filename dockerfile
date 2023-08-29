FROM python:3.10
ENV PYTHONUNBUFFERED=1

RUN pip3 install django_ckeditor
WORKDIR /focus_yt

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt


COPY . .

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]