from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from vsq.views import *

admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    url(r'^$', EarlyBirdView.as_view(), name='earlybird'),
    url(r'^registration_ok$',TemplateView.as_view(template_name='early_bird_success.html')),
    url(r'^mockup_answer$', mockup_response),
    url(r'^vsq/$', QuestionarioUtente.as_view(), name="questionario_utenti"),
    url(r'^questionario/(?P<party_key>[-\w]+)/$', QuestionarioPartitiView.as_view(), name="questionario_partiti"),
    url(r'^questionario/(?P<slug>[-\w]+)/completato$', QuestionarioPartitiClosed.as_view(), name="questionario_partiti_fine"),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^home/$', HomepageView.as_view(), name='homepage'),
    url(r'^posizione-liste/$', PartyPositionsView.as_view(), name='party-positions'),
    url(r'^temi/(?P<slug>[-\w]+)/$', TopicDetailView.as_view(), name='topic-detail'),
    url(r'^temi/$', TopicListView.as_view(), name='topic-list'),
    url(r'^lista/(?P<slug>[-\w]+)/$', PartitoDetailView.as_view(), name='party-detail'),
    url(r'^rispondi/$', QuestionarioUtenteView.as_view(), name='questionario-utente'),
    url(r'^risultato/(?P<user_key>[\w]+)$', RisultatoUtenteView.as_view(), name='risultato-utente'),
    url(r'^faq/$', FaqListView.as_view(), name='faq-list'),
    url(r'^test500/$', Test500View.as_view(), name='faq-list'),
)

if settings.DEBUG or settings.LOCAL_DEVELOPEMENT:
    urlpatterns += patterns('',
                            url(r'^{0}/(?P<path>.*)$'.format(settings.STATIC_URL.strip('/')), 'django.views.static.serve', {
                                'document_root': settings.STATIC_ROOT,
                                }),
                            )
    urlpatterns += patterns('',
        url(r'^{0}/(?P<path>.*)$'.format(settings.MEDIA_URL.strip('/')), 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )
