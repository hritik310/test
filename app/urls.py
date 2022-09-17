from django.urls import path, re_path
from app.views import ProviderView
from app.views import UserView
from app.views import CustomerView
from app.views import AgencyView
from app.views import ShipperView
from app.views import InsuranceView
from app.views import TemporaryPermitView
from app.views import ReleasedView
from app.views import PedimentorView
from app.views import InventoryView
from app.views import AccountView
from app.views import CompanyView

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    # re_path(r'^.*\.html', views.gentella_html, name='gentella'),

    # # The home page
    path('', UserView.userLogin, name='login'),
    path('html', UserView.index, name='html'),
    path('home', UserView.home, name='home'),
    path('login',UserView.userLogin,name='login'),
    path('logout',UserView.userLogout,name='logout'),

    path('account',AccountView.account,name='account'),
    path('account/create',AccountView.create,name='accountcreate'),
    path('account/update/<int:id>',AccountView.update,name='accountupdate'),
    path('account/delete/<int:id>',AccountView.delete, name ="accountdelete"),
    # path('account/updateaccount/<int:id>',AccountView.updateaccount,name='permission_account'),
    # path('account/permission/<int:id>',AccountView.permission, name ="permission"),



    # # customer urls
    path('customer',CustomerView.customer,name='customer'),
    path('customer/create',CustomerView.create,name='customerCreate'),
    path('customer/update/<int:id>',CustomerView.update,name='customerupdate'),
    path('customer/delete/<int:id>',CustomerView.delete, name ="customerdelete"),
    path('customer/view/<int:id>/',CustomerView.view,name='customer_view'),
    path("image/<int:id>",CustomerView.imagedelete, name ="image"), 


    # provider urls  
    path('provider',ProviderView.provider,name='provider'),
    path('provider/create',ProviderView.create,name='providercreate'),
    path('provider/update/<int:id>',ProviderView.update,name='providerupdate'),
    path('provider/delete/<int:id>',ProviderView.delete, name ="providerdelete"),

    # agencies urls
    path('agencies',AgencyView.agencies,name='agencies'),
    path('agencies/create',AgencyView.create,name='agenciesCreate'),
    path('agencies/update/<int:id>',AgencyView.update,name='agenciesupdate'),
    path('agencies/delete/<int:id>',AgencyView.delete, name ="agenciesdelete"),

    # # pedimentos urls
    path('pedimentos',PedimentorView.index,name='pedimentos'),
    path('pedimentos/create',PedimentorView.create,name='pedimentosCreate'),
    path('pedimentos/update/<int:id>',PedimentorView.update,name='pedimentos_update'),
    path('pedimentos/delete/<int:id>',PedimentorView.delete, name ="pedimentos_delete"),
    path('pedimentos/view/<int:id>/',PedimentorView.view,name='pedimentos_view'),
    path('pedi/<int:id>/',PedimentorView.pedi,name='pedi'), 

    # # inventory urls
    path('inventory',InventoryView.inventory,name='inventory'),
    path('inventory/create',InventoryView.create,name='create_inventory'),
    path('inventory/update/<int:id>',InventoryView.update,name='inventory_update'),
    path('inventory/delete/<int:id>',InventoryView.delete, name ="inventory_delete"), 

    # # shipper urls
    path('shipper',ShipperView.shipper, name='shipper'),
    path('shipper/create',ShipperView.create,name='shipper_create'),
    path('shipper/update/<int:id>',ShipperView.update,name='shipper_update'),
    path('shipper/delete/<int:id>',ShipperView.delete, name ="shipper_delete"), 
    path('shipper/update-shipper-status/',ShipperView.updateShipperStatus, name ="update-shipper-status"),
    path('shipper/shipper-vin/',ShipperView.shipperVin, name ="shipper-vin"),

    # # insurance urls
     path('insurance',InsuranceView.insurance,name='insurance'),
     path('insurance/create',InsuranceView.create,name='insurance_create'),
     path('insurance/update/<int:id>',InsuranceView.update,name='insurance_update'),
     path('insurance/delete/<int:id>',InsuranceView.delete, name ="insurance_delete"),
     path('insurance/update-insurance-status/',InsuranceView.updateInsuranceStatus, name ="update-insurance-status"),
     path('insurance/insurance-vin/',InsuranceView.InsuranceVin, name ="insurance-vin"),

    # #temporary permits urls
    path('temp_permits',TemporaryPermitView.index,name='temp_permits'),
    path('temp_permits/create',TemporaryPermitView.create,name='create_temp_permits'),
    path('temp_permits/update/<int:id>',TemporaryPermitView.update,name='temp_permits_update'),
    path('temp_permits/delete/<int:id>',TemporaryPermitView.delete, name ="temp_permits_delete"),
    path('temp_permits/update-temporary-status/',TemporaryPermitView.updateTemporaryStatus, name ="update-temporary-status"),
    path('temp_permits/temp_permits-vin/',TemporaryPermitView.permitVin, name ="temp_permits-vin"),


    # # Released urls
    path('released',ReleasedView.released,name='released'),
    path('released/create',ReleasedView.create,name='create_released'),
    path('released/update/<int:id>',ReleasedView.update,name='released_update'),
    path('released/delete/<int:id>',ReleasedView.delete, name ="released_delete"),
    path('released/view/<int:id>/',ReleasedView.view,name='released_view'),
    path('released/update-released-status/',ReleasedView.updateReleasedStatus, name ="update-released-status"),
    path("remove/<int:id>",ReleasedView.remove, name ="remove_img"),
    path('released/released-vin/',ReleasedView.releasedVin, name ="released-vin"),


     # Company urls
    path('company',CompanyView.index,name='company'),
    path('company/create',CompanyView.create,name='add_company'),
    path('company/update/<int:id>',CompanyView.update,name='company_update'),
    path('company/delete/<int:id>',CompanyView.delete, name ="company_delete"), 
    path('company/updateperm/<int:id>',CompanyView.updatecheck,name='company_check'),
    path('company/view/<int:id>/',CompanyView.view,name='company_view'),
    path('company/<int:id>/',CompanyView.account,name='account_company'),





   
]
