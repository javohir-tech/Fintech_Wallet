from django.urls import path
# ============== VIEWS ============
from .views import RegisterEmialorNumberView

urlpatterns = [
    path("singup/" , RegisterEmialorNumberView.as_view())    
]