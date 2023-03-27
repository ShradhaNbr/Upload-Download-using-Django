from django import forms
from .models import UploadedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('file',)
    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith(('.csv', '.xlsx')):
            raise forms.ValidationError("Only CSV or XLSX file types are allowed.")
        return file