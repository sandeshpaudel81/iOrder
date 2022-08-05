from unicodedata import name
from django.urls import path
from iOrder import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),

    path('menu/', views.getMenu, name="get-menu"),
    path('create-order/<str:qr>/', views.createOrderWithQR, name="create-order-with-qr"),
    path('confirm-order/<str:code>/', views.addOrderItems, name="add-order-items"),
    path('order/<str:code>/', views.getOrderItems, name="get-order-items"),
    path('admin/orders/', views.getAllOrdersForAdmin, name="admin-all-orders"),

]