from django.contrib.sites.models import Site
from django.core.urlresolvers import resolve, Resolver404
from vsq.models import Coalizione, Faq
from django.conf import settings


def main_settings(request):

    try:
        page = resolve(request.path_info).url_name
    except Resolver404:
        page = ''

    site_url = 'http://%s' % Site.objects.get_current().domain

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
        "LATEST_FAQ": Faq.objects.order_by('ordine')[:3],
        "SITE_URL": site_url,
        "CURRENT_URL": site_url + request.path_info
    }