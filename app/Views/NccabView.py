from django.shortcuts import render,HttpResponse


def create(request):
	req = request.GET.get('cars')
	print(req)
	return HttpResponse("ok")