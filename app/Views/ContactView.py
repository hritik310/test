from django.shortcuts import render,redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def contact(request):
    if request.method =="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')                                
        subject, from_email, to = 'Contact us.', 'info@datasportslab.com','info@datasportslab.com',
        text_content = 'This is an important message.'
        html_content = render_to_string('contactinfo/contact.html',{"name":name,'comment':comment,'email': email})
        msg = EmailMultiAlternatives(subject,text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request,"Contact request submitted successfully")
    return render(request,'contactinfo/contactform.html')