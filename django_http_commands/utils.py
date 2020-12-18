import io
import sys
import importlib

from django.conf import settings
from django.core import exceptions
from django.core.exceptions import ImproperlyConfigured
from django.core.management import BaseCommand, get_commands, CommandError, load_command_class


def create_command_parser(command_name):
    """
    Function creating argument parser for a management command
    """
    if isinstance(command_name, BaseCommand):
        # Command object passed in.
        command = command_name
        command_name = command.__class__.__module__.split('.')[-1]
    else:
        # Load the command object by name.
        try:
            app_name = get_commands()[command_name]
        except KeyError:
            raise CommandError("Unknown command: %r" % command_name)

        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            command = app_name
        else:
            command = load_command_class(app_name, command_name)

    return command.create_parser('', command_name)


def evaluate_permission_classes():
    """
    Function creating a list of permission classes from a list[str] setting
    """

    if not isinstance(settings.API_COMMANDS_PERMISSION_CLASSES, (list, tuple)):
        raise exceptions.ImproperlyConfigured("The API_COMMANDS_PERMISSION_CLASSES setting must be a list or a tuple")

    permissions = []

    for permission_class in settings.API_COMMANDS_PERMISSION_CLASSES:
        try:
            module_path, class_ = permission_class.rsplit('.', 1)
            module = importlib.import_module(module_path)
            importlib.reload(module)

            PermissionClass = getattr(module, class_)
            permissions.append(PermissionClass)

        except Exception as e:
            raise ImproperlyConfigured(
                f"Django HTTP Commands - Error occurred while evaluating API_COMMANDS_PERMISSION_CLASSES: {str(e)}"
            )

    return permissions


class Tee:
    """
    Class duplicating stdout and stderr to a specified file stream
    """

    def __init__(self, stream: io.StringIO):
        self.stream = stream

        self.stdout = sys.stdout
        self.stderr = sys.stderr

        sys.stdout = self
        sys.stderr = self

    def write(self, data):

        self.stream.write(data)
        self.stdout.write(data)

    def flush(self):
        self.stream.flush()

    def __enter__(self):
        pass

    def __exit__(self, _type, _value, _traceback):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
