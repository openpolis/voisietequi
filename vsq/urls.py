from django.conf.urls import patterns, include, url
from django.contrib import admin
from vsq.views import QuestionarioPartitiView, QuestionarioPartitiClosed
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
#    url(r'^$', 'vsq.views.home', name='home'),
    url(r'^questionario/(?P<party_key>[-\w]+)/$', QuestionarioPartitiView.as_view(), name="questionario_partiti"),
    url(r'^questionario/(?P<slug>[-\w]+)/completato$', QuestionarioPartitiClosed.as_view(), name="questionario_partiti_fine"),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
