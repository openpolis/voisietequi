from django.db import models
from markdown import markdown
from model_utils import Choices

class Domanda(models.Model):
    """
    Question asked to politicians, parties and users.

    Testo contains the question, expressed in simple terms.
    Approfondimento contains an analysis of the question, in more elaborated terms.
    Accompagno, is a text shown along, as to guide the user during the poll.
    Link contains a link to a web page where issues related to the question is discussed.
    """

    ORDINE_DOMANDE = [(i,i) for i in range(1,26,1)]

    slug = models.SlugField(max_length=200, unique=True,
                            help_text="Valore suggerito, generato dal testo. Deve essere unico.")
    testo = models.TextField()
    testo_html = models.TextField(editable=False)
    approfondimento = models.TextField(blank=True, null=True)
    approfondimento_html = models.TextField(editable=False, blank=True, null=True)
    accompagno = models.TextField(blank=True, null=True)
    accompagno_html = models.TextField(editable=False, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    ordine = models.IntegerField(blank=False, null=False, choices=ORDINE_DOMANDE)


    class Meta:
      verbose_name_plural = "Domande"

    def save(self, *args, **kwargs):
        """override save method and transform markdown into html"""
        if self.testo:
            self.testo_html = markdown(self.testo)
        if self.approfondimento:
            self.approfondimento_html = markdown(self.approfondimento)
        super(Domanda, self).save(*args, **kwargs)

    @classmethod
    def get_domande(self):
        return  Domanda.objects.order_by('ordine')

    def __unicode__(self):
        return self.slug


class Utente(models.Model):
    """
    Users are anonymous, login is never required.
    A nickname is required, but no verification is performed.
    Users can leave their email, to contact other users.

    A user can answer the poll only once.

    nickname: shown in graphics
    user_key: an hash used to create a permalink for users' polls
    date:     user's creation timestamp
    email:    user's email, if inserted by the user
    ip:       may have some statistical use in the future
    """
    user_key = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=128, blank=True, null=True)
    ip = models.IPAddressField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Utenti"

    def __unicode__(self):
        return self.email


class Partito(models.Model):
    """
    Models the political party.
    A responsible person is contacted by our editors and answers the questions,
    before the site goes public.
    The date when the answers are given is recorded in risposte_at.
    A symbol, a color and a coalition, can be assigned

    denominazione:      Complete, official name of the party
    party_key:          Hash to send the html form for collecting answers
    sigla:              Acronym, to be used in tables and report
    responsabile_nome:  Name of the party's speaker
    responsabile_mail:  Email of speaker
    risposte_at:        Date when the answers where given (None, if not given)
    sito:               Official web site of the party
    simbolo:            Official symbol of the party
    colore:             Color used in our graphic
    coalizione:         Coalition, a simple string that may be used in graphics and reports
    """
    COLORS = Choices(
        ('WHITE', 'bianco'),
        ('RED', 'rosso'),
        ('GREEN', 'verde'),
    )

    denominazione = models.CharField(max_length=255, unique=True)
    party_key = models.CharField(max_length=255, unique=True)
    sigla = models.CharField(max_length=32, blank=True, null=True)
    responsabile_nome = models.CharField(max_length=128, blank=True, null=True)
    responsabile_email = models.EmailField(max_length=128, blank=True, null=True)
    risposte_at = models.DateField(blank=True, null=True)
    sito = models.URLField(blank=True, null=True)
    simbolo = models.ImageField(blank=True, null=True, upload_to='simboli')
    colore = models.CharField(max_length=16, blank=True, null=True, choices=COLORS)
    coalizione = models.CharField(max_length=32, blank=True, null=True)
    slug = models.SlugField(max_length=60, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Partiti"

    def __unicode__(self):
        return self.denominazione


class RispostaPartito(models.Model):
    """
    domanda:      Foreign key to Domanda
    partito:      Foreign key to Partito
    risposta_int: Graded response
    risposta_txt: Textual response
    nonorig:      True if the answer is non original (derived from declarations and media)
    """
    TIPO_RISPOSTA = Choices(
        (-3, 'moltocontrario', 'Molto contrario/a'),
        (-2, 'contrario', 'Contrario/a'),
        (-1, 'tendenzialmentecontrario', 'Tendenzialmente contrario/a'),
        ( 1, 'tendenzialmentefavorevole', 'Tendenzialmente favorevole'),
        ( 2, 'favorevole', 'Favorevole'),
        ( 3, 'moltofavorevole', 'Molto favorevole'),
    )

    domanda = models.ForeignKey(Domanda)
    partito = models.ForeignKey(Partito)
    risposta_int = models.SmallIntegerField(null=False, choices=TIPO_RISPOSTA, verbose_name="Risposta")
    risposta_txt = models.TextField(blank=True, null=True, verbose_name="Risposta testuale")
    nonorig = models.BooleanField(default=False, verbose_name="Non originale")

    class Meta:
        verbose_name_plural = "Risposte partito"

#    restituisce le stringhe delle varie risposte possibili, al solo fine della visualizzazione
    @classmethod
    def get_tipo_risposta(cls):
        risposte=[]
        for tr in RispostaPartito.TIPO_RISPOSTA:
            risposte.append(tr[1])
        return risposte


class RispostaUtente(models.Model):
    """
    domanda:      Foreign key to Domanda
    utente:       Foreign key to Utente
    risposta_int: Graded response
    """
    TIPO_RISPOSTA = Choices(
        (-3, 'Molto contrario/a'),
        (-2, 'Contrario/a'),
        (-1, 'Tendenzialmente contrario/a'),
        ( 1, 'Tendenzialmente favorevole'),
        ( 2, 'Favorevole'),
        ( 3, 'Molto favorevole'),
    )

    domanda = models.ForeignKey(Domanda)
    utente = models.ForeignKey(Utente)
    risposta_int = models.SmallIntegerField(choices=TIPO_RISPOSTA, verbose_name="Risposta")

    class Meta:
        verbose_name_plural = "Risposte utente"
