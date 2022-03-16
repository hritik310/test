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
from app.models import user
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from app.models import StripeCustomer 
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect

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
            print("plans",plans)
            dict = {'Premium':settings.BASIC_PRICE_ID,'daily':settings.MONTHLY_PRICE_ID}
            plan_price =settings.MONTHLY_PRICE_ID

            print("dict",dict)
            print("plan",plan_price)
            stripe.api_key = settings.SECTRET_KEY
            checkout_session=stripe.checkout.Session.create(
                success_url="http://3.86.247.236:8000/stripe-checkout/success/?success=true&session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://3.86.247.236:8000/stripe-checkout/cancel/?cancel=true",
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
            if request.user.is_authenticated:
              return redirect(checkout_session.url) 
            else:
               
              return redirect("/signup")
      
    
    

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
  template_name = 'signup/home.html'
  import stripe



import json
@csrf_exempt
def cancel_subscription(request):
  
  c= StripeCustomer.objects.values('stripeSubscriptionId')
  print(c)
  a= stripe.Subscription.list(limit=1)
  current=request.user.id
  if StripeCustomer.objects.filter(stripeCustomerId=request.user.id).exists():
  
    d= StripeCustomer.objects.filter(stripeCustomerId=current)
    show=d.values_list('stripeSubscriptionId',flat="true")
    print(show  )
    if StripeCustomer.objects.filter(stripeCustomerId=request.user.id).exists():
        owner_id=show[0]
    else:
      owner_id=0   
    # print(b)

    z=stripe.Subscription.delete(owner_id)
    print("z",z)

    a=StripeCustomer.objects.filter(stripeCustomerId=request.user.id).delete()
    # messages.success(request,"Your Subscription is cancel")

    return render (request,"payment/cancel.html")
  if user.objects.filter(id=request.user.id):
    return redirect("/")  


  return render (request,"signup/home.html")

   

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