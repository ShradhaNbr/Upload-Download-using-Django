from django.db import models

class UploadedFile(models.Model):
    # id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.file)