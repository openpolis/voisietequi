from vsq import settings
from vsq.models import RispostaPartito


def main_settings(request):

    return {
        "DEBUG": settings.DEBUG,
        "TEMPLATE_DEBUG": settings.TEMPLATE_DEBUG,
        }