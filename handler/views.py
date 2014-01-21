from django.shortcuts import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from handler.forms import FileDescriptorForm
from handler.models import FileDescriptor

@csrf_exempt
def index(request):
	if request.method == 'POST':
		form = FileDescriptorForm(request.POST, request.FILES)

		if form.is_valid():
			try:
				myfile = FileDescriptor(rawfile = request.FILES['rawfile'])
				myfile.save()

				ret = {}
			except Exception, e:
				print str(e)

				ret = {}
		else:
			ret = {}
	else:
		ret = {}

	return HttpResponse(simplejson.dumps(ret), mimetype='application/json')
