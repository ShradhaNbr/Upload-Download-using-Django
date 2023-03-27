from django.urls import path
from .views import upload_file,success, download_file, open_file
from django.conf.urls.static import static
from django.conf import settings


app_name = 'fileupload'
urlpatterns = [
    path('', upload_file, name='upload'),
    path('success/',success, name='success'),
    path('download_file/<int:file_id>/', download_file, name='download_file'),
    path('open_file/<int:file_id>/', open_file, name='open_file')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
