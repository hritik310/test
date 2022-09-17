from django.shortcuts import render,HttpResponseRedirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import *
from django.shortcuts import redirect
import random
from django.contrib import messages

import string
from app.helper import *

def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))



@guest_user
def userLogin(request):
    if request.method == "POST":
        uname= request.POST.get('username')
        print(uname)
        upass= request.POST.get('password')
        print(upass)
        user = authenticate(username=uname,password=upass)
        if user is not None:
            login(request,user)
            return redirect('/home/')

        else:
            return HttpResponse("Invalid Credential")

    return render(request,"app/login.html")

def userLogout(request):
    auth.logout(request)
    return redirect('/login/')


@login_required
def home(request):
    return render(request,"home.html",context={"user": request.user})


# provider Crud operations.


def provider(request):
    context = {'employee_list':User.objects.all()}
    return render(request,"provider/create.html",context)

def providerIndex(request):
    if request.method == 'POST':
        myuser = User()
        print(request.POST)
        myuser.name = request.POST.get('name')
        myuser.owner = request.POST.get('owner')
        myuser.email = request.POST.get('email')
        myuser.tax_id = request.POST.get('number')
        
        myuser.save()
        messages.success(request,'Provider Added Successfully.')

        return redirect('/provider/')
    return render(request,"provider/index.html")

def providerupdate(request,id):
    employee = User.objects.get(pk=id)
    print(employee)
    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.owner = request.POST.get('owner')
        employee.email = request.POST.get('email')
        employee.tax_id = request.POST.get('number')
        
        employee.save()
        messages.success(request,'Provider details updated Successfully.')
        return redirect('/provider/')
   
    return render(request,"provider/providerUpdate.html",{'employee':employee})

def providerdelete(request,id):
    employee = User.objects.get(pk=id)
    employee.delete()
    return redirect('/provider/')


# agencies Crud operations.



def agenciesCreate(request):
    if request.method == 'POST':
        m = Agencies()
        print(request.POST)
        m.name = request.POST.get('name')
        m.domain = request.POST.get('domain')
        m.active = request.POST.get('active')
        m.patente = request.POST.get('patente')
        
        m.save()
        messages.success(request,'Agencies Added Successfully.')
        return redirect('/agencies/')
    return render(request,"provider/agenciesCreate.html")

def agencies(request):
    context = {'employee_list':Agencies.objects.all()}
    return render(request,"provider/agencies.html",context)



def agenciesupdate(request,id):
    agencies = Agencies.objects.get(pk=id)
    print(customer)
    if request.method == 'POST':
        agencies.name = request.POST.get('name')
        agencies.domain = request.POST.get('domain')
        agencies.active = request.POST.get('active')
        agencies.patente = request.POST.get('patente')
        
        
        agencies.save()
        messages.success(request,'Agencies details updated Successfully.')
        return redirect('/agencies/')
   
    return render(request,"provider/agenciesUpdate.html",{'agencies':agencies})

def agenciesdelete(request,id):
    agencies = Agencies.objects.get(pk=id)
    agencies.delete()
    return redirect('/agencies/')



# customer Crud operations.


def customerCreate(request):
    if request.method == 'POST':
        my = Customer()
        print(request.POST)
        my.passport_id = request.POST.get('passport_Id')
        my.name = request.POST.get('name')
        my.address = request.POST.get('address')
        my.country = request.POST.get('country')
        my.phone = request.POST.get('number')
        
        my.save()
        messages.success(request,'Customer Added Successfully.')
        return redirect('/customer/')
    return render(request,"provider/customerCreate.html")


def customer(request):
    context = {'employee_list':Customer.objects.all()}
    return render(request,"provider/customer.html",context)




def customerupdate(request,id):
    customer = Customer.objects.get(id=id)
    print(customer)
    if request.method == 'POST':
        customer.passport_id = request.POST.get('passport_Id')
        customer.name = request.POST.get('name')
        customer.country = request.POST.get('country')
        customer.phone = request.POST.get('number')
        customer.address = request.POST.get('address')
        
        
        customer.save()
        messages.success(request,'Customer details updated Successfully.')
        return redirect('/customer/')
   
    return render(request,"provider/customerupdate.html",{'customer':customer})


