from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from vsq.models import Domanda, Utente, Partito, RispostaPartito, RispostaUtente, EarlyBird, Coalizione, Faq

class DomandaAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['testo'] }
    readonly_fields = ('testo_html', 'approfondimento_html', 'accompagno_html')

class RispostaPartitoInline(admin.StackedInline):
    model = RispostaPartito

    extra = 1

class RispostaUtenteInline(admin.StackedInline):
    model = RispostaUtente
    extra = 1

class PartitoAdminWithRisposte(admin.ModelAdmin):

    def questionario_link(self, obj):
        return format_html('<div style="text-align:center"><a href="{}" target="blank">apri</a></div>',
                           reverse('questionario_partiti', kwargs={'party_key': obj.party_key}))

    list_display = ('denominazione', 'coalizione', 'nonorig', 'questionario_link')
    inlines = [RispostaPartitoInline, ]
    prepopulated_fields = { 'slug': ['denominazione'] }

class UtenteAdminWithRisposte(admin.ModelAdmin):
    list_display = ('nickname', 'email', 'created_at', 'ip')
    inlines = [RispostaUtenteInline, ]

class EarlyBirdAdmin(admin.ModelAdmin):
    model=EarlyBird

class CoalizioneAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordine')
    ordering = ('ordine',)
    model= Coalizione
    prepopulated_fields = { 'slug': ['nome'] }

class FaqAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['domanda'] }
    readonly_fields = ('domanda_html', 'risposta_html')


admin.site.register(Domanda, DomandaAdmin)
admin.site.register(Coalizione, CoalizioneAdmin)
admin.site.register(Utente, UtenteAdminWithRisposte)
admin.site.register(Partito, PartitoAdminWithRisposte)
admin.site.register(EarlyBird, EarlyBirdAdmin)
admin.site.register(Faq, FaqAdmin)
