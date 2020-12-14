from django.conf import settings

# permission classes for exposed Management Commands endpoint
API_COMMANDS_PERMISSION_CLASSES = getattr(
    settings, 'API_COMMANDS_PERMISSION_CLASSES', ['rest_framework.permissions.IsAdminUser']
)
