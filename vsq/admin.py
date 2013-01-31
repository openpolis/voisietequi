from django.contrib import admin
from vsq.models import Domanda, Utente, Partito, RispostaPartito, RispostaUtente, EarlyBird, Coalizione

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
    inlines = [RispostaUtenteInline, ]

class EarlyBirdAdmin(admin.ModelAdmin):
    model=EarlyBird

class CoalizioneAdmin(admin.ModelAdmin):
    model= Coalizione
    prepopulated_fields = { 'slug': ['nome'] }


admin.site.register(Domanda, DomandaAdmin)
admin.site.register(Coalizione, CoalizioneAdmin)
admin.site.register(Utente, UtenteAdminWithRisposte)
admin.site.register(Partito, PartitoAdminWithRisposte)
admin.site.register(EarlyBird, EarlyBirdAdmin)
