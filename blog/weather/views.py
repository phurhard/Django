from django.shortcuts import render

# Create your views here.

def index(request):
    '''The homepage of the weather app'''
    if request.method == "POST":
        city = request.POST['city']
        headers = request.headers
        print(headers)
        print(city)
    else:
        city = ""
    return render(request, 'home.html', {'city': city})
