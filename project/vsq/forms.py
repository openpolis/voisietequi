from django import forms
from django.conf import settings

from vsq.models import RispostaPartito, EarlyBird
from vsq.templatetags.labels import prepend


class QuestionarioPartitiForm(forms.Form):

    my_default_errors = {
        'required': 'Campo richiesto',
        'invalid': 'Valore non valido'
    }

    contact_name = forms.CharField(max_length=60, label="Responsabile per %s" % prepend(u'La', u'Il', settings.PARTY_TERM), error_messages=my_default_errors)

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        party = kwargs.pop('party')
        super(QuestionarioPartitiForm, self).__init__(*args, **kwargs)
        empty_label='-- Scegli una risposta --'

        self.fields['contact_name'].initial = party.responsabile_nome

        for i, question in enumerate(extra):
            risposta = party.get_answer_for(question)
            self.fields['answer_c[%s]' % question.ordine] = forms.ChoiceField(
                tuple([(u'', empty_label)] + list(RispostaPartito.TIPO_RISPOSTA)),
                label=question.testo,
                error_messages = self.my_default_errors,
                required=False,
                initial=risposta.risposta_int if risposta else ''
            )
            self.fields['answer_t[%s]' % question.ordine] = forms.CharField(
                widget=forms.Textarea(), required=False,
                initial=risposta.risposta_txt if risposta else ''
            )

#    restituisce le risposte della domanda index
    def get_answer(self, index):
        i = str(index)
        c = self.cleaned_data['answer_c['+i+']']
        t = self.cleaned_data['answer_t['+i+']']
        return c,t


class EarlyBirdForm(forms.ModelForm):
    my_default_errors = {
        'required': 'Campo richiesto',
        'invalid': 'Attenzione: Indirizzo email non valido',

    }

    email = forms.EmailField(max_length=200, error_messages=my_default_errors)

    class Meta:
        model = EarlyBird
        fields = ['email', ]


class SubscriptionForm(forms.Form):

    my_default_errors = {
        'required': 'Campo richiesto',
        'invalid': 'Attenzione: Indirizzo email non valido',
    }
    email = forms.EmailField(max_length=200, error_messages=my_default_errors)