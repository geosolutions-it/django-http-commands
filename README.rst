====================
Django HTTP Commands
====================

Django HTTP Commands is a Django app to expose management commands in form of HTTP API.


Quick start
-----------

1. Add "django_http_commands" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'django_http_commands',
    ]

2. Include the Http Commands URLconf in your project urls.py like this::

    path('api/', include('django_http_commands.urls')),

3. Run ``python manage.py migrate`` to create the management commands models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to select which commands should be exposed (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/api/management/ to inspect the API.