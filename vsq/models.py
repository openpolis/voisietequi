# coding=utf-8
from datetime import datetime
from django.db import models
from markdown import markdown
from model_utils import Choices
from django.template.defaultfilters import slugify
from settings import SLUG_MAX_LENGTH
from vsq import fields

class Domanda(models.Model):
    """
    Question asked to politicians, parties and users.

    Testo contains the question, expressed in simple terms.
    Approfondimento contains an analysis of the question, in more elaborated terms.
    Accompagno, is a text shown along, as to guide the user during the poll.
    Link contains a link to a web page where issues related to the question is discussed.
    """

    ORDINE_DOMANDE = [(i,i) for i in range(1,26,1)]

    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True,
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
        ordering = ['ordine']

    def save(self, *args, **kwargs):
        """override save method and transform markdown into html"""
        if self.testo:
            self.testo_html = markdown(self.testo)
        if self.approfondimento:
            self.approfondimento_html = markdown(self.approfondimento)
        if self.testo:
            self.slug = slugify(self.testo[:SLUG_MAX_LENGTH])

        super(Domanda, self).save(*args, **kwargs)

    @classmethod
    def get_domande(self):
        return  Domanda.objects.all()

    @classmethod
    def get_n_domande(cls):
        return Domanda.objects.count()

    def _get_by_ordine(self, ordine):
        if not (1 <= ordine <= 25):
            return None
        try:
            return Domanda.objects.get(ordine=ordine)
        except (Domanda.DoesNotExist, Domanda.MultipleObjectsReturned):
            return None

    def next_by_ordine(self):
        return self._get_by_ordine( self.ordine + 1 )

    def prev_by_ordine(self):
        return self._get_by_ordine( self.ordine - 1 )

    @property
    def risposte(self): return self.rispostapartito_set.all()

    @property
    def risposte_commentate(self): return self.rispostapartito_set.filter(risposta_txt__isnull=False)

    @property
    def risposte_non_commentate(self): return self.rispostapartito_set.filter(risposta_txt__isnull=True)

    def get_partiti_by_risposta(self, answer):
        # select_related to increase performances
        for risposta in self.rispostapartito_set.all().select_related('partito','partito__coalizione'):
            if risposta.risposta_int == answer:
                yield risposta.partito

    @models.permalink
    def get_absolute_url(self):
        return ('topic-detail', (), {'slug': self.slug})

    def __unicode__(self):
        return u"%s - %s" % (self.id, self.slug)


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
    nickname = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=128, blank=True, null=True)
    ip = models.IPAddressField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Utenti"

    def __unicode__(self):
        return self.email


class Coalizione(models.Model):

    nome = models.CharField(max_length=50)
    slug = models.SlugField()
    colore = fields.RGBColorField()

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Coalizioni"


class Partito(models.Model):
    """
    Models the political party.
    A responsible person is contacted by our editors and answers the questions,
    before the site goes public.
    The date when the answers are given is recorded in risposte_at.
    A symbol, a color and a coalition, can be assigned

    coalizione:         Coalition
    denominazione:      Complete, official name of the party
    party_key:          Hash to send the html form for collecting answers
    sigla:              Acronym, to be used in tables and report
    responsabile_nome:  Name of the party's speaker
    responsabile_mail:  Email of speaker
    risposte_at:        Date when the answers where given (None, if not given)
    sito:               Official web site of the party
    simbolo:            Official symbol of the party
    """

    coalizione = models.ForeignKey(Coalizione)
    denominazione = models.CharField(max_length=255, unique=True)
    party_key = models.CharField(max_length=255, unique=True)
    sigla = models.CharField(max_length=32, blank=False, null=False, unique=True)
    responsabile_nome = models.CharField(max_length=128, blank=True, null=True)
    responsabile_email = models.EmailField(max_length=128, blank=True, null=True)
    risposte_at = models.DateField(blank=True, null=True)
    sito = models.URLField(blank=True, null=True)
    simbolo = models.ImageField(blank=True, null=True, upload_to='simboli')
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, blank=True, null=True, unique=True)

    class Meta:
        verbose_name_plural = "Partiti"

    def __unicode__(self):
        return u"{partito} ({coalizione})".format(
            partito=self.denominazione,
            coalizione=self.coalizione
        )

    def get_answers(self):
        return RispostaPartito.objects.filter(partito=self).order_by('domanda__ordine')

    def save(self, *args, **kwargs):
        """override save method """

        if self.denominazione and not self.slug:
            self.slug = slugify(self.denominazione[:SLUG_MAX_LENGTH])


        super(Partito, self).save(*args, **kwargs)

# function for AJAX response mockup, only for test purpose
    @classmethod
    def get_partiti_list(cls):
        return Partito.objects.all().values('pk','sigla')

    @models.permalink
    def get_absolute_url(self):
        return ('party-detail', (), {'slug': self.slug})


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

    def distanza(self, altra_risposta):
        """
        :param altra_risposta:
        :type altra_risposta: RispostaPartito
        """
        if self.risposta_int == altra_risposta.risposta_int:
            return 0
        mod_x = abs(self.risposta_int)
        mod_y = abs(altra_risposta.risposta_int)
        if (self.risposta_int > 0 and altra_risposta.risposta_int < 0) or (self.risposta_int < 0 and altra_risposta.risposta_int > 0):
            return mod_y + 2
        if mod_x > mod_y:
            return { 1: 2, 2: 1 }[mod_y]
        else:
            return mod_y - mod_x

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
        (-3, 'moltocontrario', 'Molto contrario/a'),
        (-2, 'contrario', 'Contrario/a'),
        (-1, 'tendenzialmentecontrario', 'Tendenzialmente contrario/a'),
        ( 1, 'tendenzialmentefavorevole', 'Tendenzialmente favorevole'),
        ( 2, 'favorevole', 'Favorevole'),
        ( 3, 'moltofavorevole', 'Molto favorevole'),
    )

    domanda = models.ForeignKey(Domanda)
    utente = models.ForeignKey(Utente)
    risposta_int = models.SmallIntegerField(choices=TIPO_RISPOSTA, verbose_name="Risposta")

    class Meta:
        verbose_name_plural = "Risposte utente"



class EarlyBird(models.Model):
    """
    Class that stores the emails of the people who want to be alerted when the website will be online
    """
    email = models.EmailField(unique=True,error_messages={'unique':"Attenzione: indirizzo email già inserito."})


    class Meta:
        verbose_name_plural = "Utenti Early Bird"

    def __unicode__(self):
        return self.email



class Faq(models.Model):

    domanda = models.TextField()
    domanda_html = models.TextField(editable=False)
    risposta = models.TextField()
    risposta_html = models.TextField(editable=False)
    ordine = models.IntegerField(blank=False, null=False)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True,
                            help_text="Valore suggerito, generato dal testo. Deve essere unico.")

    class Meta:
        verbose_name_plural = "Faq"
        ordering = ['ordine']

    def save(self, *args, **kwargs):
        """override save method and transform markdown into html"""
        if self.domanda:
            self.domanda_html = markdown(self.domanda)
        if self.risposta:
            self.risposta_html = markdown(self.risposta)
        if self.domanda:
            self.slug = slugify(self.domanda[:SLUG_MAX_LENGTH])

        super(Faq, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return 'faq-detail', (), {'slug': self.slug}

    def __unicode__(self):
        return u"%s - %s" % (self.ordine, self.slug)
