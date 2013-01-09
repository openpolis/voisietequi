from django.views.generic import TemplateView, DetailView
from vsq.models import Partito, RispostaPartito, Domanda
from django.shortcuts import redirect, render_to_response
from vsq.forms import QuestionarioPartitiForm


def questionario_partiti(request):
#    extra_questions = get_questions(request)
    form = QuestionarioPartitiForm(request.POST or None, extra=extra_questions)

    if form.is_valid():
#        do_something_with(form.cleaned_data)
#        controlla e salva le risposte
        for (question, answer) in form.extra_answers():
#            save_answer(request, question, answer)
            pass
        return redirect("questionario_partiti_success")

    return render_to_response("signup/form.html", {'form': form})


class QuestionarioPartitiView(TemplateView):

    context = {}
    template_name = "partiti.html"

    def get_context_data(self, **kwargs ):
        context = super(QuestionarioPartitiView, self).get_context_data(**kwargs)
        key = kwargs['party_key']

        try:
            p = Partito.objects.get(party_key=key)
            context['nome_lista']=p.denominazione
        except Partito.DoesNotExist:
#            TODO: redirect to "closed" page
            pass

#        carica le domande, le possibili risposte e genera il form
        context['possible_answers']=RispostaPartito.TIPO_RISPOSTA
        context['questions']=Domanda.objects.all()


        return context