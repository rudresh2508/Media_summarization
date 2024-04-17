# summarizer/urls.py
from base64 import urlsafe_b64decode
from django.urls import path
from .views import SummarizerView
from . import views


urlpatterns = [
    path('summarizer/upload/', views.SummarizerView.as_view(), name='upload_summary'),
    path('summarizer/summary/', views.summary_page, name='summary_page'),  # Add this line
    # Add more URL patterns as needed
]




