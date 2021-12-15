from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required
from app.forms.account import *
from app.helper import *



@login_required
def create(request):
    if request.method == 'POST':
        accountform = AccountCreateForm(request.POST)
        if accountform.is_valid():
            accountform.instance.user_type=3
            user=accountform.save(commit=False)
            password = accountform.cleaned_data['password']
            user.set_password(password)

            user.save()
            messages.success(request,'Customer Added Successfully.')
            return redirect('/account')
        else:
            return render(request,"account/create.html",{'form':accountform})

    form = AccountCreateForm()
    return render(request,"account/create.html",{'form':form})


@login_required
def account(request):
    context = {'employee_list':User.objects.all()}
    return render(request,"account/index.html",context)


@login_required
def update(request,id):
    employee = User.objects.get(pk=id)
    current=request.user.get_all_permissions()
    print(current)
    print(employee.phone)
    if request.method == 'POST':
        employee.username = request.POST.get('username')
        employee.email = request.POST.get('email')
        employee.password = request.POST.get('password')
        employee.phone = request.POST.get('phone')
        
        employee.save()
        messages.success(request,'Accounts details updated Successfully.')
        return redirect('/account')
   
    return render(request,"account/update.html",{'employee':employee})


@login_required
def delete(request,id):
    employee = User.objects.get(pk=id)
    employee.delete()
    return redirect('/account')


@login_required
def permission(request,id):
    if request.method == 'POST':
        perm = Permissions()
        perm.permission = request.POST.getlist('permission')
        print(perm.permission)
        perm.user_id = id
        perm.save()
    return render(request,"account/permission.html")


