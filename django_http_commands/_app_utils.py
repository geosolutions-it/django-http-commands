from django.conf import settings
from django.db.utils import ProgrammingError
from django.core.management import get_commands

from django_http_commands.models import ManagementCommand
from django_http_commands import settings as defult_settings


def parse_management_commands() -> None:
    """
    Method parsing and managing available management commands
    for exposing them as HTTP API
    """
    commands = get_commands()

    # make sure commands are processed only if the table for ManagementCommand is already created
    try:
        ManagementCommand.objects.first()
    except ProgrammingError as e:
        pass
    else:
        # add management commands to the ManagementCommand table
        for cmd, app in commands.items():
            ManagementCommand.objects.get_or_create(name=cmd, app=str(app))

        # remove commands which are no longer present in the system from ManagementCommand table
        cmds_to_delete = set([cmd.name for cmd in ManagementCommand.objects.all()]) - set(commands.keys())
        if cmds_to_delete:
            ManagementCommand.objects.filter(name__in=cmds_to_delete).delete()


def apply_default_settings():
    """
    Method applying default settings, if they are not present in the project settings
    """

    for name in dir(defult_settings):
        if name.isupper() and not hasattr(settings, name):
            # if setting is not present in settings, update settings with it
            setattr(settings, name, getattr(defult_settings, name))
