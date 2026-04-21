from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def home(request):
    return JsonResponse({'message': 'API Django funcionando'})

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
]
