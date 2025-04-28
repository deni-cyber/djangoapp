from payments.models import Payment, PaymentCallbackLog
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from payments.models import Payment, PaymentCallbackLog

from payments.models import Payment, PaymentCallbackLog

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        print(request.body)
        data = json.loads(request.body)

        # Save the full callback for future reference
        PaymentCallbackLog.objects.create(raw_data=data)

        result_code = data['Body']['stkCallback']['ResultCode']
        metadata = data['Body']['stkCallback'].get('CallbackMetadata', {})

        if result_code == 0:
            phone_number = None
            amount = None
            mpesa_receipt_number = None

            for item in metadata.get('Item', []):
                if item['Name'] == 'PhoneNumber':
                    phone_number = item['Value']
                if item['Name'] == 'Amount':
                    amount = item['Value']
                if item['Name'] == 'MpesaReceiptNumber':
                    mpesa_receipt_number = item['Value']

            payment = Payment.objects.filter(phone_number=phone_number, status='Pending').first()

            if payment:
                payment.status = 'Paid'
                payment.transaction_id = mpesa_receipt_number
                payment.save()
        else:
            pass

        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
