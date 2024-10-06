from django.shortcuts import render,redirect
from . models import chart
from django.contrib.auth.decorators import login_required
from users.forms import FeedbackForm

@login_required(login_url='/account')
def charts(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Automatically assign the logged-in user
            feedback.save()
            
    chart_list=chart.objects.order_by('-priority')
    print(chart_list)
    for i in chart_list:
        print(i.title)
    context={'chart' : chart_list}
    return render(request, 'lchart.html',context)