def customerdelete(request,id):
    customer = Customer.objects.get(pk=id)
    customer.delete()
    return redirect('/customer/')

#pedimentos
def pedimentos(request):
    context = {'pedimentos_list':Pedimentos.objects.all()}
    return render(request,"pedimentos/table.html",context )

def pedimentosCreate(request):
    if request.method == 'POST':
        pedi=Pedimentos()
        pedi.refrence_id = request.POST.get('passport_Id')
        pedi.pedimento_no = request.POST.get('name')
        pedi.date = request.POST.get('address')
        pedi.importer = request.POST.get('country')
        pedi.office = request.POST.get('office')
        pedi.signature = request.POST.get('signature')
        pedi.payment = request.POST.get('payment')
        pedi.cove = request.POST.get('cove')
        pedi.doda = request.POST.get('doda')
        pedi.ready = request.POST.get('ready')
        pedi.save()
        messages.success(request,'Pedimentos Added Successfully.')
        return redirect('/pedimentos/')

    return render(request,"pedimentos/pedimentosCreate.html")
def pedimentos_update(request, id):
    pedi = Pedimentos.objects.get(id=id)
    if request.method == 'POST':
        pedi.refrence_id = request.POST.get('refrence_id')
        pedi.pedimento_no = request.POST.get('name')
        pedi.date = request.POST.get('address')
        pedi.importer = request.POST.get('country')
        pedi.office = request.POST.get('office')
        pedi.signature = request.POST.get('signature')
        pedi.payment = request.POST.get('payment')
        pedi.cove = request.POST.get('cove')
        pedi.doda = request.POST.get('doda')
        pedi.ready = request.POST.get('ready')
        pedi.save()
        messages.success(request,'Pedimentos details updated Successfully.')
        return redirect('/pedimentos/')

    return render(request,"pedimentos/update_pedimentos.html",{'pedimentos_id':pedi})
def pedimentos_delete(request, id):
    pedimentos = Pedimentos.objects.get(id=id)
    pedimentos.delete()
    return redirect('/pedimentos/')
#inventory
def inventory(request):
    context = {'inventory_list':Inventories.objects.all()}
    return render(request,"pedimentos/inventory_table.html", context)

def create_inventory(request):

    pedimen=Pedimentos.objects.all()
    if request.method == 'POST':
        inven=Inventories()
        print(request.POST)
        inven.order_no = request.POST.get('order_no')
        inven.quantity = request.POST.get('quantity')
        inven.unit_type = request.POST.get('unit_type')
        inven.vechicle = request.POST.get('vechicle')
        inven.description = request.POST.get('description')
        inven.price = request.POST.get('price')
        inven.price_total = request.POST.get('price_total')
        inven.pedimentorid_id = request.POST.get('pedimentorid')
        inven.save()
        messages.success(request,'Inventory Added Successfully.')
        return redirect('/inventory/')

    return render(request,"pedimentos/create_inventory.html",{'pedi':pedimen})
def inventory_update(request, id):
    inven = Inventories.objects.get(id=id)
    if request.method == 'POST':
        print(request.POST)
        inven.order_no = request.POST.get('order_no')
        inven.quantity = request.POST.get('quantity')
        inven.unit_type = request.POST.get('unit_type')
        inven.vechicle = request.POST.get('vechicle')
        inven.description = request.POST.get('description')
        inven.price = request.POST.get('price')
        inven.price_total = request.POST.get('price_total')
        inven.save()
        messages.success(request,'Inventory details updated Successfully.')
        return redirect('/inventory/')

    return render(request,"pedimentos/update_inventory.html",{'inventory_id':inven})
def inventory_delete(request, id):
    inventory = Inventories.objects.get(id=id)
    inventory.delete()
    return redirect('/inventory/')
