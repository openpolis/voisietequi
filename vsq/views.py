from django.views.generic import TemplateView, DetailView
from vsq.models import Partito, RispostaPartito, Domanda

class QuestionarioPartitiView(TemplateView):

    context = {}
    template_name = "partiti.html"

    def get_context_data(self, **kwargs ):
        context = super(QuestionarioPartitiView, self).get_context_data(**kwargs)
        key = kwargs['party_key']

        try:
            p = Partito.objects.get(party_key=key)
            context['partito']=p
        except Partito.DoesNotExist:
#            TODO: redirect to home page
            pass

#        carica le domande, le possibili risposte e genera il form


        return context