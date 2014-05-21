from django import http
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.serializers import serialize
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils.functional import curry
from django.views.generic import TemplateView, DetailView, CreateView, ListView, View
import feedparser
from vsq.models import Partito, RispostaPartito, Domanda, EarlyBird, Utente, Faq, RispostaUtente, Coalizione
from django.shortcuts import redirect, render_to_response, get_object_or_404
from vsq.forms import QuestionarioPartitiForm, EarlyBirdForm, SubscriptionForm
from vsq.utils import quantile
from datetime import datetime
from settings_local import PROJECT_ROOT, MANAGERS
from settings import MIN_GRAPH_X, MIN_GRAPH_Y, MAX_GRAPH_X, MAX_GRAPH_Y
import random
import json
from json.encoder import JSONEncoder
from django.core.cache import cache

class QuestionarioUtente(TemplateView):
    template_name = "q_utenti.html"

    def get_context_data(self, **kwargs):
        context = super(QuestionarioUtente, self).get_context_data(**kwargs)

#        passa al contesto i colori associati ai partiti per il grafico finale
        context['partiti_color']=Partito.objects.all().\
            annotate(c=Count('rispostapartito')).\
            filter(c__gt=0).values('sigla','coalizione__colore')

        return context

class QuestionarioPartitiView(TemplateView):

    context = {}
    template_name = "q_partiti.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        questions = Domanda.get_domande()
        form= QuestionarioPartitiForm(self.request.POST , extra=questions)
        p = get_object_or_404(Partito, party_key=kwargs['party_key'])

        if form.is_valid():
            #        controlla e salva le risposte
            p.responsabile_nome = form.cleaned_data['contact_name']
            p.risposte_at = datetime.now()

            for d in questions:
                c,t = form.get_answer(d.ordine)
                rp = RispostaPartito(partito=p,domanda=d, risposta_int=c, risposta_txt=t)
                rp.save()

            p.save()

#            manda una mail ai managers dell'applicazione con il link per controllare i risultati del questionario
            template = get_template("q_partiti_alert_mail.html")
            context=Context(
                {
                    'nome_lista':p.denominazione,
                    'url_link':PROJECT_ROOT + "questionario/" + p.slug + "/completato",
                }
            )
            text_c = template.render(context)
            subj = "VoiSieteQui - La lista " + p.denominazione + " ha completato il questionario"
            from_email = "noreply@voisietequi.it"
            to_address=[]
            for m in MANAGERS:
                to_address.append(m[1])
            msg= EmailMessage(
                subj,
                text_c,
                from_email,
                to_address,
            )
            msg.send()

            return redirect("questionario_partiti_fine",slug=p.slug)
        else:
            context['has_errors']="True"


#       stampa la form con gli eventuali errori
        context['form']=form
        return self.render_to_response(context)


    #se la chiave del questionario e' gia' stata utilizzata e il questionario e' stato salvato correttamente
    #fa un redirect verso la pagina finale di quella lista
    def get(self, request, *args, **kwargs):
        party_key = kwargs['party_key']
        p = get_object_or_404(Partito, party_key=party_key)
        if RispostaPartito.objects.filter(partito=p).count()>0 :
            return redirect("questionario_partiti_fine",slug=p.slug)

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


    def get_context_data(self, **kwargs ):

        context = super(QuestionarioPartitiView, self).get_context_data(**kwargs)
        questions = Domanda.get_domande()
        n_questions=Domanda.get_n_domande()
        form= QuestionarioPartitiForm( extra=questions)

        party_key = kwargs['party_key']
        p = get_object_or_404(Partito, party_key=party_key)

        context['nome_lista']=p.denominazione
        context['n_questions']=n_questions
        context['form']=form
        context['possible_answers']=RispostaPartito.get_tipo_risposta()

        return context


class QuestionarioPartitiClosed(TemplateView):
    template_name = "q_partiti_fine.html"

    #se lo slug del partito esiste e il partito ha gia' risposto prosegue con la pagina dei risultati
    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        p = get_object_or_404(Partito, slug=slug)
        if RispostaPartito.objects.filter(partito=p).count()<0 :
            raise Http404

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(QuestionarioPartitiClosed, self).get_context_data(**kwargs)
        p = get_object_or_404(Partito, slug=kwargs['slug'])

        context['nome_lista']=p.denominazione
        context['n_questions']=Domanda.get_n_domande()
        context['nome_responsabile']=p.responsabile_nome
        context['answers']=p.get_answers()

        return context


