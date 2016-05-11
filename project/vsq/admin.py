from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from vsq.models import Domanda, Utente, Partito, RispostaPartito, RispostaUtente, EarlyBird, Coalizione, Faq

class DomandaAdmin(admin.ModelAdmin):
    readonly_fields = ('testo_html_safe', 'approfondimento_html_safe', 'accompagno_html_safe')

    def _surround_element(self, el):
        return mark_safe(u'<div style="display:inline-block">%s</div>' % el)

    def testo_html_safe(self, instance):
        return self._surround_element(instance.testo_html or '-- vuoto --')
    testo_html_safe.short_description = "Testo"

    def approfondimento_html_safe(self, instance):
        return self._surround_element(instance.approfondimento_html or '-- vuoto --')
    approfondimento_html_safe.short_description = "Approfondimento"

    def accompagno_html_safe(self, instance):
        return self._surround_element(instance.accompagno_html or '-- vuoto --')
    accompagno_html_safe.short_description = "Accompagno"

    def partiti_count(self):
        if not hasattr(self, '_partiti_count'):
            self._partiti_count = Partito.objects.count()
        return self._partiti_count

    def risposte_partiti(self, instance):
        risposte = instance.risposte.count()
        partiti = self.partiti_count()
        txt = "%d/%d" % (risposte, partiti)
        if risposte == self.partiti_count():
            return format_html('<span style="color:green">{}</span>', txt)
        else:
            return format_html('<span style="color:red">{}</span>', txt)

    prepopulated_fields = { 'slug': ['testo'] }
    list_display = ['__unicode__', 'risposte_partiti', 'link']


class RispostaPartitoInline(admin.StackedInline):
    model = RispostaPartito

    def get_max_num(self, request, obj=None, **kwargs):
        return Domanda.objects.count()

    extra = 1
    ordering = ['domanda__ordine', ]
    readonly_fields = ('domanda', )

    fieldsets = (
        (None, {
            'fields': ('domanda', ('risposta_int', 'risposta_txt', 'nonorig'))
        }),
    )

class RispostaUtenteInline(admin.StackedInline):
    model = RispostaUtente
    extra = 1

class PartitoAdminWithRisposte(admin.ModelAdmin):

    def questionario_link(self, obj):
        return format_html('<div style="text-align:center"><a href="{}" target="blank">apri</a></div>',
                           reverse('questionario_partiti', kwargs={'party_key': obj.party_key}))
    questionario_link.short_description = "Questionario"

    def questionario_completed(self, obj):
        return obj.has_replied_to_all_answers()
    questionario_completed.short_description = "Completato"
    questionario_completed.boolean = True

    prepopulated_fields = {'slug': ('denominazione',),}
    readonly_fields = ('risposte_at', 'coord_x', 'coord_y')
    fieldsets = (
        (None, {
            'fields': (
                'coalizione', 'denominazione', 'sigla', 'party_key', 'simbolo', 'leader',
                'description', 'linked_parties', 'responsabile_email'
            )
        }),
        ('Questionario', {
            'description': "Questi campi vengono popolati dal questionario e dal generatore del grafico delle distanze",
            'classes': ('collapse',),
            'fields': ('responsabile_nome', 'risposte_at', 'nonorig', ('coord_x', 'coord_y'))
        }),
        ('Riferimenti web', {
            'classes': ('collapse',),
            'fields': ('slug', 'sito', 'twitter_user', 'facebook_url', 'twitter_hashtag')
        }),
        ('Informazioni finanziarie', {
            'classes': ('collapse',),
            'fields': (('election_expenses', 'election_expenses_document'), ('balance_sheet', 'balance_sheet_document')),
        }),
    )


    list_display = ('denominazione', 'coalizione', 'nonorig', 'questionario_link', 'questionario_completed')
    inlines = [RispostaPartitoInline, ]

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
