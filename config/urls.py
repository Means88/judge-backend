"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from django.conf import settings
from problem.api import ProblemViewSet
import django.views.static

from submission.api import SubmissionViewSet

router = routers.DefaultRouter()
router.register('problem', ProblemViewSet)
router.register('submission', SubmissionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    re_path('^$', django.views.static.serve, {
        'path': 'index.html',
        'document_root': settings.REACT_BUILD_DIR,
    }),
]

ROOT_FILES = (
    'index.html',
    'manifest.json',
    'asset-manifest.json',
    'favicon.ico',
    'service-worker.js',
)

urlpatterns += map(lambda f: path(f, django.views.static.serve, {
    'path': f,
    'document_root': settings.REACT_BUILD_DIR,
}), ROOT_FILES)

if settings.DEBUG:
    urlpatterns += [
        path('media/<path:path>', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
        re_path('(static/)?<path:path>', django.views.static.serve, {'document_root': settings.REACT_BUILD_STATIC_DIR}),
    ]
