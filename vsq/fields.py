from django.utils.functional import curry
import re

from django.db.models import CharField
from django.forms.fields import RegexField

from widgets import ColorFieldWidget

RGB_REGEX = re.compile('^#?((?:[0-F]{3}){1,2})$', re.IGNORECASE)
HEX = '0123456789abcdef'
HEX2 = dict((a+b, HEX.index(a)*16 + HEX.index(b)) for a in HEX for b in HEX)

class RGBColorField(CharField):

    widget = ColorFieldWidget

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super(RGBColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.update({
            'form_class': RegexField,
            'widget': self.widget,
            'regex': RGB_REGEX
        })
        return super(RGBColorField, self).formfield(**kwargs)

    def contribute_to_class(self, cls, name):

        super(RGBColorField,self).contribute_to_class(cls, name)
        def _convert_hex_to_rgb_triplet(instance):
            triplet = getattr(instance, name, None)
            if triplet is None: return 0,0,0
            triplet = triplet.lower().strip('#')
            return HEX2[triplet[0:2]], HEX2[triplet[2:4]], HEX2[triplet[4:6]]
        setattr(cls, 'get_%s_rgb' % self.name, _convert_hex_to_rgb_triplet)




try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^vsq\.fields\.RGBColorField"])
except ImportError:
    pass