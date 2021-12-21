from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required
from app.forms.provider import *
from django .contrib.auth.hashers import make_password



@login_required
def index(request):
	context = {'company_list':Company.objects.all()}
	return render(request,"company/index.html",context )

@login_required
def create(request):
	if request.method=="POST":
		per=userPermission()
		company=Company()
		company.company_name=request.POST.get("company_name")
		company.company_description=request.POST.get("company_description")
		company.save()
		per.company_id=company.id
		per.save()
		messages.success(request,'Company Added Successfully.')
		return redirect('/company')
	return render(request,"company/create.html")



@login_required
def update(request,id):
	company = Company.objects.get(id=id)
	print(company)
	if request.method == 'POST':
		company.company_name=request.POST.get("company_name")
		company.company_description=request.POST.get("company_description")
		company.save()
		messages.success(request,'Company updated Successfully.')
		return redirect('/company')
	return render(request,"company/update.html",{'company':company})


@login_required
def delete(request,id):
	company = Company.objects.get(id=id)
	company.delete()
	return redirect('/company')


@login_required
def updatecheck(request,id):
	a=userPermission.objects.get(company=id)
	if request.method == 'POST':
		a.shipper_Exports = request.POST.get('shipper_Exports',False)
		a.pedimentos = request.POST.get('pedimentos',False)
		a.temporary_Permits = request.POST.get('temporary_Permits',False)
		a.customer = request.POST.get('customer',False)
		a.insurance = request.POST.get('insurance',False)
		a.released = request.POST.get('released',False)
		a.reports = request.POST.get('reports',False)
		a.validate = request.POST.get('validate',False)
		a.catalogs = request.POST.get('catalogs',False)
		a.save()
		messages.success(request,'Permission updated Successfully.')
		return redirect(request.path_info)
	return render(request,"company/permission.html",{"save":a})


@login_required
def view(request,id):
    comp = Company.objects.get(id=id)
    print(comp)
    userview = User.objects.filter(company_id = id)
    print(userview.query)
    return render(request,"company/view.html",{'company':comp,'account':userview})

    
@login_required
def account(request,id):
    user = Company.objects.get(id=id)
    if request.method == 'POST':
        inven=User()

        inven.username = request.POST.get('username')
        inven.email = request.POST.get('email')
        inven.password = request.POST.get('password')
        inven.password = make_password(inven.password)
        inven.phone = request.POST.get('phone')
        inven.company_id = id
        inven.user_type=3
        inven.save()
        messages.success(request,'Account Added Successfully.')
        return redirect('company_view',id=id)
    return render(request,"company/company_account.html",{'pedimentos':user})
    