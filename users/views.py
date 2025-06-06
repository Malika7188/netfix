from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer
from services.models import RequestedService


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'users/register.html')


class AnonymousUserMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('/')


class CustomerSignUpView(AnonymousUserMixin, CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class CompanySignUpView(AnonymousUserMixin, CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def LoginUserView(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    login(request, user)
                    return redirect('/')
                else:
                    form.add_error(None, 'Invalid email or password')
            except User.DoesNotExist:
                form.add_error(None, 'Invalid email or password')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def company_requested_services(request):
    if not request.user.is_company:
        return redirect('/')
        
    company = request.user.company
    requested_services = RequestedService.objects.filter(
        service__company=company
    ).order_by('-date_requested')
    
    return render(request, 'users/company_requested_services.html', {
        'requested_services': requested_services
    })
