from django.http import HttpResponse
from common.similarity import  *

# Create your views here.
def index(request):
    ''' index Hello World
    '''
    return HttpResponse("Hello World")

def importcommon(request):
    str = test()
    return HttpResponse(str)


