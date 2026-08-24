from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages

from tracker.forms import RegisterForm, ExpenseForm
from tracker.models import Expense, Category

class RegisterView(View):

    def get(self, request, *args, **kwargs):

        form = RegisterForm()

        return render(
            request,
            "tracker/register.html",
            {"form": form}
        )
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success( request,"Account created successfully! Please login." )
            return redirect("login")

        return render(
        request,
        "tracker/register.html",
        {"form": form}
    )

    
class DashboardView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        total_expenses = Expense.objects.filter(
            user=request.user
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0



        transaction_count = Expense.objects.filter(
            user=request.user
        ).count()

        today = timezone.localdate()

        this_month_expenses = Expense.objects.filter(
            user=request.user,
            date__year=today.year,
            date__month=today.month
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0


        recent_expenses = Expense.objects.filter(
            user=request.user
        ).order_by(
            "-date",
            "-id"
        )[:5]


    
        category_expenses = (
            Expense.objects
            .filter(user=request.user)
            .values("category__name")
            .annotate(
                total=Sum("amount")
            )
            .order_by("-total")
        )

        context = {
            "total_expenses": total_expenses,
            "transaction_count": transaction_count,
            "this_month_expenses": this_month_expenses,
            "recent_expenses": recent_expenses,
            "category_expenses": category_expenses,

        }


        return render(
            request,
            "tracker/dashboard.html",
            context
        )


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = "tracker/expense_list.html"
    context_object_name = "expenses"
    paginate_by = 5


    def get_queryset(self):

        expenses = Expense.objects.filter(
            user=self.request.user
        ).order_by("-date")


        search = self.request.GET.get("search")

        if search:
            expenses = expenses.filter(
                title__icontains=search
            )

        category = self.request.GET.get("category")

        if category:

            expenses = expenses.filter(
                category_id=category
            )
        start_date = self.request.GET.get("start_date")

        if start_date:
            expenses = expenses.filter(
                date__gte=start_date
            )

        end_date = self.request.GET.get("end_date")


        if end_date:
            expenses = expenses.filter(
                date__lte=end_date
            )

        return expenses

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context



class ExpenseCreateView(LoginRequiredMixin, CreateView):

    model = Expense
    form_class = ExpenseForm
    template_name = "tracker/expense_form.html"
    success_url = reverse_lazy("expense-list")

    def form_valid(self, form):

        form.instance.user = self.request.user
        return super().form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):

    model = Expense
    form_class = ExpenseForm
    template_name = "tracker/expense_form.html"
    success_url = reverse_lazy("expense-list")

    def get_queryset(self):
        return Expense.objects.filter(
            user=self.request.user
        )

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
     model = Expense
     template_name = "tracker/expense_confirm_delete.html"
     success_url = reverse_lazy("expense-list")


     def get_queryset(self):
        return Expense.objects.filter(
            user=self.request.user
        )