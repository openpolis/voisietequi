from django.contrib.sites.models import Site
from django.core.urlresolvers import resolve, Resolver404
from vsq.models import Coalizione, Faq, Domanda
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
        "EARLYBIRD_ENABLED": settings.EARLYBIRD_ENABLE,
        "ELECTION_NAME": settings.ELECTION_NAME,
        "HASHTAG": settings.HASHTAG,
        "PARTY_LEADER": settings.PARTY_LEADER,
        "PARTY_COALITION": settings.PARTY_COALITION,
        "PARTY_TERM": settings.PARTY_TERM,
        "PARTY_TERM_PLURAL": settings.PARTY_TERM_PLURAL,
        "PARTY_TERM_GENDER": settings.PARTY_TERM_GENDER,
        "OF_PARTY_TERM_PLURAL": settings.OF_PARTY_TERM_PLURAL,
        "THE_PARTY_TERM_PLURAL": settings.THE_PARTY_TERM_PLURAL,
        "OTHER_ELECTIONS": settings.OTHER_ELECTIONS,
        "SHOW_PARTY_COALITION": settings.SHOW_PARTY_COALITION,
        "CURRENT_PAGE": page,
        "MEDIA_URL": settings.MEDIA_URL,
        "COALIZIONI": Coalizione.objects.all(),
        "QUESTIONS_COUNT": Domanda.objects.count(),
        "DISQUS_FORUM": settings.DISQUS_FORUM if hasattr(settings, 'DISQUS_FORUM') else '',
        "COMPUTER_URL": settings.COMPUTER_URL if settings.COMPUTER_URL[-1] == '/'
                        else settings.COMPUTER_URL + '/',
        "ELECTION_CODE": settings.ELECTION_CODE,
        "LATEST_FAQ": Faq.objects.order_by('ordine')[:3],
        "SITE_URL": site_url if site_url[-1] == '/' else site_url + '/',
        "CURRENT_URL": site_url + request.path_info,
        "MAILBIN_URL": settings.MAILBIN_URL,
    }
