from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required

@login_required
def inventory(request):
    context = {'inventory_list':Inventories.objects.all()}
    return render(request,"Inventory/index.html", context)


@login_required
def create(request):

    pedimen=Pedimentos.objects.all()
    if request.method == 'POST':
        inven=Inventories()
        print(request.POST)
        inven.order_no = request.POST.get('order_no')
        inven.quantity = request.POST.get('quantity')
        inven.unit_type = request.POST.get('unit_type')
        inven.vechicle = request.POST.get('vechicle')
        inven.description = request.POST.get('description')
        inven.price = request.POST.get('price')
        inven.price_total = request.POST.get('price_total')
        inven.pedimentorid_id = request.POST.get('pedimentorid')
        inven.save()
        messages.success(request,'Inventory Added Successfully.')
        return redirect('/inventory')

    return render(request,"Inventory/create.html",{'pedi':pedimen})

@login_required    
def update(request, id):
    inven = Inventories.objects.get(id=id)
    if request.method == 'POST':
        print(request.POST)
        inven.order_no = request.POST.get('order_no')
        inven.quantity = request.POST.get('quantity')
        inven.unit_type = request.POST.get('unit_type')
        inven.vechicle = request.POST.get('vechicle')
        inven.description = request.POST.get('description')
        inven.price = request.POST.get('price')
        inven.price_total = request.POST.get('price_total')
        inven.save()
        messages.success(request,'Inventory details updated Successfully.')
        return redirect('/inventory')

    return render(request,"Inventory/update.html",{'inventory_id':inven})

@login_required    
def delete(request, id):
    inventory = Inventories.objects.get(id=id)
    inventory.delete()
    return redirect('/inventory')