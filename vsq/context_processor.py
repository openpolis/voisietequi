from django.core.urlresolvers import resolve, Resolver404
from vsq import settings
from vsq.models import Coalizione


def main_settings(request):

    try:
        page = resolve(request.path_info).url_name
    except Resolver404:
        page = ''

    return {
        "DEBUG": settings.DEBUG,
        "TEMPLATE_DEBUG": settings.TEMPLATE_DEBUG,
        "CURRENT_PAGE": page,
        "MEDIA_URL": settings.MEDIA_URL,
        "COALIZIONI": Coalizione.objects.all(),
        }