from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required
from app.forms.agency import *

@login_required
def create(request):
    if request.method == 'POST':
        agencyForm = AgencyCreateForm(request.POST)
        if agencyForm.is_valid():
            if agencyForm.save():
                messages.success(request,'Agencies Added Successfully.')
                return redirect('/agencies')
        else:
            print(agencyForm)
            return render(request,"agency/create.html",{'form':agencyForm})
        
    form = AgencyCreateForm(None)  
    return render(request,"agency/create.html",{'form':form})
    
@login_required
def agencies(request):
    startDate = request.GET.get('start_date',False)
    endDate = request.GET.get('end_date',False)
    agency=Agencies.objects.all()

    if startDate and endDate:
        agency = Agencies.objects.filter(created_at__date__range=(startDate, endDate))
        print(agency.query)
    context = {'employee_list':agency}
    return render(request,"agency/index.html",context)


@login_required
def update(request,id):
    agencies = Agencies.objects.get(pk=id)
    if request.method == 'POST':
        agencies.name = request.POST.get('name')
        agencies.domain = request.POST.get('domain')
        agencies.active = request.POST.get('active')
        agencies.patente = request.POST.get('patente')
        
        
        agencies.save()
        messages.success(request,'Agencies details updated Successfully.')
        return redirect('/agencies')
   
    return render(request,"agency/update.html",{'agencies':agencies})

@login_required    
def delete(request,id):
    agencies = Agencies.objects.get(pk=id)
    agencies.delete()
    return redirect('/agencies')