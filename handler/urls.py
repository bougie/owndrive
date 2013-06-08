from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'handler.views.urls', name='handler_home'),
	url(r'^add/$', 'handler.views.add', name='handler_add'),
)
