from django.shortcuts import render

# Create your views here.
def index(request):
    return render(
        request,
        'firstapp/index.html',
        {}
    )
    
def htmlview01(request):
    return render(
        request,
        'firstapp/front/01_html.html',
        {}
    )