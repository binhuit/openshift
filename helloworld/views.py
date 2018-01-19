from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
import mimetypes
import os
import glob
from . import huffman
from django.conf import settings
# Create your views here.


def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        files = glob.glob('media/compress/*')
        for f in files:
            os.remove(f)
        files = glob.glob('media/result/*')
        for f in files:
            os.remove(f)
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        f_path = os.path.join('compress',myfile.name)
        filename = fs.save(f_path, myfile)
        result_path = huffman.compress(os.path.join(settings.MEDIA_ROOT,f_path))
        result_fule = os.path.split(result_path)[-1]
        uploaded_file_url = fs.url(filename)
        return render(request, 'index.html', {
            'uploaded_file_url': result_fule
        })
    return render(request, 'index.html')

def download(request, file_name):
    file_path = settings.MEDIA_ROOT +'/result/'+ file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name) 
    return response