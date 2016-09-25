from django.http import HttpResponse

# Create your views here.
def index(request):
    ''' index Hello World
    '''
    return HttpResponse("Hello World")
