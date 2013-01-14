from django import forms
from vsq.models import RispostaPartito, EarlyBird


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
            self.fields['answer_c[%s]' % question.pk] = forms.ChoiceField(
                tuple([(u'', empty_label)] + list(RispostaPartito.TIPO_RISPOSTA)),
                label=question.testo,
                error_messages = self.my_default_errors,
            )
            self.fields['answer_t[%s]' % question.pk] = forms.CharField(
                widget=forms.Textarea(), required=False
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
        'invalid': 'Valore non valido'
    }

    email = forms.EmailField(max_length=200, error_messages=my_default_errors)

    class Meta:
        model = EarlyBird

