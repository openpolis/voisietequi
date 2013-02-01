from django import template

register = template.Library()

@register.simple_tag
def label_risposta(obj):
    return {
        -3: 'mc',
        -2: 'c',
        -1: 'tc',
        1: 'tf',
        2: 'f',
        3: 'mf'
    }[obj.risposta_int]


@register.simple_tag(takes_context=True)
def immagine_partito(context, partito, size=False):
    return """<a href="{party_url}"><img
        class="img-circle-coalition img-coalition-{coalizione} img-circle-loghi{size}"
        src="{image_url}" alt="{sigla}" /></a>""".format(
        party_url=partito.get_absolute_url(),
        coalizione= partito.coalizione.slug,
        image_url= context['MEDIA_URL'] + partito.simbolo.url,
        sigla= partito.sigla,
        size= ' img-circle-{0}'.format(size) if size else ''
    )

@register.simple_tag(takes_context=True)
def immagini_partiti_per_posizione(context, domanda, risposta, size=False):
    images = []
    for partito in domanda.get_partiti_by_risposta(risposta):
        images.append(
            immagine_partito(context, partito, size)
        )
    return "".join(images)