#shipper
def shipper(request):
    context = {'shipper_list':Shipper_Exports.objects.all()}
    return render(request,"shipper/shipper_view.html", context)

def create_shipper(request):
    if request.method == 'POST':
        shipper=Shipper_Exports()
        print(request.POST)
        shipper.itn = request.POST.get('itn')
        shipper.date = request.POST.get('date')
        shipper.name = request.POST.get('shipper_name')
        shipper.refrence = request.POST.get('refrence')
        shipper.vin = request.POST.get('vin')
        shipper.make = request.POST.get('make')
        shipper.year = request.POST.get('year')
        shipper.note = request.POST.get('note')
        shipper.save()
        messages.success(request,'Shipper_Exports Added Successfully.')
        return redirect('/shipper/')

    return render(request,"shipper/create_shipper.html")
def shipper_update(request, id):

    shipper = Shipper_Exports.objects.get(id=id)
    if request.method == 'POST':
        print(request.POST)
        shipper.itn = request.POST.get('itn')
        shipper.date = request.POST.get('date')
        shipper.name = request.POST.get('shipper_name')
        shipper.refrence = request.POST.get('refrence')
        shipper.vin = request.POST.get('vin')
        shipper.make = request.POST.get('make')
        shipper.year = request.POST.get('year')
        shipper.note = request.POST.get('note')
        shipper.save()
        messages.success(request,'Shipper details updated Successfully.')
        return redirect('/shipper/')

    return render(request,"shipper/update_shipper.html",{'shipper_id':shipper})
def shipper_delete(request, id):
    shipper = Shipper_Exports.objects.get(id=id)
    shipper.delete()
    return redirect('/shipper/')

def updateShipperStatus(request):
  
    shipper = Shipper_Exports.objects.get(id=request.GET.get('id'))
    if shipper.paid == 1:
        shipper.paid = 0
    else:
        shipper.paid = 1
    shipper.save()
    data = {
    "status":"OK",
    "id":shipper.id,
    "paid":shipper.paid
    }

    return JsonResponse(data)
#insurance
def insurance(request):
    context = {'insurance_list':Insurance.objects.all()}
    return render(request,"insurance/insurance_view.html",context) 

def insurance_create(request):
    if request.method == 'POST':
        insurance=Insurance()
        print(request.POST)
        insurance.date = request.POST.get('ins_date')
        insurance.ins_name = request.POST.get('ins_name')
        insurance.days = request.POST.get('ins_days')
        insurance.vin = request.POST.get('ins_vin')
        insurance.make = request.POST.get('ins_make')
        insurance.year = request.POST.get('ins_year')
        insurance.note = request.POST.get('ins_notes')
        insurance.save()
        messages.success(request,'Insurance Added Successfully.')
        return redirect('/insurance/')
    return render(request,"insurance/create_insurance.html")  
def insurance_update(request, id):
    insurance = Insurance.objects.get(id=id)
    if request.method == 'POST':
        insurance.date = request.POST.get('ins_date')
        insurance.ins_name = request.POST.get('ins_name')
        insurance.days = request.POST.get('ins_days')
        insurance.vin = request.POST.get('ins_vin')
        insurance.make = request.POST.get('ins_make')
        insurance.year = request.POST.get('ins_year')
        insurance.note = request.POST.get('ins_notes')
        insurance.save()
        messages.success(request,'Insurance details updated Successfully.')
        return redirect('/insurance/')
    return render(request,"insurance/update_insurance.html",{'insurance_id':insurance})

def insurance_delete(request, id):
    insurance = Insurance.objects.get(id=id)
    insurance.delete()
    return redirect('/insurance/')

def updateInsuranceStatus(request):
  
    insurance = Insurance.objects.get(id=request.GET.get('id'))
    if insurance.paid == 1:
        insurance.paid = 0
    else:
        insurance.paid = 1
    insurance.save()
    data = {
    "status":"OK",
    "id":insurance.id,
    "paid":insurance.paid
    }

    return JsonResponse(data)

#temporary permits
def temp_permits(request):
    context = {'permits_list':Temporary_Permits.objects.all()}
    return render(request,"temp_permits/temp_permits_view.html", context)

