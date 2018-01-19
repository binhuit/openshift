from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
import mimetypes
import os
import glob
# Create your views here.


def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        files = glob.glob('media/compress/*')
        for f in files:
            os.remove(f)
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(os.path.join('compress',myfile.name), myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'index.html', {
            'uploaded_file_url': myfile.name
        })
    return render(request, 'index.html')

def download(request, file_name):
    file_path = settings.MEDIA_ROOT +'/compress/'+ file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name) 
    return response