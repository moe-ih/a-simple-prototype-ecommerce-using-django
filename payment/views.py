from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import stripe
from django.http.response import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


from basket import basket
from order.views import payment_confirmation


@login_required
def main(request):
    basket_session = basket.Basket(request)
    total = str(basket_session.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    if basket_session.current_basket_session:
        stripe.api_key = "sk_test_51ITS4wLj3bOPswXRIdrgWqrXTmykXjDcW1g8QIW8xtV3zi9hNolGzrlkCMMbLJtkOCAP8YMboyCpouIH1QbMpYRK00N7MyT0w3"
    
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='usd',
            metadata={'userid': request.user.id}
        )

        return render(request, 'payment/main.htm', {'client_secret': intent.client_secret})
    else:
        return redirect('/')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    print("HHHHHHHHHHHHHH")
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


def order_success(request):
    basket_session = basket.Basket(request)
    basket_session.clear()
    return render(request ,"payment/thanks.htm")
