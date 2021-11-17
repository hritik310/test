from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from app.models import *
from django.contrib.auth.decorators import login_required

@login_required
def insurance(request):
    context = {'insurance_list':Insurance.objects.all()}
    return render(request,"insurance/index.html",context) 



@login_required
def create(request):
    if request.method == 'POST':
        insurance=Insurance()
        print(request.POST)
        #jfgjffjgfhh
        insurance.Type = request.POST.get('type')
        insurance.policy_number = request.POST.get('policy_number')
        insurance.date = request.POST.get('ins_date')
        insurance.ins_name = request.POST.get('ins_name')
        insurance.days = request.POST.get('ins_days')
        insurance.vin = request.POST.get('ins_vin')
        insurance.make = request.POST.get('ins_make')
        insurance.year = request.POST.get('ins_year')
        insurance.note = request.POST.get('ins_notes')
        insurance.save()
        messages.success(request,'Insurance Added Successfully.')
        return redirect('/insurance')
    return render(request,"insurance/create.html")


@login_required      
def update(request, id):
    insurance = Insurance.objects.get(id=id)
    if request.method == 'POST':
        insurance.Type = request.POST.get('type')
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