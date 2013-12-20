from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'dynamic_model_classes.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    (r"^media/(.+)", static.serve, {"document_root": settings.MEDIA_ROOT}),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )