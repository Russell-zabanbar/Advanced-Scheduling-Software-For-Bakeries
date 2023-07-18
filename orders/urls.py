from django.urls import path
from orders import views

urlpatterns = [
    path('baker/', views.CreateOrderApiView.as_view()),
    # path('all_orders/', views.SendAllStore.as_view()),

]
