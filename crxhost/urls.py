from django.conf.urls import patterns, url

urlpatterns = patterns('crxhost.views',
    url(r'^download/(?P<crxname>[^/]+)/(?P<version>.+)', 'download', {}, 'crx_download'),
    url(r'^updates.xml$', 'updates_xml', {}, 'crx_updates_xml')
)