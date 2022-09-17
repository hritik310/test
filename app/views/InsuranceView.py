from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from app.models import *
from django.contrib.auth.decorators import login_required
from app.helper import *
from vininfo import Vin

@login_required
def insurance(request):
    startDate=request.GET.get('start_date',False)
    endDate=request.GET.get('end_date',False)
    paid = request.GET.get('paid',False)
    insurance=Insurance.objects.all()
    if isProvider(request):
        insurance=insurance.filter(created_by=request.user)

    if startDate and endDate:
        insurance = insurance.filter(created_at__date__range=(startDate, endDate))

    if paid:
        insurance = insurance.filter(paid=paid)
        print(insurance.query)

    context = {'insurance_list':insurance}
    return render(request,"insurance/index.html",context)




@login_required
def create(request):
    # user=User.objects.get(id=id)
    if request.method == 'POST':
        insurance=Insurance()
        print(request.POST)
        #jfgjffjgfhh
        insurance.Type = request.POST.get('type')
        insurance.insurer = request.POST.get('insurer')
        insurance.policy_number = request.POST.get('policy_number')
        insurance.date = request.POST.get('ins_date')
        insurance.ins_name = request.POST.get('ins_name')
        insurance.days = request.POST.get('ins_days')
        insurance.vin = request.POST.get('ins_vin')
        insurance.make = request.POST.get('ins_make')
        insurance.year = request.POST.get('ins_year')
        insurance.note = request.POST.get('ins_notes')
        insurance.created_by=request.user
        insurance.save()
        messages.success(request,'Insurance Added Successfully.')
        return redirect('/insurance')
    return render(request,"insurance/create.html")


@login_required      
def update(request, id):
    insurance = Insurance.objects.get(id=id)
    if request.method == 'POST':
        insurance.Type = request.POST.get('type')
        insurance.insurer = request.POST.get('insurer')
        insurance.policy_number = request.POST.get('policy_number')
        insurance.date = request.POST.get('ins_date')
        insurance.ins_name = request.POST.get('ins_name')
        insurance.days = request.POST.get('ins_days')
        insurance.vin = request.POST.get('ins_vin')
        insurance.make = request.POST.get('ins_make')
        insurance.year = request.POST.get('ins_year')
        insurance.note = request.POST.get('ins_notes')
        insurance.save()
        messages.success(request,'Insurance details updated Successfully.')
        return redirect('/insurance')
    return render(request,"insurance/update.html",{'insurance_id':insurance})



@login_required
def delete(request, id):
    insurance = Insurance.objects.get(id=id)
    insurance.delete()
    return redirect('/insurance')


@login_required
def updateInsuranceStatus(request):
  
    insurance = Insurance.objects.get(id=request.GET.get('id'))
    print(insurance)
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


@login_required
def InsuranceVin(request):

    insurance = Vin(request.GET.get('id'))
    print("insurance")
    print(insurance)
    print(insurance.manufacturer)
    print(insurance.years)


    data = {
    "status":"OK",
    "make":insurance.manufacturer,
    "year":insurance.years
 
    }
    return JsonResponse(data)


