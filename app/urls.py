from django.urls import path
from django.urls import path
from app.Views import Loginviews
from app.Views import Signupviews
from app.Views import Paymentview


from . import views

urlpatterns = [
    path('', Signupviews.create, name='index'),
    path('login', Loginviews.user_login, name='login'),
    path('charge', Paymentview.charge, name='charge'), # new
    path('home', Paymentview.HomePageView.as_view(), name='home'),
]


