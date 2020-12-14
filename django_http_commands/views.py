import io

from rest_framework import status, views
from rest_framework.response import Response
from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist

from .models import ManagementCommand
from .utils import create_command_parser, evaluate_permission_classes
from .serializers import ManagementCommandSerializer


class ManagementCommandView(views.APIView):

    permission_classes = evaluate_permission_classes()

    def get(self, request, cmd=None, format=None):

        # --- handle list case ---
        if cmd is None:
            queryset = ManagementCommand.objects.filter(expose=True)
            return Response({'success': True, 'error': None, 'data': ManagementCommandSerializer(queryset, many=True).data})

        # --- handle detail case ---
        # check if Management Command is exposed
        if ManagementCommand.objects.filter(expose=True, name=cmd).first() is None:
            return Response({'success': False, 'error': 'Command not found'}, status=status.HTTP_404_NOT_FOUND)

        # fetch help text of the Command
        parser = create_command_parser(cmd)
        with io.StringIO() as output:
            parser.print_help(output)
            logged_output = output.getvalue()

        return Response({'success': True, 'error': None, 'data': logged_output})

    def post(self, request, cmd=None):
        """
        Method handling command execution order. Expects application/json content type in a following shape:
        {
            "args": [<arg1>, <arg2>],
            "kwargs: {<key1>: <val1>, <key2>: <val2>}
        }
        """

        # --- handle list case ---
        if cmd is None:
            return Response({'success': False, 'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # --- handle detail case ---

        args = request.data.get('args', [])
        kwargs = request.data.get('kwargs', {})

        queryset = ManagementCommand.objects.filter(expose=True)
        try:
            mgmt_cmd = queryset.get(name=cmd)
        except ObjectDoesNotExist:
            return Response({'success': False, 'error': 'Command not found'},
                            status=status.HTTP_404_NOT_FOUND)

        if "--help" in args:
            return Response({'success': False, 'error': 'Forbidden argument: "--help"'},
                            status=status.HTTP_400_BAD_REQUEST)

        with io.StringIO() as output:
            call_command(mgmt_cmd.name, *args, **kwargs, stdout=output)
            logged_output = output.getvalue()

        response = {
            'success': True,
            'error': None,
            'log': logged_output
        }

        return Response(response)
