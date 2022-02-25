from multiprocessing import context
from django.http.response import JsonResponse, HttpResponse 
from django.contrib.auth.models import User  # new
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from app.models import StripeCustomer 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from app.models import StripeCustomer 


class StripeCheckoutAPIView(TemplateView):
  template_name = "payment/checkout.html"
  def get_context_data(self, **kwargs):
    context={
      'stripe_public_key' : settings.PUBLISH_KEY
    }
    return context

  def post(self, request, *args, **kwargs):
        context={}
        # print("iddddd",request.user.subscription.id)
        if request.method=="POST":
            plans = request.POST.get("plan")
            dict = {'Premium':settings.BASIC_PRICE_ID,'daily':settings.MONTHLY_PRICE_ID}
            plan_price = dict[plans]

            print("dict",dict)
            print("plan",plan_price)
            stripe.api_key = settings.SECTRET_KEY
            checkout_session=stripe.checkout.Session.create(
                success_url="http://3.92.217.18:8000/stripe-checkout/success/?success=true&session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://3.92.217.18:8000/stripe-checkout/cancel/?cancel=true",
                payment_method_types=["card"],
                client_reference_id = self.request.user.id,
                #metadata = {'user_id':45, 'email':"customer@gmail.com"},
                line_items=[
                    {
                        "quantity": 1,
                        "price": plan_price 
                    },
                ],
                mode="subscription",     
            ) 
            print("checkout",checkout_session)
            iddd=checkout_session.id
            print("detail",iddd)

            # a=StripeCustomer() 
            # a.stripeCustomerId=self.request.user.id
            # a.stripeSubscriptionId=iddd
            # a.save()
            return redirect(checkout_session.url)  
        
      
    
    

class SuccessPayment(TemplateView):
  template_name = 'payment/success.html'
  def get_context_data(self, **kwargs,):
    a=stripe.Subscription.list(limit=1)
    b= a.data[0].id
    q=StripeCustomer() 
    q.stripeCustomerId=self.request.user.id
    q.stripeSubscriptionId=b
    q.membershipstatus = 1
    q.save()

    context = {}
    print("context",context)
    return context


class CancelPayment(TemplateView):
  template_name = 'payment/cancel.html'
  import stripe



import json
@csrf_exempt
def cancel_subscription(request):
  c= StripeCustomer.objects.values('stripeSubscriptionId')
  print(c)
  a= stripe.Subscription.list(limit=1)
  current=request.user.id
  b= a.data[0].id
  # b= StripeCustomer.objects.filter(stripeCustomerId=current).get("stripeSubscriptionId")
  # print(b)
  z=stripe.Subscription.delete(b)
  return redirect("Your subscription is cancel",)
   

# @csrf_exempt
# def stripe_webhook(request):
#   payload = request.body.decode('utf-8')  
#   sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#   event = None

#   try:
#     event = stripe.Webhook.construct_event(
#     payload, sig_header, settings.STRIPE_SIGNING_SECRET
#     )
#   except ValueError as e:
#     # Invalid payload
#     return HttpResponse(status=400)
#   except stripe.error.SignatureVerificationError as e:
#     # Invalid signature
#     return HttpResponse(status=400)

#   # Do something with event

#   return HttpResponse(status=200)