class EarlyBirdView(CreateView):
    template_name = 'early_bird.html'
    success_url = 'registration_ok'
    form_class = EarlyBirdForm
    model = EarlyBird

    def get_context_data(self, **kwargs):
        return super(EarlyBirdView, self).get_context_data(partiti=Partito.objects.filter(simbolo__isnull=False).all(), **kwargs)


class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return json.loads(serialize('json', obj))
        return JSONEncoder.default(self,obj)

dumps = curry(json.dumps, cls=DjangoJSONEncoder)

def mockup_response(request):

    partiti_list=Partito.get_partiti_list()
    dict={}
#    adds mockup results for Partiti
    for p in partiti_list:
        dict[str(p['pk'])]=[
                p['sigla'],
                random.uniform(MIN_GRAPH_X, MAX_GRAPH_X),
                random.uniform(MIN_GRAPH_Y, MAX_GRAPH_Y)
            ]

#    adds mockup results for the user
    dict['user']=[
        'user',
        random.uniform(MIN_GRAPH_X, MAX_GRAPH_X),
        random.uniform(MIN_GRAPH_Y, MAX_GRAPH_Y)
    ]

    response = {
                'posizioni': dict,
                'codice_utente': 'XYZ',

        }
    content=json.dumps(response)

    return HttpResponse(content,
        content_type='application/json',
    )


class HomepageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView,self).get_context_data(**kwargs)
        context['conteggio_utenti'] = Utente.objects.count()

        # rimosso, era una patch messa prima del vsq13
        # context['partiti_up'] = Partito.objects.\
        #     filter(coalizione__in=(3, 6, 7, 4)).order_by('coalizione__ordine').select_related('coalizione')
        # context['partiti_dn'] = Partito.objects. \
        #     filter(coalizione__in=(8, 2, 5, 1)).order_by('coalizione__ordine').select_related('coalizione')

        context['partiti'] = liste = Partito.objects.all().order_by('coalizione__ordine').select_related('coalizione')
        context['partiti_non_orig'] = [p for p in liste if p.nonorig]
        coordinate = []
        for l in liste:
            coord = [l.sigla, l.coord_x, l.coord_y]
            coordinate.append(coord)
        context['coordinate'] = json.dumps(coordinate)

        # create a list of pairs,
        # where first element is a instance of Domanda
        # and second is a list of aggregate count, answer by answer.
        # (domanda1, [ ['Molto Contrario', 54321], ['Contrario', 54321], ...  ]),
        # (domanda2, [ ['Molto Contrario', 12345], ['Contrario', 54321], ...  ]),
        # ...
        conteggio_risposte = cache.get('conteggio_risposte')
        if conteggio_risposte is None:
            try:
                with open(settings.RESULTS_DUMP) as f:
                    import csv
                    domande = Domanda.objects.all()
                    reader = csv.DictReader(f)
                    headers = list(reader.fieldnames)
                    conteggio_risposte = []
                    for row in reader:
                        conteggio_risposte.append((
                            filter(lambda x: x.ordine == int(row['Ordine']), domande)[0],
                            [(x, row[x]) for x in headers[2:]]
                        ))
                cache.set('conteggio_risposte', conteggio_risposte)
            except IOError:
                # if not exists, display images of parties
                cache.set('conteggio_risposte', False)
                conteggio_risposte = []

        context['conteggio_risposte'] = conteggio_risposte

        blog_posts = cache.get('blog_posts')
        if blog_posts is None:
            try:
                blog_posts = feedparser.parse('http://blog.openpolis.it/categorie/%s/feed/' % settings.OP_BLOG_CATEGORY).entries[:3]
                cache.set('blog_posts', blog_posts)
            except:
                blog_posts = []
                cache.set('blog_posts', False)
        context['op_blog_posts'] = blog_posts

        return context


class SubscriptionView(HomepageView):

    def post(self, request, *args, **kwargs):
        # initialize form with POST data
        self.form = SubscriptionForm(request.POST)

        if self.form.is_valid():
            # send to zmq
            import zmq
            context = zmq.Context()
            print 'connecting to %s' % settings.MAILBIN_URL

            # socket to sending messages to save
            save_sender = context.socket(zmq.PUSH)
            print 'initialize sender socket in PUSH mode'

            try:
                save_sender.connect(settings.MAILBIN_URL)
            except Exception, e:
                print "Error connecting: %s" % e
            data = {
                # 'first_name': '',
                # 'last_name': '',
                'email': self.form.cleaned_data['email'],
                'ip_address': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT'),
                'service_uri': settings.MAILBIN_SERVICE
            }
            # send message to receiver
            save_sender.send_json(data)

            # set success message in user cookie
            from django.contrib import messages
            messages.add_message(request, messages.INFO, 'Iscrizione avvenuta con successo.', extra_tags='email')
            return redirect('homepage')

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubscriptionView, self).get_context_data(**kwargs)

        if not hasattr(self, 'form') and self.request.method == 'GET':
            # initialize empty form
            context['subscription_form'] = SubscriptionForm()
        else:
            # form already initialized by post() method
            context['subscription_form'] = self.form

        return context


