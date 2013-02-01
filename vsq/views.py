from django.core.mail import EmailMessage
from django.core.serializers import serialize
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils.functional import curry
from django.views.generic import TemplateView, DetailView, CreateView, ListView
from vsq.models import Partito, RispostaPartito, Domanda, EarlyBird, Utente
from django.shortcuts import redirect, render_to_response, get_object_or_404
from vsq.forms import QuestionarioPartitiForm, EarlyBirdForm
from datetime import datetime
from settings_local import PROJECT_ROOT, MANAGERS
from settings import MIN_GRAPH_X, MIN_GRAPH_Y, MAX_GRAPH_X, MAX_GRAPH_Y
import random
import json
from json.encoder import JSONEncoder

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
                c,t = form.get_answer(d.pk)
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
        return context

class PartyPositionsView(ListView):
    model = Domanda
    template_name = 'vsq/domanda_partiti_list.html'

    def get_context_data(self, **kwargs):
        context = super(PartyPositionsView,self).get_context_data(**kwargs)
        context['liste_elettorali'] = Partito.objects.all().select_related('coalizione')
        return context

class TopicDetailView(DetailView):
    model = Domanda

class TopicListView(ListView):
    model = Domanda

class PartitoDetailView(DetailView):
    model = Partito