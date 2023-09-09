from django.urls import path
from .views import CreateAdvisor, CreateClient, AdvisorClientView, AddProducts, PurchaseProduct

urlpatterns = [
    path('create-advisor', CreateAdvisor.as_view()),
    path('create-client', CreateClient.as_view()),
    path('advisor-client-view', AdvisorClientView.as_view()),
    path('add-product', AddProducts.as_view()),
    path('purchase-product', PurchaseProduct.as_view()),
]