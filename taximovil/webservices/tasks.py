from __future__ import absolute_import, unicode_literals

import math

import conekta
from celery import shared_task
from django.core.mail import EmailMessage

from config.models import Servicio
from taximovil.settings import CONEKTA_PRIVATE_KEY, CONEKTA_LOCALE, CONEKTA_VERSION


@shared_task
def sendMail(to, subject, message):
    subject = subject + " [do not reply]"
    msg = EmailMessage(subject, message, to=to)
    msg.content_subtype = 'html'
    msg.send()


@shared_task
def cobra_servicio(servicio):
    s = Servicio.objects.get(pk=servicio)
    if s.estatus_pago is not None:
        if servicio.estatus_pago == 1:
            return
    conekta.api_key = CONEKTA_PRIVATE_KEY
    conekta.locale = CONEKTA_LOCALE
    conekta.api_version = CONEKTA_VERSION
    try:
        order = conekta.Order.create({
            "line_items": [
                {
                    "name": "Viaje taximovil #" + str(servicio),
                    "description": "Servicio de taxi",
                    "unit_price": math.ceil(s.costo * 100),
                    "quantity": 1
                }
            ],
            "customer_info": {
                "customer_id": s.cliente.customer_id
            },
            "charges": [{
                "payment_method": {
                    "type": "card",
                    "payment_source_id": s.tarjeta.token
                },
                "amount": math.ceil(s.costo * 100)
            }],
            "currency": "MXN",
        })
        if order.payment_status == 'paid':
            s.estatus_pago = 1
            s.save()
    except conekta.ProcessingError as error:
        e = error.error_json['details']
        e = e[0]
        print(e['message'])