class PartyPositionsView(ListView):
    model = Domanda
    template_name = 'vsq/partito_list.html'

    def get_context_data(self, **kwargs):
        context = super(PartyPositionsView,self).get_context_data(**kwargs)
        context['liste_elettorali'] = liste = Partito.objects.all().select_related('coalizione')
        coordinate = []
        for l in liste:
            coord = [l.sigla, l.coord_x, l.coord_y]
            coordinate.append(coord)
        context['coordinate'] = json.dumps(coordinate)

        return context

class TopicDetailView(DetailView):
    model = Domanda

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView,self).get_context_data(**kwargs)

        numeri_risposte = list(RispostaUtente.objects.filter(domanda=self.object).values('risposta_int').\
            annotate(nr=Count('risposta_int')))

        mfv = fav = tfv = tcn = con = mcn = 0
        for r in numeri_risposte:
            if r['risposta_int'] == 3:
                mfv = r['nr']
            if r['risposta_int'] == 2:
                fav = r['nr']
            if r['risposta_int'] == 1:
                tfv = r['nr']
            if r['risposta_int'] == -1:
                tcn = r['nr']
            if r['risposta_int'] == -2:
                con = r['nr']
            if r['risposta_int'] == -3:
                mcn = r['nr']

        context['mfv'] = mfv
        context['fav'] = fav
        context['tfv'] = tfv
        context['tcn'] = tcn
        context['con'] = con
        context['mcn'] = mcn
        context['tot'] = mfv + fav + tfv + tcn + con + mcn

        return context

class TopicListView(ListView):
    model = Domanda

class FaqListView(ListView):
    model = Faq

class PartitoDetailView(DetailView):
    model = Partito

    def get_context_data(self, **kwargs):
        context = super(PartitoDetailView,self).get_context_data(**kwargs)
        context['nome_partito'] = self.object.denominazione
        context['partito'] = self.object.sigla
        context['domande'] = Domanda.objects.all()
        context['partiti'] = partiti = Partito.objects.all().select_related('coalizione')
        context['risposte_partito'] = RispostaPartito.objects.filter(partito__sigla=self.object.sigla). \
            order_by('domanda'). \
            values('domanda', 'risposta_int', 'risposta_txt')
        context['risposte_partiti'] = RispostaPartito.objects.all().exclude(partito__sigla=self.object.sigla).\
            order_by('partito', 'domanda'). \
            values('partito__party_key', 'partito__sigla','domanda', 'risposta_int', 'risposta_txt')

        coordinate = []
        for p in partiti:
            coord = [p.sigla, p.coord_x, p.coord_y]
            coordinate.append(coord)
        context['coordinate'] = json.dumps(coordinate)

        return context


class QuestionarioUtenteView(TemplateView):

    template_name = 'vsq/questionario.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionarioUtenteView,self).get_context_data(**kwargs)

        context['domande'] = Domanda.objects.all()
        context['partiti'] = partiti = Partito.objects.all().select_related('coalizione')
        context['risposte_partiti'] = RispostaPartito.objects.all().order_by('partito', 'domanda'). \
            values('partito__party_key', 'partito__sigla','domanda', 'risposta_int')

        return context


class RisultatoUtenteView(TemplateView):

    template_name = 'vsq/risultato_utente.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        is_embedded = request.GET.get('embed', False)
        if is_embedded:
            self.template_name = 'vsq/risultato_embedded.html'
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(RisultatoUtenteView,self).get_context_data(**kwargs)

        try:
            context['utente'] = utente = Utente.objects.get(user_key=kwargs['user_key'])
        except Utente.DoesNotExist:
            self.template_name = 'vsq/risultato_waiting.html'
            return context

        context['domande'] = Domanda.objects.all()
        context['partiti'] = Partito.objects.all().select_related('coalizione')
        context['risposte_partiti'] = RispostaPartito.objects.all().order_by('partito', 'domanda').\
            values('partito__party_key', 'partito__sigla','domanda', 'risposta_int')

        context['risposte_utente'] = utente.rispostautente_set.all()
        context['coord_utente'] = utente.coord

        return context


class Test500View(View):

    def get(self, **kwargs):
        a = 3/0


