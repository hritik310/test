from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required
from app.forms.provider import *
from app.helper import *





@login_required
def provider(request):
    startDate = request.GET.get('start_date',False)
    endDate = request.GET.get('end_date',False)
    provider = Provider.objects.all()
    if isProvider(request):
        provider = provider.filter(created_by = request.user)


    if startDate and endDate:
        provider = provider.filter(created_at__date__range=(startDate, endDate))
        print(user.query)
    context = {'employee_list':provider}
    return render(request,"provider/index.html",context)



@login_required
def create(request):
    if request.method == 'POST':
        providerform = ProviderCreateForm(request.POST)
        if providerform.is_valid():
            providerform.instance.created_by = request.user
            if providerform.save():
                messages.success(request,'Provider Added Successfully.')
                return redirect('/provider')
        else:
            return render(request,"provider/create.html",{'form':providerform})

    form = ProviderCreateForm()
    return render(request,"provider/create.html",{'form':form})


@login_required
def update(request,id):
    employee = Provider.objects.get(pk=id)
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
    employee = Provider.objects.get(pk=id)
    employee.delete()
    return redirect('/provider')
