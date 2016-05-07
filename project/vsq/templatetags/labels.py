from django import template
from django.utils.html import format_html, escape

from vsq.models import RispostaPartito

register = template.Library()

@register.simple_tag
def label_risposta(risposta_int):
    return {
        -3: 'mc',
        -2: 'c',
        -1: 'tc',
        1: 'tf',
        2: 'f',
        3: 'mf'
    }[risposta_int]

@register.simple_tag
def label_risposta_text(risposta_int):
    return {
        -3: 'Molto contrario/a',
        -2: 'Contrario/a',
        -1: 'Tendenzialmente contrario/a',
        1: 'Tendenzialmente favorevole',
        2: 'Favorevole',
        3: 'Molto favorevole'
    }[risposta_int]

#@register.filter
#def lista_altre_risposte(risposta_int):
#    return {
#        -3: [-2,-1, 1, 2, 3],
#        -2: [-3,-1, 1, 2, 3],
#        -1: [-2,-3, 1, 2, 3],
#         1: [ 2, 3,-1,-2,-3],
#         2: [ 3, 1,-1,-2,-3],
#         3: [ 2, 1,-1,-2,-3],
#    }[risposta_int]


@register.simple_tag()
def immagine_partito(partito, size=False, title=None):
    return format_html(u"""<a href="{party_url}"><img
        class="img-circle-coalition img-coalition-{coalizione} img-circle-loghi{size}"
        src="{image_url}" alt="{sigla}" title="{title}" /></a>""",
        party_url=partito.get_absolute_url(),
        coalizione=partito.coalizione.slug,
        image_url=partito.simbolo_url,
        sigla=partito.sigla,
        size=u' img-circle-{0}'.format(size) if size else '',
        title=escape(title if title else partito.denominazione)
    )

@register.simple_tag(takes_context=True)
def immagini_partiti_per_posizione(context, domanda, risposta, size=False):
    images = []
    for partito in domanda.get_partiti_by_risposta(risposta):
        images.append(
            immagine_partito( partito, size)
        )
    return format_html("".join(images))