from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app.helper import *



@login_required
def index(request):
    startDate = request.GET.get('start_date',False)
    endDate = request.GET.get('end_date',False)
    pedimentor=Pedimentos.objects.all()
    if isProvider(request):
        pedimentor = pedimentor.filter(created_by = request.user)

    if startDate and endDate:
        pedimentor = pedimentor.filter(created_at__date__range=(startDate, endDate))
        print(pedimentor.query)
    context = {'pedimentos_list':pedimentor}
    return render(request,"pedimentos/index.html",context )

@login_required
def create(request):
    customer=Customer.objects.all()
    provider = User.objects.all()
    if request.method == 'POST':
        pedi=Pedimentos()
        pedi.refrence_id = request.POST.get('passport_Id')
        pedi.pedimento_no = request.POST.get('name')
        pedi.date = request.POST.get('address')
        pedi.importer = request.POST.get('country')
        pedi.office = request.POST.get('office')
        pedi.signature = request.POST.get('signature')
        pedi.payment = request.POST.get('payment')
        pedi.cove = request.POST.get('cove')
        pedi.doda = request.POST.get('doda')
        pedi.ready = request.POST.get('ready')
        pedi.remarks = request.POST.get('remark')
        pedi.lock1 = request.POST.get('lock1')
        pedi.lock2 = request.POST.get('lock2')
        pedi.lock3 = request.POST.get('lock3')
        pedi.lock4 = request.POST.get('lock4')
        pedi.lock5 = request.POST.get('lock5')
        pedi.lock6 = request.POST.get('lock6')
        pedi.lock7 = request.POST.get('lock7')
        pedi.lock8 = request.POST.get('lock8')
        pedi.supplier = request.POST.get('supplier')
        pedi.created_by = request.user
        pedi.save()
        files = request.FILES.getlist('file',False)
        if files:
            saveMultipleFiles(files,pedi)


        # for f in pedi.document:
        #     Pedimentos(document=f).save()
        messages.success(request,'Pedimentos Added Successfully.')
        return redirect('/pedimentos')

    return render(request,"pedimentos/create.html",{'custom':customer,'provide':provider})
    #     pedimentorform = PedimentorCreateForm(request.POST,request.FILES)
    #     if pedimentorform.is_valid():
    #         if pedimentorform.save():
    #             messages.success(request,'Pedimentos Added Successfully.')
    #             return redirect('/pedimentos')

    #     else:
    #         return render(request,"pedimentos/create.html",{'form':pedimentorform})

    # form = PedimentorCreateForm()
    # return render(request,"pedimentos/create.html",{'form':form,'custom':customer,'provide':provider})


@login_required    
def update(request, id):
    customer=Customer.objects.all()
    provider = User.objects.all()
    pedi = Pedimentos.objects.get(id=id)
    if request.method == 'POST':


        if (request.FILES.get('files',None)):
            img = request.FILES['files'];
            pedi.document = img
        pedi.refrence_id = request.POST.get('refrence_id')
        pedi.pedimento_no = request.POST.get('name')
        pedi.date = request.POST.get('address')
        pedi.importer = request.POST.get('country')
        pedi.office = request.POST.get('office')
        pedi.signature = request.POST.get('signature')
        pedi.payment = request.POST.get('payment')
        pedi.cove = request.POST.get('cove')
        pedi.doda = request.POST.get('doda')
        pedi.ready = request.POST.get('ready')
        pedi.remarks = request.POST.get('remark')
        pedi.lock1 = request.POST.get('lock1')
        pedi.lock2 = request.POST.get('lock2')
        pedi.lock3 = request.POST.get('lock3')
        pedi.lock4 = request.POST.get('lock4')
        pedi.lock5 = request.POST.get('lock5')
        pedi.lock6 = request.POST.get('lock6')
        pedi.lock7 = request.POST.get('lock7')
        pedi.lock8 = request.POST.get('lock8')
        pedi.supplier = request.POST.get('supplier')

        pedi.save()
        messages.success(request,'Pedimentos details updated Successfully.')
        return redirect('/pedimentos')

    return render(request,"pedimentos/update.html",{'pedimentos_id':pedi,'custom':customer,'provide':provider})

@login_required    
def update(request, id):
    customer=Customer.objects.all()
    provider = User.objects.all()
    pedi = Pedimentos.objects.get(id=id)
    if request.method == 'POST':


        if (request.FILES.get('files',None)):
            img = request.FILES['files'];
            pedi.document = img
        pedi.refrence_id = request.POST.get('refrence_id')
        pedi.pedimento_no = request.POST.get('name')
        pedi.date = request.POST.get('address')
        pedi.importer = request.POST.get('country')
        pedi.office = request.POST.get('office')
        pedi.signature = request.POST.get('signature')
        pedi.payment = request.POST.get('payment')
        pedi.cove = request.POST.get('cove')
        pedi.doda = request.POST.get('doda')
        pedi.ready = request.POST.get('ready')
        pedi.remarks = request.POST.get('remark')
        pedi.lock1 = request.POST.get('lock1')
        pedi.lock2 = request.POST.get('lock2')
        pedi.lock3 = request.POST.get('lock3')
        pedi.lock4 = request.POST.get('lock4')
        pedi.lock5 = request.POST.get('lock5')
        pedi.lock6 = request.POST.get('lock6')
        pedi.lock7 = request.POST.get('lock7')
        pedi.lock8 = request.POST.get('lock8')
        pedi.supplier = request.POST.get('supplier')

        pedi.save()
        messages.success(request,'Pedimentos details updated Successfully.')
        return redirect('/pedimentos')

    return render(request,"pedimentos/update.html",{'pedimentos_id':pedi,'custom':customer,'provide':provider})

@login_required
def delete(request, id):
    pedimentos = Pedimentos.objects.get(id=id)
    pedimentos.delete()
    return redirect('/pedimentos')

@login_required
def view(request,id):
    pedimentos = Pedimentos.objects.get(id=id)
    inventory=Inventories.objects.filter(pedimentorid_id=id)
    file=File.objects.filter(id=id)
    print (str(file.query))
    return render(request,"pedimentos/view.html",{'pedimentor':inventory,'pedimentos':pedimentos,
        'file':file})
    
@login_required
def pedi(request,id):
    pediment = Pedimentos.objects.get(id=id)
    if request.method == 'POST':
        inven=Inventories()
        inven.order_no = request.POST.get('order_no')
        inven.quantity = request.POST.get('quantity')
        inven.unit_type = request.POST.get('unit_type')
        inven.vechicle = request.POST.get('vechicle')
        inven.description = request.POST.get('description')
        inven.price = request.POST.get('price')
        inven.price_total = request.POST.get('price_total')
        inven.pedimentorid_id = id
        inven.save()
        messages.success(request,'Inventory Added Successfully.')
        return redirect('pedimentos_view',id=id)
    return render(request,"pedimentos/pedimentor_inven.html",{'pedimentos':pediment})