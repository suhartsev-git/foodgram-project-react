FROM python:3.9 
WORKDIR /app 
COPY . . 
RUN pip install -r requirements.txt 
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
ONBUILD RUN python manage.py makemigrations
ONBUILD RUN python manage.py migrate
ONBUILD RUN python manage.py import_ingredients
ONBUILD RUN python manage.py collectstatic --noinput