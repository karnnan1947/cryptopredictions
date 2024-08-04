from django.shortcuts import render,redirect
from . models import chart

# Create your views here.
def charts(request):
    chart_list=chart.objects.order_by('-priority')
    print(chart_list)
    for i in chart_list:
        print(i.title)
    context={'chart' : chart_list}
    return render(request, 'lchart.html',context)