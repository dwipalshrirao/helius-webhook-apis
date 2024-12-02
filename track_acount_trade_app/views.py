# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import SwapEvent
import hmac
import hashlib

class HeliusWebhookException(Exception):
    pass

@csrf_exempt
@require_http_methods(["POST"])
def helius_webhook(request):
    try:
        # # Verify Helius webhook signature if provided
        # if 'HTTP_X_HELIUS_SIGNATURE' in request.META:
        #     signature = request.META['HTTP_X_HELIUS_SIGNATURE']
        #     webhook_secret = 'your_webhook_secret'  # Store this securely in environment variables
            
        #     # Calculate expected signature
        #     payload = request.body
        #     expected_signature = hmac.new(
        #         webhook_secret.encode('utf-8'),
        #         payload,
        #         hashlib.sha256
        #     ).hexdigest()
            
        #     if not hmac.compare_digest(signature, expected_signature):
        #         raise HeliusWebhookException("Invalid webhook signature")

        # Parse the webhook payload
        data = json.loads(request.body)
        
        # Process each event in the webhook
        processed_events = []
        for event in data:
            if event.get('type') == 'SWAP':
                # Extract relevant swap information including account address
                swap_event = SwapEvent.objects.create(
                    transaction_id=event.get('signature'),
                    account_address=event.get('feePayer'),  # Added account address
                    timestamp=event.get('timestamp'),
                    sell_token_mint=event.get('tokenTransfers', [{}])[0].get('mint'),
                    sell_token_amount=event.get('tokenTransfers', [{}])[0].get('amount'),
                    buy_token_mint=event.get('tokenTransfers', [{}])[1].get('mint'),
                    buy_token_amount=event.get('tokenTransfers', [{}])[1].get('amount'),
                    type=event.get('type'),
                    raw_data=event
                )
                processed_events.append(swap_event.transaction_id)

            elif event.get('type') == 'UNKNOWN':
                # Extract relevant swap information including account address
                swap_event = SwapEvent.objects.create(
                    transaction_id=event.get('signature'),
                    account_address=event.get('feePayer'),  # Added account address
                    timestamp=event.get('timestamp'),
                    sell_token_mint=event.get('tokenTransfers', [{}])[0].get('mint'),
                    sell_token_amount=event.get('tokenTransfers', [{}])[0].get('amount'),
                    buy_token_mint=event.get('tokenTransfers', [{}])[1].get('mint'),
                    buy_token_amount=event.get('tokenTransfers', [{}])[1].get('amount'),
                    raw_data=event,
                    type=event.get('type'),
                )
                processed_events.append(swap_event.transaction_id)
            else:
                # Handle other event types
                print("other events", event)
                print("================================\n"*4)

        return JsonResponse({
            'status': 'success',
            'message': 'Swap events processed successfully',
            'processed_events': processed_events
        }, status=200)

    except HeliusWebhookException as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=401)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON payload'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


