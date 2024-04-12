from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    def get_uploaded_documents(self):
        return self.get_uploaded_documents

class PDFDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    title = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to='pdf_documents/')
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

   
