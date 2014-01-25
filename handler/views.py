from django.shortcuts import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PIL import Image
import os

from handler.forms import FileDescriptorForm
from handler.models import FileDescriptor

@csrf_exempt
def index(request):
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		form = FileDescriptorForm(request.POST, request.FILES)

		if form.is_valid():
			try:
				myfile = FileDescriptor()

				myfile.path = request.FILES['file']
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

					thumb_w, thumb_h = settings.THUMB_SIZE

					# Image path with path relative to the MEDIA_ROOT directory
					imgpath = myfile.path.name

					# Generate thumbnail path
					# Add _min before the file extension
					thumbpath = imgpath.split('.')
					thumbpath_len = len(thumbpath) - 1
					if thumbpath_len == 1:
						thumbpath = str(thumbpath[0]) + '_min.' + str(thumbpath[thumbpath_len])
					else:
						thumbpath = str(thumbpath[0:thumbpath_len - 1]) + '_min.' + str(thumbpath[thumbpath_len])

					# Convert to RGB if necessary
					image = Image.open(os.path.join(settings.MEDIA_ROOT, imgpath))
					if image.mode not in ['L', 'RGB']:
						image.convert('RGB')

					# Define thumbnail size
					if thumb_w == thumb_h:
						xsize, ysize = image.size
						minsize = min(xsize, ysize)

						xnewsize = (xsize - minsize) / 2
						ynewsize = (ysize - minsize) / 2

						image2 = image.crop((xnewsize, ynewsize, xsize-xnewsize, ysize-ynewsize))
						image2.load()
						image2.thumbnail(settings.THUMB_SIZE, Image.ANTIALIAS)
					else:
						image2 = image
						image2.thumbnail(setting.THUMB_SIzE, Image.ANTIALIAS)
					
					format = myfile.type.split('/')[1]
					image2.save(os.path.join(settings.MEDIA_ROOT, thumbpath), format)

					myfile.thumbnail = thumbpath
					myfile.save()

					ret = {
						'filename': fname,
						'thumbnail': thumbpath,
						'url': imgpath
					}
				else:
					return {'error': 'format %s of file is not allowed' % (myfile.type)}
			except Exception, e:
				ret = {'error': str(e)}
		else:
			ret = {'error': 'Form is incorrect'}
	else:
		ret = {'error': 'Unsupported method'}

	return HttpResponse(simplejson.dumps(ret), mimetype='application/json')
