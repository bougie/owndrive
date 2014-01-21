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
				myfile = FileDescriptor()

				myfile.path = request.FILES['file']
				myfile.description = form.cleaned_data['description']
				myfile.tag = form.cleaned_data['tag']

				myfile.save()

				ret = {
					'filename': myfile.path.name,
					'url': myfile.path.url
				}
			except Exception, e:
				ret = {'error': str(e)}
		else:
			ret = {'error': 'Form is incorrect'}
	else:
		ret = {'error': 'Unsupported method'}

	return HttpResponse(simplejson.dumps(ret), mimetype='application/json')
