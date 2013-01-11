from django import forms
from vsq.models import RispostaPartito


class QuestionarioPartitiForm(forms.Form):

    my_default_errors = {
        'required': 'Campo richiesto',
        'invalid': 'Valore non valido'
    }

    contact_name = forms.CharField(max_length=60, label="Responsabile per la lista", error_messages=my_default_errors)

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(QuestionarioPartitiForm, self).__init__(*args, **kwargs)
        empty_label='-- Scegli una risposta --'

        for i, question in enumerate(extra):
            self.fields['answer_c[%s]' % question.ordine] = forms.ChoiceField(
#                choices=RispostaPartito.TIPO_RISPOSTA,
                tuple([(u'', empty_label)] + list(RispostaPartito.TIPO_RISPOSTA)),
                label=question.testo,
                error_messages = self.my_default_errors,
            )
            self.fields['answer_t[%s]' % question.ordine] = forms.CharField(
                widget=forms.Textarea(), required=False
            )

#    restituisce le risposte della select box
    def answers_c(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('answer_c['):
                yield (self.fields[name].label, value)

#    restituisce le risposte testuali
    def answers_t(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('answer_t['):
                yield (self.fields[name].label, value)


