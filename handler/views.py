from django.shortcuts import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from handler.forms import FileDescriptorForm
from handler.models import FileDescriptor

@csrf_exempt
def add(request):
	if request.method == 'POST':
		form = FileDescriptorForm(request.POST, request.FILES)

		if form.is_valid():
			myfile = FileDescriptor(rawfile = request.FILES['rawfile'])
			myfile.save()

			ret = {}
		else:
			ret = {}
	else:
		ret = {}

	return HttpResponse(simplejson.dumps(ret), mimetype='application/json')

def urls(request):
	ret = {
		'index': reverse('handler_home'),
		'add': reverse('handler_add')
	}

	return HttpResponse(simplejson.dumps(ret), mimetype='application/json')
