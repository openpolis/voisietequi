# coding=utf-8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.staticfiles.templatetags.staticfiles import static
from markdown import markdown
from model_utils import Choices
from ckeditor.fields import RichTextField

from vsq import fields

class Domanda(models.Model):
    """
    Question asked to politicians, parties and users.

    Testo contains the question, expressed in simple terms.
    Approfondimento contains an analysis of the question, in more elaborated terms.
    Accompagno, is a text shown along, as to guide the user during the poll.
    Link contains a link to a web page where issues related to the question is discussed.
    """

    ORDINE_DOMANDE = [(i,i) for i in range(1, 26, 1)]

    slug = models.SlugField(max_length=settings.SLUG_MAX_LENGTH, unique=True,
                            help_text="Valore suggerito, generato dal testo. Deve essere unico. Sono ammessi i seguenti caratteri [-_a-zA-Z0-9]")
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
            self.slug = slugify(self.testo[:settings.SLUG_MAX_LENGTH])

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
    def risposte(self): return self.rispostapartito_set.all().order_by('partito__coalizione__ordine')

    @property
    def risposte_commentate(self): return self.rispostapartito_set.exclude(risposta_txt='')

    @property
    def risposte_non_commentate(self): return self.rispostapartito_set.filter(risposta_txt='')

    def get_partiti_by_risposta(self, answer):
        # select_related to increase performances
        for risposta in self.rispostapartito_set.all().select_related('partito','partito__coalizione'):
            if risposta.risposta_int == answer:
                yield risposta.partito

    def get_absolute_url(self):
        return reverse('topic-detail', kwargs={'slug': self.slug})

    def __unicode__(self):
        return u"%s] - %s" % (self.ordine, self.testo)


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
    agent:    user's brower UserAgent
    ip:       may have some statistical use in the future
    coord:    json string of triples list (party_key, x, y) of the coordinates
    """
    user_key = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=128, blank=True, null=True)
    agent = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    coord = models.TextField(blank=True, null=True)
    has_sent_emails = models.BooleanField(default=False, blank=True)
    wants_newsletter = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name_plural = "Utenti"

    def __unicode__(self):
        return self.nickname

    def get_answers(self):
        return RispostaUtente.objects.filter(utente=self).order_by('domanda__ordine')


class Coalizione(models.Model):

    nome = models.CharField(max_length=50)
    slug = models.SlugField(help_text="Valore suggerito, generato dal nome. Deve essere unico. Sono ammessi i seguenti caratteri [-_a-zA-Z0-9]")
    colore = fields.RGBColorField()
    ordine = models.IntegerField(blank=False, null=False, default=0)

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
    coord_x:            coordinate x
    coord_y:            coordinate y
    nonorig:            Party has not responded; positions were derived from public declarations
    """

    coalizione = models.ForeignKey(Coalizione)
    denominazione = models.CharField(max_length=255, unique=True)
    party_key = models.SlugField(max_length=255, unique=True,
                                 help_text="Codice univoco utilizzato per generare la url del questionario. Sono ammessi i seguenti caratteri [-_a-zA-Z0-9]")
    sigla = models.CharField(max_length=32, blank=False, null=False, unique=True)
    responsabile_nome = models.CharField(max_length=128, blank=True, null=True)
    responsabile_email = models.EmailField(max_length=128, blank=True, null=True)
    risposte_at = models.DateField(blank=True, null=True, verbose_name='Data risposta')
    sito = models.URLField(blank=True, null=True)
    simbolo = models.ImageField(blank=True, null=True, upload_to='simboli')
    slug = models.SlugField(max_length=settings.SLUG_MAX_LENGTH, blank=True, null=True, unique=True,
                            help_text="Codice univoco utilizzato per generare la url del partito. Sono ammessi i seguenti caratteri [-_a-zA-Z0-9]")
    coord_x = models.FloatField(default=0.0, blank=True)
    coord_y = models.FloatField(default=0.0, blank=True)
    twitter_hashtag = models.CharField(blank=True, null=True, max_length=255)
    twitter_user = models.CharField(blank=True, null=True, max_length=255)
    facebook_url = models.CharField(blank=True, null=True, max_length=255)
    leader = models.CharField(blank=True, null=True, max_length=255)
    nonorig = models.BooleanField(default=False, verbose_name="Non originale")

    description = RichTextField(blank=True, verbose_name=settings.PARTY_DESCRIPTION_TERM)
    linked_parties = RichTextField(blank=True, verbose_name=settings.PARTY_LINKED_PARTIES_TERM)
    election_expenses = fields.CharField(blank=True, max_length=500, verbose_name="Spese elettorali")
    election_expenses_document = models.FileField(blank=True, upload_to='spese-elettorali', verbose_name="Documento delle spese elettorali")
    balance_sheet = fields.CharField(blank=True, max_length=500, verbose_name="Dichiarazione patrimoniale")
    balance_sheet_document = models.FileField(blank=True, upload_to='dichiarazioni-patrimoniali', verbose_name="Documento della dichiarazione patrimoniale")

    @property
    def gender(self):
        last_char = self.denominazione.split()[0][-1]
        if last_char in ('e', 'a'):
            return 'f'
        else:
            return 'm'

    class Meta:
        verbose_name = settings.PARTY_TERM
        verbose_name_plural = settings.PARTY_TERM_PLURAL

    def __unicode__(self):
        if settings.SHOW_PARTY_COALITION:
            return u"{partito} ({coalizione})".format(
                partito=self.denominazione,
                coalizione=self.coalizione
            )
        else:
            return self.denominazione

    @property
    def coordinate(self): return self.coord_x, self.coord_y

    def get_answers(self):
        return RispostaPartito.objects.filter(partito=self).order_by('domanda__ordine')

    def get_answer_for(self, question):
        try:
            return self.rispostapartito_set.get(domanda=question)
        except RispostaPartito.DoesNotExist:
            return None

    def has_replied_to_all_answers(self):
        answers = Domanda.objects.values_list('pk', flat=True)
        return self.rispostapartito_set.filter(domanda_id__in=answers).count() == len(answers)

    @property
    def simbolo_url(self):
        """
        Returns the URL of the image associated with this Object.
        If an image hasn't been uploaded yet, it returns a stock image

        :returns: str -- the image url

        """
        if self.simbolo and hasattr(self.simbolo, 'url'):
            return self.simbolo.url
        else:
            return static('img/no-logo.png')

    def save(self, *args, **kwargs):
        """override save method """

        if self.denominazione and not self.slug:
            self.slug = slugify(self.denominazione[:settings.SLUG_MAX_LENGTH])


        super(Partito, self).save(*args, **kwargs)

    def distanza(self, altro_partito):
        """
        :param altro_partito:
        :type altro_partito: Partito
        """
        return ( ((self.coord_x - altro_partito.coord_x) ** 2) + ((self.coord_y - self.coord_y) ** 2) ) ** 1/2

