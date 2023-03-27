from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from pandas import read_excel, read_csv
from .models import UploadedFile

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'open_link', 'download_link')
    
    def open_link(self, obj):
        return format_html('<a href="{}" target="_blank">Open</a>', reverse('open_file', args=[obj.id]))
    open_link.short_description = ''
    
    def download_link(self, obj):
        return format_html('<a href="{}">Download</a>', obj.file.url)
    download_link.short_description = ''
    
    def render_table(self, queryset):
        # Read the file data and convert to a pandas dataframe
        if queryset.file_type == 'Excel':
            df = read_excel(queryset.file)
        elif queryset.file_type == 'CSV':
            df = read_csv(queryset.file)
        else:
            return "Unsupported file type"
        
        # Render the dataframe as an HTML table
        return format_html(df.to_html())
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Get the UploadedFile object
        obj = self.get_object(request, object_id)
        if not obj:
            return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

        # Set the page title and add the rendered table to the context
        extra_context = extra_context or {}
        extra_context['title'] = obj.name
        extra_context['table'] = self.render_table(obj)

        # Render the change form template
        return self.render_change_form(request, self.get_object(request, object_id), form_url=form_url, extra_context=extra_context)
    
admin.site.register(UploadedFile, UploadedFileAdmin)
