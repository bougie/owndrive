SITE_NAME = ""

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': 'db.sqlite',
		'USER': '',
		'PASSWORD': '',
		'PORT': '',
	}
}

import os
MEDIA_ROOT = os.path.join(os.getcwd(), 'media')
MEDIA_URL = '/media/'

THUMB_SIZE = (125, 125)