# function for AJAX response mockup, only for test purpose
    @classmethod
    def get_partiti_list(cls):
        return Partito.objects.all().values('pk','sigla')

    def get_absolute_url(self):
        return reverse('party-detail', kwargs={'slug': self.slug})


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
        if self.risposta_int == 3 and altra_risposta.risposta_int < 0:
            result = abs(2-altra_risposta.risposta_int)
        elif self.risposta_int == -3 and altra_risposta.risposta_int > 0:
            result = abs(-2-altra_risposta.risposta_int)
        else:
            result = abs(self.risposta_int - altra_risposta.risposta_int)
        return result

    class Meta:
        verbose_name_plural = "Risposte partito"
        # unique_together = ['domanda', 'partito']

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

    domanda = RichTextField()
    risposta = RichTextField()
    ordine = models.IntegerField(blank=False, null=False)
    slug = models.SlugField(max_length=settings.SLUG_MAX_LENGTH, unique=True,
                            help_text="Valore suggerito, generato dal testo. Deve essere unico. Sono ammessi i seguenti caratteri [-_a-zA-Z0-9]")

    class Meta:
        verbose_name_plural = "Faq"
        ordering = ['ordine']

    def save(self, *args, **kwargs):
        if self.domanda and not self.slug:
            self.slug = slugify(self.domanda[:settings.SLUG_MAX_LENGTH])

        super(Faq, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('faq-detail', kwargs={'slug': self.slug})

    def __unicode__(self):
        return u"%s - %s" % (self.ordine, self.slug)
