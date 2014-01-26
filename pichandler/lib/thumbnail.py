# -*- coding: utf8 -*

import os

from PIL import Image

#
# Generate a thumbnail with the size given by size
# for the picture given by base.
# Save it in the same directory of base
#
def generate(base, size, rootdir):
	thumb_w, thumb_h = size

	imgpath = base.path.name

	# Generate thumbnail path
	# Add _min before the file extension
	thumbpath = imgpath.split('.')
	thumbpath_len = len(thumbpath) - 1
	if thumbpath_len == 1:
		thumbpath = str(thumbpath[0]) + '_min.' + str(thumbpath[thumbpath_len])
	else:
		thumbpath = str(thumbpath[0:thumbpath_len - 1]) + '_min.' + str(thumbpath[thumbpath_len])

	# Convert to RGB if necessary
	image = Image.open(os.path.join(rootdir, imgpath))
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
		image2.thumbnail(size, Image.ANTIALIAS)
	else:
		image2 = image
		image2.thumbnail(size, Image.ANTIALIAS)

	format = base.type.split('/')[1]
	image2.save(os.path.join(rootdir, thumbpath), format)

	return thumbpath
