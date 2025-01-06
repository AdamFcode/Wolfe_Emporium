from django.shortcuts import render

# Create your views here.
def index(request):
    """ Returns render of the index page """

    return render(request, 'home/index.html')

def mission(request):
    """Returns render of the mission statement page"""

    return render(request, 'home/mission.html') 