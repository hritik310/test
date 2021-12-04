from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required


@login_required
def released(request):
    startDate = request.GET.get('start_date',False)
    endDate = request.GET.get('end_date',False)
    paid = request.GET.get('paid',False)
    released=Released.objects.all()

    if startDate and endDate:
        released = Released.objects.filter(created_at__date__range=(startDate, endDate))
        print(released.query)

    if paid:
        released = released.filter(paid=paid)
        print(released.query)

    context = {'released_list':released}
    return render(request,"released/index.html", context)


@login_required
def create(request):
    if request.method =='POST':
        relea = Released()
        relea.date = request.POST.get('date')
        relea.file = request.POST.get('file')
        relea.name = request.POST.get('name')
        relea.itn = request.POST.get('refrence')
        relea.vin = request.POST.get('vin')
        relea.make = request.POST.get('make')
        relea.year = request.POST.get('year')
        relea.scan = request.FILES.get('scan')
        relea.note = request.POST.get('note')
        relea.save()
        messages.success(request,'Released Created Successfully.')
        return redirect('/released') 
    

    return render(request,"released/create.html")

@login_required
def delete(request,id):
    release = Released.objects.get(id=id)
    release.delete()
    return redirect('/released')


@login_required
def update(request,id):
    relea = Released.objects.get(pk=id)
    if request.method =='POST':
        if (request.FILES.get('scan',None)):
            img = request.FILES['scan'];
            print(img)
            relea.scan = img
        relea.date = request.POST.get('date')
        relea.file = request.POST.get('file')
        relea.name = request.POST.get('name')
        relea.itn = request.POST.get('refrence')
        relea.vin = request.POST.get('vin')
        relea.make = request.POST.get('make')
        relea.year = request.POST.get('year')
        relea.note = request.POST.get('note')
        relea.save()
        messages.success(request,'Released details updated Successfully.')
        return redirect('/released') 
    

    return render(request,"released/update.html",{'released':relea})



@login_required
def view(request,id):
    released = Released.objects.get(id=id)
    return render(request,"released/view.html",{'release':released})



@login_required
def updateReleasedStatus(request):
  
    release = Released.objects.get(id=request.GET.get('id'))
    if release.paid == 1:
        release.paid = 0
    else:
        release.paid = 1
    release.save()
    data = {
    "status":"OK",
    "id":release.id,
    "paid":release.paid
    }

    return JsonResponse(data)


@login_required   
def remove(request,id):
    released=Released.objects.get(id=id)
    print(released)
    released.scan=""
    released.save()

    return render(request,"released/update.html",{'released':released})


