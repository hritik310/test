from django.urls import path
from django.urls import path
from app.Views import Loginviews
from app.Views import Signupviews
from app.Views import Paymentview
from app.Views import  Paymentview
from app.Views import Newprediction
from app.Views import NFLview
from app.Views import TwitterView
from app.Views import ContactView



 

from . import views

urlpatterns = [
    path('', Signupviews.index, name='index'),
    path('signup/', Signupviews.create, name='signup'),
    path('login', Loginviews.user_login, name='login'),
    path('logout',Loginviews.userLogout,name='logout'),
    path('sport',Loginviews.setting,name = 'sport'),
    path('update/<int:id>',Loginviews.update, name ='update'),


 # build model urls
    path('buildmodel/<int:id>', Signupviews.buildmodel, name ='buildmodel'),
    path('buildmodel1/', Signupviews.heatmap, name ='buildmodel1'),
    path('buildmodel3/', Signupviews.selectvariable, name='buildmodel3'),
    path('buildmodel5/', Signupviews.modelname, name='buildmodel5'),
    path('download',Signupviews.download_file,name='download'),
    path('download/corr',Signupviews.download_corr_file,name='download/corr'),
    path('prediction', Newprediction.newprediction, name = 'prediction'),
    path('simulation', Newprediction.simulation, name = 'simulation'),



    path('buildmodel/status/',Signupviews.buildmodelStatus, name ="buildmodel-status"),
    path('buildmodel/update/',Signupviews.buildmodelUpdate, name ="buildmodel-update"),
    path('buildmodel/remove/',Signupviews.buildmodelremove, name ="buildmodel-remove"),
    path('buildmodelbutton',Signupviews.buildmodelbutton, name ="buildmodel-button"),
    path('register',Signupviews.create,name="register"),
    path('passwordchange/<int:id>',Loginviews.passwordchange, name ='passwordchange'),
    path('updatemodel/<int:id>',Signupviews.update,name="updatemodel"),
    path('delete/<int:id>',Signupviews.deletemodel,name="delete"),
   
    path('download/var',Signupviews.download_var,name='download/var'),


    path('reset/<int:id>',Signupviews.reset,name='reset'),




    
#payment urls
    path('stripe-checkout/', Paymentview.StripeCheckoutAPIView.as_view(), name = 'stripe_checkout'),
    path('stripe-checkout/success/',Paymentview.SuccessPayment.as_view(), name="success"),
    path('stripe-checkout/cancel/',Paymentview.cancel_subscription, name="cancel"),
    path('activate/<uidb64>/<token>/',Signupviews.activate, name='activate'),

    path('account',Signupviews.account,name="account"),
    path('membership',Signupviews.membership,name="membership"),
    path("mymodel",Signupviews.mymodel,name="mymodel"),


    path("minmax",Signupviews.minmax,name="minmax"),


    # NFL View
    path('NFL', NFLview.nfl, name = 'NFL'),
    
    # TwitterView urls
    path('tweets', TwitterView.tweetshow, name = 'tweets'),


    # ContactView urls
    path('contactinfo', ContactView.contact, name='contactinfo'),



]





