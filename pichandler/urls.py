from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'pichandler.views.index', name='handler_picture'),
)
