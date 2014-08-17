from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from dynamic_model_classes.views import home, model_content_view, sync

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^model/(?P<model_name>[^/]+)/$', model_content_view, name = 'by_model'),
    #url(r'^(?P<model>[^/]+)/(?P<obj>)/$', 'dynamic_model_classes.views.model_content_view', name = 'by_object'),
    url(r'^model/(?P<model_name>[^/]+)/update/$', sync, name='model_update'),
    )

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^favicon\.ico$', 'redirect_to', {'url': '/media/img/favicon.png'}),


)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r"^media/(.+)", static.serve, {"document_root": settings.MEDIA_ROOT}),
                            )


