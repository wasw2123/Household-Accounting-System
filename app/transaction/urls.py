from django.urls import path

from .views import TransactionDetailView, TransactionListView

urlpatterns = [
    path("transaction/", TransactionListView.as_view(), name="transaction_list"),
    path("transaction/<int:pk>/", TransactionDetailView.as_view(), name="transaction_detail"),
]
