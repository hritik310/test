from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required
from app.forms.provider import *




@login_required
def provider(request):
    context = {'employee_list':User.objects.all()}
    return render(request,"provider/index.html",context)



@login_required
def create(request):
    if request.method == 'POST':
        providerform = ProviderCreateForm(request.POST)
        if providerform.is_valid():
            if providerform.save():
                messages.success(request,'Provider Added Successfully.')
                return redirect('/provider')
        else:
            return render(request,"provider/create.html",{'form':providerform})

    form = ProviderCreateForm()
    return render(request,"provider/create.html",{'form':form})


@login_required
def update(request,id):
    employee = User.objects.get(pk=id)
    print(employee)
    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.owner = request.POST.get('owner')
        employee.email = request.POST.get('email')
        employee.tax_id = request.POST.get('number')
        
        employee.save()
        messages.success(request,'Provider details updated Successfully.')
        return redirect('/provider')
   
    return render(request,"provider/update.html",{'employee':employee})


@login_required
def delete(request,id):
    employee = User.objects.get(pk=id)
    employee.delete()
    return redirect('/provider')
