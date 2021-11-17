from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required

@login_required
def create(request):
    if request.method == 'POST':
        m = Agencies()
        print(request.POST)
        m.name = request.POST.get('name')
        m.domain = request.POST.get('domain')
        m.active = request.POST.get('active')
        m.patente = request.POST.get('patente')
        
        m.save()
        messages.success(request,'Agencies Added Successfully.')
        return redirect('/agencies')
    return render(request,"agency/create.html")
    
@login_required
def agencies(request):
    context = {'employee_list':Agencies.objects.all()}
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