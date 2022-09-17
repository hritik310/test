from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required
from app.forms.customer import *
from app.helper import *


@login_required
def create(request):
    if request.method == 'POST':
        customerform = CustomerCreateForm(request.POST,request.FILES)
        if customerform.is_valid():
            customerform.instance.created_by = request.user
            if customerform.save():
                messages.success(request,'Customer Added Successfully.')
                return redirect('/customer')
        else:
            return render(request,"customer/create.html",{'form':customerform})

    form = CustomerCreateForm()
    return render(request,"customer/create.html",{'form':form})


@login_required
def customer(request):
    startDate = request.GET.get('start_date',False)
    endDate = request.GET.get('end_date',False)
    customer=Customer.objects.all()
    if isProvider(request):
        customer=customer.filter(created_by=request.user)
        print(customer.query)

    if startDate and endDate:
        customer = customer.filter(created_at__date__range=(startDate, endDate))
        print(customer.query)
    context = {'employee_list':customer}
    return render(request,"customer/index.html",context)



@login_required
def update(request,id):
    customer = Customer.objects.get(id=id)
    print(customer)
    if request.method == 'POST':
        if (request.FILES.get('pass_image',None)):
            img = request.FILES['pass_image'];
            customer.passport_upload = img
        customer.passport_id = request.POST.get('passport_Id')
        customer.passport_expiry = request.POST.get('passport_expiry')
        customer.name = request.POST.get('name')
        customer.country = request.POST.get('country')
        customer.phone = request.POST.get('number')
        customer.email = request.POST.get('email')
        customer.address = request.POST.get('address')
        customer.city    =request.POST.get('city')
        customer.rfc     =request.POST.get('rfc')
        customer.state   =request.POST.get('state')
        customer.curp   =request.POST.get('curp')
        
        
        customer.save()
        messages.success(request,'Customer details updated Successfully.')
        return redirect('/customer')
   
    return render(request,"customer/update.html",{'customer':customer})

@login_required
def delete(request,id):
    customer = Customer.objects.get(pk=id)
    customer.delete()
    return redirect('/customer')

@login_required
def view(request,id):
    customer = Customer.objects.get(id=id)
    return render(request,"customer/view.html",{'custom':customer})


@login_required   
def imagedelete(request,id):
    cust=Customer.objects.get(id=id)
    print(cust)
    cust.passport_upload=""
    cust.save()

    return render(request,"customer/update.html",{'customer':cust})
