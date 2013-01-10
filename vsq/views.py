from django.views.generic import TemplateView, DetailView
from vsq.models import Partito, RispostaPartito, Domanda
from django.shortcuts import redirect, render_to_response
from vsq.forms import QuestionarioPartitiForm


class QuestionarioPartitiClosed(TemplateView):
    template_name = "partiti_fine.html"

    def get_context_data(self, **kwargs):
        context = super(QuestionarioPartitiClosed, self).get_context_data(**kwargs)
        return context


class QuestionarioPartitiView(TemplateView):

    context = {}
    template_name = "partiti.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        questions = Domanda.get_domande()
        n_questions=questions.count()
        form= QuestionarioPartitiForm(self.request.POST , extra=questions)

        party_key = kwargs['party_key']
        p = Partito.objects.get(party_key=party_key)


        if form.is_valid():
            #        do_something_with(form.cleaned_data)
            #        controlla e salva le risposte
#            for (question, answer) in form.answers():
            #            save_answer(request, question, answer)

            return redirect("questionario_partiti_fine",slug=p.slug)

        #                stampa la form con gli eventuali errori

        context['form']=form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs ):

        context = super(QuestionarioPartitiView, self).get_context_data(**kwargs)
        questions = Domanda.get_domande()
        n_questions=questions.count()
        form= QuestionarioPartitiForm( extra=questions)

        party_key = kwargs['party_key']
        p = Partito.objects.get(party_key=party_key)

        if p:
            context['nome_lista']=p.denominazione

            if RispostaPartito.objects.filter(partito=p).count() >0 :
                return redirect("partiti_fine.html")
            else:

                context['n_questions']=n_questions
                context['form']=form
                context['possible_answers']=RispostaPartito.get_tipo_risposta()

                return context
        else:

            #                return redirect("404")
            return context
