# Invisible Ink - Django Server

The Django server provides the REST API for the clients and stores the data.

### Used software

For details see [requirements.txt](requirements.txt)!

* [Django](http://www.djangoproject.com/)
    * [Tastypie](http://django-tastypie.readthedocs.org/) (`django-tastypie`)
    * [OAuth2](http://django-oauth2-provider.readthedocs.org) (`django-oauth2-provider`)
    * [Tastypie Swagger](https://github.com/minism/django-tastypie-swagger) (`django-tastypie-swagger`)
    * [Cron](https://github.com/Tivix/django-cron)  (`django_cron`)

### Run

1. Create a settings file `cp settings-sample.py settings.py` and modify the `SECRET_KEY` in this file (it can't be empty)
2. Install the requirements `pip install -r requirements.txt`
3. Create database tables and a superuser `python manage.py syncdb`
4. Run server `python manage.py runserver`

    Admin site: [http://localhost:8000/admin/](http://localhost:8000/admin/)

    API: [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)
