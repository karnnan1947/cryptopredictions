from django.shortcuts import render,redirect
from .forms import Selectalgorithm,SelectCoin,SelectDuration
from users.forms import FeedbackForm
# Create your views here.
def predicts(request):
    form = FeedbackForm()
    if request.method == 'POST':
        forma = Selectalgorithm(request.POST)
        formb = SelectCoin(request.POST)
        formc = SelectDuration(request.POST)
        if forma.is_valid() and formb.is_valid() and formc.is_valid() :
            selected_item=forma.cleaned_data['item']
            selected_coin=formb.cleaned_data['item']
            selected_duration=formc.cleaned_data['item']
            print(selected_item,selected_coin,selected_duration)
    else:
        forma=Selectalgorithm()
        formb=SelectCoin()
        formc=SelectDuration()
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)  # Don't save to DB yet
                feedback.user = request.user        # Assign the logged-in user
                feedback.save()
                return redirect('predicts')  

    return render(request,"predict.html",{'forma': forma , 'formb': formb , 'formc':formc, 'form' : form})