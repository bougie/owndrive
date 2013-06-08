from django import forms

class FileDescriptorForm(forms.Form):
	rawfile = forms.FileField()
