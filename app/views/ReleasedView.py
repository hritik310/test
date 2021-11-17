from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required


@login_required
def released(request):
    context = {'released_list':Released.objects.all()}
    return render(request,"released/index.html", context)

@login_required
def create(request):
    if request.method =='POST':
        relea = Released()
        relea.date = request.POST.get('date')
        relea.file = request.POST.get('file')
        relea.name = request.POST.get('name')
        relea.refrence = request.POST.get('refrence')
        relea.vin = request.POST.get('vin')
        relea.make = request.POST.get('make')
        relea.year = request.POST.get('year')
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
        relea.date = request.POST.get('date')
        relea.file = request.POST.get('file')
        relea.name = request.POST.get('name')
        relea.refrence = request.POST.get('refrence')
        relea.vin = request.POST.get('vin')
        relea.make = request.POST.get('make')
        relea.year = request.POST.get('year')
        relea.note = request.POST.get('note')
        relea.save()
        messages.success(request,'Released details updated Successfully.')
        return redirect('/released') 
    

    return render(request,"released/update.html",{'released':relea})



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