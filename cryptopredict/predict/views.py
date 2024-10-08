from django.shortcuts import render

# Create your views here.
def predicts(request):
    return render(request,"predict.html")