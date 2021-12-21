from django.contrib.auth import authenticate, login,logout
from app.models import *
from app.helper import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import redirect
from django.db.models import Q



def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))

@guest_user
def userLogin(request):
    if request.method == "POST":
        uname= request.POST.get('username')
        print(uname)
        upass= request.POST.get('password')
        print(upass)
        user = authenticate(username=uname,password=upass)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('/home')

        else:
            messages.error(request,"Invalid Credential")
            return redirect('/login')

    return render(request,"app/login.html")


@login_required
def userLogout(request):
    auth.logout(request)
    return redirect('/login')


@login_required
def home(request):
    permissions = User.objects.filter(company_id=request.user.id)
    print(permissions.query)

    # per = Permissions.objects.filter(user_id = request.user.id)
    # print(per.query)
    # permissions = userPermission.objects.filter(user_id=request.user.id)
    # print(permissions.query)
    # userPermissions = permissions
    # print(userPermissions)
    # if userPermissions:
    #     if permissionGiven in userPermissions:
    #         return True
    searchdata = request.GET.get('data',False)
    dateRange = request.GET.get('date',False)
    print(dateRange)
    count= Released.objects.all().count()
    pedi= Pedimentos.objects.all().count()
    insura= Insurance.objects.all().count()
    temp= Temporary_Permits.objects.all().count()
    custom= Customer.objects.all().count()
    shipp= Shipper_Exports.objects.all().count()
    show =Shipper_Exports.objects.all().order_by('-id')[:20]
    shows=Insurance.objects.all().order_by('-id')[:20]  
    display=Temporary_Permits.objects.all().order_by('-id')[:20]   
    if dateRange:
        splitRange = dateRange.split(" - ")
        print(splitRange)
        startDate = datetime.datetime.strptime(splitRange[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        print(startDate)
        endDate = datetime.datetime.strptime(splitRange[1], "%m/%d/%Y").strftime("%Y-%m-%d")
        print(endDate)
        count= Released.objects.filter(created_at__date__range=(startDate, endDate)).count()
        pedi= Pedimentos.objects.filter(created_at__date__range=(startDate, endDate)).count()
        insura= Insurance.objects.filter(created_at__date__range=(startDate, endDate)).count()
        temp= Temporary_Permits.objects.filter(created_at__date__range=(startDate, endDate)).count()
        custom= Customer.objects.filter(created_at__date__range=(startDate, endDate)).count()
        shipp= Shipper_Exports.objects.filter(created_at__date__range=(startDate, endDate)).count()

    if not searchdata:
        searchdata=""
    shipper,temp_permit,released,insurance=([] for i in range(4))


    if searchdata:
        shipper = Shipper_Exports.objects.filter(Q(name__icontains=searchdata)|Q(vin__icontains=searchdata)|Q(make__icontains=searchdata))
        print(shipper.query)
    if searchdata:
        temp_permit = Temporary_Permits.objects.filter(Q(permit_name__icontains=searchdata)|Q(permit_vin__icontains=searchdata)|Q(permit_make__icontains=searchdata))
        print(temp_permit.query)
    if searchdata:
        released = Released.objects.filter(Q(name__icontains=searchdata)|Q(vin__icontains=searchdata)|Q(make__icontains=searchdata))
        print(shipper.query)
    if searchdata:
        insurance = Insurance.objects.filter(Q(ins_name__icontains=searchdata)|Q(vin__icontains=searchdata)|Q(make__icontains=searchdata))
        print(insurance.query)
    context= {'count': count,'pedi':pedi,'custom':custom,'shipp':shipp,'temp':temp,'insurance':insura,'shipper':shipper,'temp_permit':temp_permit,'released':released,'insuran':insurance,'search':searchdata,'show':show,'shows':shows,'display':display}
    return render(request,"home.html",context)

    # count= Released.objects.all().count()
    # pedi= Pedimentos.objects.all().count()
    # insura= Insurance.objects.all().count()
    # temp= Temporary_Permits.objects.all().count()
    # custom= Customer.objects.all().count()
    # shipp= Shipper_Exports.objects.all().count()={'user': request.user,'shipper':shipper}    
    # context= {'count': count,'pedi':pedi,'custom':custom,'insurance':insura,'shipp':shipp,'temp':temp}

 # today = datetime.date.today()
 #    lastMonth = today - datetime.timedelta(days=30)
 #    count= Released.objects.filter(created_at__date__range=(lastMonth,today)).count()
 #    print(connection.queries[-1]['sql'])
 #    pedi= Pedimentos.objects.filter(created_at__date__range=(lastMonth,today)).count()
 #    insura= Insurance.objects.filter(created_at__date__range=(lastMonth,today)).count()
 #    temp= Temporary_Permits.objects.filter(created_at__date__range=(lastMonth,today)).count()
 #    custom= Customer.objects.filter(created_at__date__range=(lastMonth,today)).count()
 #    shipp= Shipper_Exports.objects.filter(created_at__date__range=(lastMonth,today)).count()  
 #    context= {'count': count,'pedi':pedi,'custom':custom,'insurance':insura,'shipp':shipp,'temp':temp}