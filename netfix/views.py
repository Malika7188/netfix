from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import User, Company, Customer
from services.models import Service, RequestedService


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


@login_required
def customer_profile(request, name):
    # Fetch the customer user and all their requested services
    user = get_object_or_404(User, username=name)
    customer = get_object_or_404(Customer, user=user)
    requested_services = RequestedService.objects.filter(
        customer=customer).order_by("-date_requested")
    
    return render(request, 'users/customer_profile.html', {
        'user': user,
        'requested_services': requested_services
    })


@login_required
def company_profile(request, name):
    # Fetch the company user and all of their services
    user = get_object_or_404(User, username=name)
    company = get_object_or_404(Company, user=user)
    services = Service.objects.filter(
        company=company).order_by("-date")
    
    return render(request, 'users/company_profile.html', {
        'user': user,
        'company': company,
        'services': services
    })