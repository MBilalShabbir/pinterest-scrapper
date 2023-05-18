from django.urls import path
from .views import ScrappingView, SeleniumScrappingView

urlpatterns = [
    # Organization CRUD urls
    path("scrap/", ScrappingView.as_view(), name="scrap"),
    path("scrap/selenium/", SeleniumScrappingView.as_view(), name="scrap_selenium")
]
