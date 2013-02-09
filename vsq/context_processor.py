from django.core.urlresolvers import resolve, Resolver404
from vsq.models import Coalizione
from django.conf import settings


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
        "QUESTIONS_COUNT": 25,
        "DISQUS_FORUM": settings.DISQUS_FORUM if hasattr(settings, 'DISQUS_FORUM') else '',
        "COMPUTER_URL": settings.COMPUTER_URL,
        "ELECTION_CODE": settings.ELECTION_CODE,
    }