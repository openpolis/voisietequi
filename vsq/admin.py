from django.contrib import admin
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
    inlines = [RispostaPartitoInline, ]
    prepopulated_fields = { 'slug': ['denominazione'] }

class UtenteAdminWithRisposte(admin.ModelAdmin):
    list_display = ('nickname', 'email')
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
