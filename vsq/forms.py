from django import forms

class QuestionarioPartitiForm(forms.Form):
    contact_name = forms.CharField(max_length=60)

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(QuestionarioPartitiForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(extra):
            self.fields['custom_%s' % i] = forms.CharField(label=question)

    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)


