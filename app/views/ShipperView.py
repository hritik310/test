from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required
from app.forms.shipper import *
from app.helper import *
from vininfo import Vin
from django.http import JsonResponse


@login_required
def shipper(request):
    startDate = request.GET.get('start_date',False)
    print(startDate)
    endDate = request.GET.get('end_date',False)
    paid = request.GET.get('paid',False)
    shipper=Shipper_Exports.objects.all()
    if isProvider(request):
        shipper = shipper.filter(created_by = request.user) 

    if startDate and endDate:
        shipper = shipper.filter(created_at__date__range=(startDate, endDate))
        print(shipper.query)

    if paid:
        shipper = shipper.filter(paid=paid)
        print(shipper.query)

    context = {'shipper_list':shipper}
    return render(request,"shipper/index.html",context)


@login_required
def create(request):
    if request.method == 'POST':
        shipperform = ShipperCreateForm(request.POST)
        print(shipperform)
        if shipperform.is_valid():
            shipperform.instance.created_by = request.user
            if shipperform.save():
                messages.success(request,'Shipper_Exports Added Successfully.')
                return redirect('/shipper')
        else:
            return render(request,"shipper/create.html",{'form':shipperform})

    form = ShipperCreateForm()
    return render(request,"shipper/create.html",{'form':form})



@login_required    
def update(request, id):

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
        return redirect('/shipper')

    return render(request,"shipper/update.html",{'shipper_id':shipper})

@login_required
def delete(request, id):
    shipper = Shipper_Exports.objects.get(id=id)
    shipper.delete()
    return redirect('/shipper')


@login_required
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



@login_required
def shipperVin(request):

    shipper = Vin(request.GET.get('id'))
    print(shipper)
    print(shipper.manufacturer)
    print(shipper.years)


    data = {
    "status":"OK",
    "make":shipper.manufacturer,
    "year":shipper.years
 
    }
    return JsonResponse(data)

