from django.http import HttpResponse
from django.shortcuts import render
def index(request):
    parmas={'name':"Chirag","place":"Bhavngar"}
    return render(request,'index.html',parmas)
    # return HttpResponse('''<h1>Hello World<h1/>
    #                     I am Index
    #                     <a href="https://www.logicraysacademy.com/">Logicraysacademy</a>
    #                     <a href="/about">About Us</a>
    #                     ''')
def about(request):
    return render(request,'about.html')
    # return HttpResponse('''
    #         <h1>Hello I am Your About</h1>
    #                      <a href="/">Home</a>
    # ''')


def resume(request):
    fname=request.GET.get('fname')
    lname=request.GET.get('lname')
    email=request.GET.get('email')
    sname=request.GET.get('sname')
    technology=request.GET.get('technology')
    pozition=request.GET.get('pozition')
    number=request.GET.get('number')
    mobile=request.GET.get('mcleobile')
    address=request.GET.get('address')
    params={"fname":fname,"lname":lname,"email":email,"sname" :sname,"technology":technology,"pozition":pozition,"number":number,"mobile":mobile,"address":address}
    return render(request,'resume.html',params)

