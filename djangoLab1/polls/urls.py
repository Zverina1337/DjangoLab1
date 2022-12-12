from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index, DetailView, ResultsView, vote, IndexView

urlpatterns = [
    path('',index, name='home'),
    path('<int:pk>/', DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', vote, name='vote'),
    path('index/', IndexView.as_view(), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)