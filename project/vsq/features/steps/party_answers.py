#!/usr/bin/env python
# -*- coding: utf8 -*-

from behave import *

@given('the questions exist in the DB')
def step(context):
    from vsq.models import Domanda
    (d1, create) = Domanda.objects.get_or_create(
        slug='domanda-di-test-1',
        testo="Domanda di test 1",
        testo_html="<p>Domanda di test 1</p>"
    )

    (d2, create) = Domanda.objects.get_or_create(
        slug='domanda-di-test-2',
        testo="Domanda di test 2",
        testo_html="<p>Domanda di test 2</p>"
    )

    (d3, create) = Domanda.objects.get_or_create(
        slug='domanda-di-test-3',
        testo="Domanda di test 3",
        testo_html="<p>Domanda di test 3</p>"
    )
    context.questions = (d1, d2, d3)

@given('the party exists in the DB')
def step(context):
    from vsq.models import Partito
    (p, create) = Partito.objects.get_or_create(
        denominazione="Feudalesimo e libertà",
        party_key="inhocsignovinces",
        sigla="FeL"
    )
    context.party = p



@given('I have not answered the questions, yet')
def step(context):
    from vsq.models import RispostaPartito
    RispostaPartito.objects.filter(partito=context.party).delete()
    assert RispostaPartito.objects.filter(partito=context.party).count() == 0



@given('I have already answered the questions')
def step(context):
    from vsq.models import RispostaPartito

    r1 = RispostaPartito(
        partito=context.party,
        domanda=context.questions[0],
        risposta_int=RispostaPartito.TIPO_RISPOSTA.moltocontrario,
        risposta_txt="Un commento alla risposta numero 1"
    )
    r1.save()
    r2 = RispostaPartito(
            partito=context.party,
            domanda=context.questions[1],
            risposta_int=RispostaPartito.TIPO_RISPOSTA.contrario,
            risposta_txt="Un commento alla risposta numero 2"
    )
    r2.save()
    r3 = RispostaPartito(
            partito=context.party,
            domanda=context.questions[2],
            risposta_int=RispostaPartito.TIPO_RISPOSTA.moltofavorevole,
            risposta_txt="Un commento alla risposta numero 3"
    )
    r3.save()
    assert RispostaPartito.objects.filter(partito=context.party).count() == 3



@when('I visit the private URL, with my party-key')
def step(context):
    br = context.browser
    br.open(context.browser_url('/risposte-partito/{0}'.format(context.party.party_key)))
    br.select_form(nr=0)

@when('I fill in the empty answers fields')
def step(context):
    assert False

@when('I press the submit button')
def step(context):
    assert False

@then('the answers are stored into the system')
def step(context):
    assert False

@then('the page shows the form with the read-only answers')
def step(context):
    assert False