from django import forms

class FileDescriptorForm(forms.Form):
	file = forms.FileField()
	description = forms.CharField(required=False)
	tag = forms.CharField(required=False)
