from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.context_processors import request
from vsq.views import *
from vsq.models import EarlyBird
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', EarlyBirdView.as_view(), name='earlybird'),
    url(r'^registration_ok$',TemplateView.as_view(template_name='early_bird_success.html')),
#    url(r'^mockup_answer$', mockup_response),
#    url(r'^questionario/(?P<party_key>[-\w]+)/$', QuestionarioPartitiView.as_view(), name="questionario_partiti"),
#    url(r'^questionario/(?P<slug>[-\w]+)/completato$', QuestionarioPartitiClosed.as_view(), name="questionario_partiti_fine"),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
