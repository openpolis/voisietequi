from django.http import Http404
from django.views.generic import TemplateView, DetailView
from vsq.models import Partito, RispostaPartito, Domanda
from django.shortcuts import redirect, render_to_response, get_object_or_404
from vsq.forms import QuestionarioPartitiForm
from datetime import datetime




class QuestionarioPartitiView(TemplateView):

    context = {}
    template_name = "partiti.html"

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
#            TODO: inviare mail a Vincenzo dopo il salvataggio con il link per vedere la pagina risposte
            return redirect("questionario_partiti_fine",slug=p.slug)

#       stampa la form con gli eventuali errori
        context['form']=form
        return self.render_to_response(context)


    def get_context_data(self, **kwargs ):

        context = super(QuestionarioPartitiView, self).get_context_data(**kwargs)
        questions = Domanda.get_domande()
        n_questions=questions.count()
        form= QuestionarioPartitiForm( extra=questions)

        party_key = kwargs['party_key']
        p = get_object_or_404(Partito, party_key=party_key)

        context['nome_lista']=p.denominazione

        context['n_questions']=n_questions
        context['form']=form
        context['possible_answers']=RispostaPartito.get_tipo_risposta()

        return context


#se la chiave del questionario e' gia' stata utilizzata e il questionario e' stato salvato correttamente
#fa un redirect verso la pagina finale di quella lista
    def get(self, request, *args, **kwargs):
        party_key = kwargs['party_key']
        p = get_object_or_404(Partito, party_key=party_key)
        if RispostaPartito.objects.filter(partito=p).count()>0 :
            return redirect("questionario_partiti_fine",slug=p.slug)


class QuestionarioPartitiClosed(TemplateView):
    template_name = "partiti_fine.html"

    def get_context_data(self, **kwargs):
        context = super(QuestionarioPartitiClosed, self).get_context_data(**kwargs)
        p = get_object_or_404(Partito, slug=kwargs['slug'])


        context['nome_lista']=p.denominazione
        context['nome_responsabile']=p.responsabile_nome

        return context
