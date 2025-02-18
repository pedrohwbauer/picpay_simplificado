from ninja import Router
from .schemas import TransactionSchema
from .models import Transactions
from django.shortcuts import get_object_or_404
from users.models import User
from rolepermissions.checkers import has_permission
from django.db import transaction as django_transaction
import requests
from django_q.tasks import async_task
from .tasks import send_notification

from django.conf import settings

payments_router = Router()

@payments_router.post('/', response={200: dict, 400: dict})
def transaction(request, transaction: TransactionSchema):
    payer = get_object_or_404(User, id=transaction.payer)
    payee = get_object_or_404(User, id=transaction.payee)
    
    if payer.amount < transaction.amount:
        return 400, {'error': 'Saldo inusficiente'}
    
    if not has_permission(payer, 'make_transfer'):
        return 403, {'errors': 'Você não tem permissão para realizar transferencia'}
    
    if not has_permission(payee, 'receive_transfer'):
        return 403, {'errors': 'O usuário não pode receber transferências'}
    
    with django_transaction.atomic():
        payer.pay(transaction.amount)
        payee.receive(transaction.amount)
        
        transct = Transactions(
            amount = transaction.amount,
            payer_id = transaction.payer,
            payee_id = transaction.payee,
        )
        
        payer.save()
        payee.save()
        transct.save()

        response = requests.get(settings.AUTHORIZE_TRANSFER_ENDPOINT).json()
        if response.get('status') != 'authorized':
            raise Exception()
        
    async_task(send_notification, payer.first_name, payee.first_name, transaction.amount)
    return 200, {'transaction_id': 1}