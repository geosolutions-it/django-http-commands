from django.apps import AppConfig


VERSION = (0, 1, 0)
__version__ = ".".join([str(i) for i in VERSION])
__author__ = "geosolutions-it"
__email__ = "info@geosolutionsgroup.com"
__url__ = "https://github.com/geosolutions-it/django-http-commands"
__license__ = "GNU General Public License"


class DjangoHttpCommandsConfig(AppConfig):
    name = "django_http_commands"
    verbose_name = "Django HTTP Management Commands"

    def ready(self):
        from ._app_utils import parse_management_commands, apply_default_settings

        apply_default_settings()
        parse_management_commands()


default_app_config = "django_http_commands.DjangoHttpCommandsConfig"
