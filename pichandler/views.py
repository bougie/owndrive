# -*- coding: utf8 -*

from django.shortcuts import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pichandler.forms import FileDescriptorForm
from pichandler.models import FileDescriptor
from pichandler.lib.thumbnail import generate

@csrf_exempt
def index(request):
	if request.method == 'GET':
		_pictures = FileDescriptor.objects.all()
		
		pictures = []
		for pict in _pictures:
			pictures.append({
				'name': pict.name,
				'description': pict.description,
				'tag': pict.tag,
				'image': pict.path.name,
				'thumbnail': pict.thumbnail
			})

		ret = {'content': pictures} 

	elif request.method == 'POST':
		form = FileDescriptorForm(request.POST, request.FILES)

		if form.is_valid():
			try:
				myfile = FileDescriptor()

				myfile.path = request.FILES['file']
				myfile.name = myfile.path.name
				myfile.type = request.FILES['file'].content_type
				myfile.description = form.cleaned_data['description']
				myfile.tag = form.cleaned_data['tag']

				# Image filename without any path
				fname = myfile.path.name

				# Check if file type upload is allowed
				# Typically, upload only image file
				allowed_mime = set(['image/jpeg', 'image/png', 'image/gif'])
				if myfile.type in allowed_mime:
					myfile.save()

					thumbpath = generate(
						base=myfile,
						size=settings.THUMB_SIZE,
						rootdir=settings.MEDIA_ROOT)

					myfile.thumbnail = thumbpath
					myfile.save()

					ret = {
						'filename': fname,
						'thumbnail': thumbpath,
						'url': myfile.path.name
					}
				else:
					return {'error': 'format %s of file is not allowed' % (myfile.type)}
			except Exception, e:
				myfile.delete()
				ret = {'error': str(e)}
		else:
			ret = {'error': 'Form is incorrect'}
	else:
		ret = {'error': 'Unsupported method'}

	return HttpResponse(simplejson.dumps(ret), mimetype='application/json')
