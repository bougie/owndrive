from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'handler.views.index', name='handler_file'),
)
