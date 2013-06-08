from django.db import models

class FileDescriptor(models.Model):
	rawfile = models.FileField(upload_to='%Y/%m/%d')
