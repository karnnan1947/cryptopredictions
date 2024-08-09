from django.shortcuts import render

# Create your views here.
def newz(request):
    api_request=request.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    api=json.loads(api_request.content)
    return render(request,'newz.html,{'api':api}')