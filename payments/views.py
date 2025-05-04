from payments.models import Payment, PaymentCallbackLog
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('callback received', data)

            # Log raw callback data
            PaymentCallbackLog.objects.create(raw_data=data)

            callback = data.get('Body', {}).get('stkCallback', {})
            result_code = callback.get('ResultCode')
            result_desc = callback.get('ResultDesc')
            merchant_request_id = callback.get('MerchantRequestID')
            checkout_request_id = callback.get('CheckoutRequestID')

            # Attempt to find the related payment
            checkout_request_id = data['Body']['stkCallback'].get('CheckoutRequestID')
            payment = Payment.objects.filter(checkout_request_id=checkout_request_id, status='Pending').first()
            
            
            if not payment:
                print(f"No payment found for CheckoutRequestID: {checkout_request_id}")
                return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})

            payment.result_desc = result_desc
            payment.merchant_request_id = merchant_request_id
            payment.checkout_request_id = checkout_request_id

            if result_code == 0:
                # Success case
                metadata = callback.get('CallbackMetadata', {}).get('Item', [])
                for item in metadata:
                    name = item.get('Name')
                    value = item.get('Value')

                    if name == 'MpesaReceiptNumber':
                        payment.receipt_number = value
                    elif name == 'PhoneNumber':
                        payment.phone_number = value
                    elif name == 'Amount':
                        payment.amount = value
                    elif name == 'TransactionDate':
                        payment.transaction_date = str(value)

                payment.status = 'Success'
                payment.save()
            else:
                # Failed or cancelled transaction
                payment.status = 'Failed'
                payment.save()

        except Exception as e:
            print("Error processing payment callback:", str(e))

        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