def create_temp_permits(request):
    if request.method == 'POST':
        permits=Temporary_Permits()
        permits.permit_date = request.POST.get('permit_date')
        permits.permit_name = request.POST.get('permit_name')
        permits.permit_hour = request.POST.get('permit_hour')
        permits.permit_number = request.POST.get('permit_number')
        permits.permit_vin = request.POST.get('permit_vin')
        permits.permit_make = request.POST.get('permit_make')
        permits.permit_year = request.POST.get('permit_year')
        permits.permit_note = request.POST.get('permit_note')
        permits.save()
        messages.success(request,'Temporary_permits Added Successfully.')
        return redirect('/temp_permits/')
    return render(request,"temp_permits/create_temp_permit.html")  

def temp_permitsupdate(request,id):

    permits = Temporary_Permits.objects.get(id=id)
    if request.method == 'POST':
        permits.permit_date = request.POST.get('permit_date')
        permits.permit_name = request.POST.get('permit_name')
        permits.permit_hour = request.POST.get('permit_hour')
        permits.permit_number = request.POST.get('permit_number')
        permits.permit_vin = request.POST.get('permit_vin')
        permits.permit_make = request.POST.get('permit_make')
        permits.permit_year = request.POST.get('permit_year')
        permits.permit_note = request.POST.get('permit_note')
        permits.save()
        messages.success(request,'temp_permits details updated Successfully.') 
        return redirect('/temp_permits/')
    return render(request,"temp_permits/permits_update.html",{'permit_id':permits})  

def temp_permitsdelete(request,id):
    permits = Temporary_Permits.objects.get(id=id)
    permits.delete()
    return redirect('/temp_permits/')

def updateTemporaryStatus(request):
  
    temporary = Temporary_Permits.objects.get(id=request.GET.get('id'))
    if temporary.paid == 1:
        temporary.paid = 0
    else:
        temporary.paid = 1
    temporary.save()
    data = {
    "status":"OK",
    "id":temporary.id,
    "paid":temporary.paid
    }

    return JsonResponse(data)



# Released Views
def released(request):
    context = {'released_list':Released.objects.all()}
    return render(request,"released/released_view.html", context)

def create_released(request):
    if request.method =='POST':
        relea = Released()
        relea.date = request.POST.get('date')
        relea.file = request.POST.get('file')
        relea.name = request.POST.get('name')
        relea.refrence = request.POST.get('refrence')
        relea.vin = request.POST.get('vin')
        relea.make = request.POST.get('make')
        relea.year = request.POST.get('year')
        relea.note = request.POST.get('note')
        relea.save()
        messages.success(request,'Released Created Successfully.')
        return redirect('/released/') 
    

    return render(request,"released/releasedCreate.html")


def released_delete(request,id):
    release = Released.objects.get(id=id)
    release.delete()
    return redirect('/released/')



def released_update(request,id):
    relea = Released.objects.get(pk=id)
    if request.method =='POST':
        relea.date = request.POST.get('date')
        relea.file = request.POST.get('file')
        relea.name = request.POST.get('name')
        relea.refrence = request.POST.get('refrence')
        relea.vin = request.POST.get('vin')
        relea.make = request.POST.get('make')
        relea.year = request.POST.get('year')
        relea.note = request.POST.get('note')
        relea.save()
        messages.success(request,'Released details updated Successfully.')
        return redirect('/released/') 
    

    return render(request,"released/released_update.html",{'released':relea})


def updateReleasedStatus(request):
  
    release = Released.objects.get(id=request.GET.get('id'))
    if release.paid == 1:
        release.paid = 0
    else:
        release.paid = 1
    release.save()
    data = {
    "status":"OK",
    "id":release.id,
    "paid":release.paid
    }

    return JsonResponse(data)


def pedimentor(request,id):
    inventory=Inventories.objects.filter(pedimentorid_id=id)
    return render(request,"pedimentos/pedimentor_inventory.html",{'pedimentor':inventory})



