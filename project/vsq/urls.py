from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from vsq import views

admin.autodiscover()

from django.http import HttpResponse
def counter_view(request):
    return HttpResponse(str(views.Utente.objects.count()))

urlpatterns = [

    #url(r'^$', EarlyBirdView.as_view(), name='earlybird'),
    url(r'^registration_ok$', views.TemplateView.as_view(template_name='early_bird_success.html')),
    url(r'^mockup_answer$', views.mockup_response),
    url(r'^vsq/$', views.QuestionarioUtente.as_view(), name="questionario_utenti"),
    url(r'^questionario/(?P<party_key>[-\w]+)/$', views.QuestionarioPartitiView.as_view(), name="questionario_partiti"),
    url(r'^questionario/(?P<slug>[-\w]+)/completato$', views.QuestionarioPartitiClosed.as_view(), name="questionario_partiti_fine"),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^liste/$', views.PartyPositionsView.as_view(), name='party-positions'),
    url(r'^lista/(?P<slug>[-\w]+)/$', views.PartitoDetailView.as_view(), name='party-detail'),
    url(r'^temi/(?P<slug>[-\w]+)/$', views.TopicDetailView.as_view(), name='topic-detail'),
    url(r'^temi/$', views.TopicListView.as_view(), name='topic-list'),
    url(r'^rispondi/$', views.QuestionarioUtenteView.as_view(), name='questionario-utente'),
    url(r'^risultato/(?P<user_key>[-\w]+)/$', views.RisultatoUtenteView.as_view(), name='risultato-utente'),
    url(r'^faq/$', views.FaqListView.as_view(), name='faq-list'),
    url(r'^privacy/$', views.TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    url(r'^counter/$', counter_view, name='counter'),
    url(r'^iscrizione/$', views.SubscriptionView.as_view(), name='subscribe-url'),
    url(r'^test500/$', views.Test500View.as_view(), name='test-500'),
]

# Works only with DEBUG = True
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)