from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
#now import the views.py file into this code

from . import views

urlpatterns=[
    path('', views.Dashboard, name='dashboard'),
    path('encrypt/', views.Encrypt, name='encrypt'),
    path('decrypt/', views.Decrypt, name='decrypt'),
    path('manage/', views.Manage, name='manage'),
    path('test/', views.Test, name='test'),
    path('manage/<slug:slug>', views.ManageFile, name='manage-file'),
    path('delete/<slug:slug>', views.DeleteFile, name='delete-file'),
    path('download/<slug:slug>', views.DownloadFile, name='download-file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)