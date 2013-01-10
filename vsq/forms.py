from django import forms
from vsq.models import RispostaPartito

class QuestionarioPartitiForm(forms.Form):
    contact_name = forms.CharField(max_length=60, label="Responsabile per la lista")

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(QuestionarioPartitiForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(extra):
            self.fields['answer_c[%s]' % i] = forms.ChoiceField(choices=RispostaPartito.TIPO_RISPOSTA, label=extra[i])
            self.fields['answer_t[%s]' % i] = forms.CharField(widget=forms.Textarea())

    def answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('answer_c['):
                yield (self.fields[name].label, value)


