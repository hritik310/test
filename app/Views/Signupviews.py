from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from app.models import *
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from app.forms.user import *
from django.db.models import F
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY # new


def index(request):   
    context = {'user_list':user.objects.all()}
    return render(request,"index.html",context) 


def create(request):
    if request.method == 'POST':
        accountform = AddCreateForm(request.POST)
        if accountform.is_valid():
            new_user = accountform.save()
            users = user.objects.get(id=new_user.id)
            strip_customer = stripe.Customer.create(
                description= users.username,
                email=users.email
            )
            new_user.set_password(
                accountform.cleaned_data.get('password')         
            )

            if accountform.save():
                messages.success(request,'Account Added Successfully.')
                return redirect('login')
        else:
            return render(request,"signup/index.html",{'form':accountform})

    form = AddCreateForm()
    return render(request,"signup/index.html",{'form':form})

# def make(request,id):
#     users = user.objects.get(id=id)
#     strip_customer = stripe.Customer.create(
#         description= users.name,
#         email=users.email
#     )
#     print("see",strip_customer.description)
#     print("email",strip_customer.email)







# Create the PaymentIntent
        # intent = stripe.PaymentIntent.create(
        # payment_method = "pm_card_visa",
        # amount = 1099,
        # currency = 'usd',
        # confirmation_method = 'manual',
        # confirm = True,
        # )
        # print("secret",intent.client_secret)
            # intent = stripe.PaymentIntent.confirm([intent.id])
        # except stripe.error.CardError as e:
        #     # Display error on client
        #     return json.dumps({'error': e.user_message}), 200

        # return generate_response(intent)
    return render(request, 'payment/charge.html')

        # )
    #     return render(request, 'payment/charge.html')
    # return render(request, 'payment/charge.html')



    #To create a PaymentIntent for confirmation, see our guide at: https://stripe.com/docs/payments/payment-intents/creating-payment-intents#creating-for-automatic
        # stripe.PaymentIntent.confirm(
        # format,
        # payment_method="pm_card_visa",
        # )
        
        # stripe.PaymentMethod.create(
        # type="card",
        # card={
        #     "number": "4242424242424242",
        #     "exp_month": 2,
        #     "exp_year": 2023,
        #     "cvc": "314",
        #     },
        # )
        # charge = stripe.Charge.create(
        #     amount=500,
        #     currency='inr',
        #     description='charge',
        #     source=request.POST['stripeToken']