from django.db import models

class FileDescriptor(models.Model):
	path = models.FileField(upload_to='%Y/%m/%d')
	description = models.CharField(max_length=255, blank=True, null=True)
	tag = models.CharField(max_length=255, blank=True, null=True)
	type = models.CharField(max_length=30, blank=True, null=True)
