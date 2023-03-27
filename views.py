from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import FileUploadForm
from .models import UploadedFile
import pandas as pd

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # after validating the file access the uploaded file
            file = form.cleaned_data['file']
            uploaded_file = UploadedFile(file=file)
            uploaded_file.save()
            # returns the url of success
            success_url = reverse('success')
            return redirect(success_url)
        else:
            form.add_error('file',"")
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

def success(request):
    uploaded_file = UploadedFile.objects.all()
    context = {'uploaded_files': uploaded_file}
    print(uploaded_file)
    return render(request, 'success.html',context)

def download_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(pk=file_id)
    file_path = uploaded_file.file.path
    with open(file_path,'rb') as file:
        response = HttpResponse(file.read(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' + uploaded_file.file.name.split('/')[-1]
        return response

def open_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    file_extension = uploaded_file.file.name.split('.')[-1]
    if file_extension == 'csv':
        data = pd.read_csv(uploaded_file.file)
    elif file_extension == 'xlsx':
        data = pd.read_excel(uploaded_file.file)

    html = data.to_html()

    return HttpResponse(html)