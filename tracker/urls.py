
from django.urls import path

from tracker.views import (
    RegisterView,
    DashboardView,
    ExpenseListView,
    ExpenseCreateView,
    ExpenseUpdateView,
    ExpenseDeleteView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name= "register") ,
    path("", DashboardView.as_view(), name="dashboard"),

    path("expenses/",ExpenseListView.as_view(),
        name="expense-list"
    ),

    path("expenses/add/", ExpenseCreateView.as_view(),
        name="expense-create"
    ),

    path("expenses/<int:pk>/edit/", ExpenseUpdateView.as_view(),
        name="expense-update"
    ),

    path( "expenses/<int:pk>/delete/", ExpenseDeleteView.as_view(),
        name="expense-delete"
    ),
]

    





