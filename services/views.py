from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from users.models import Company, Customer, User

from .models import Service, RequestedService
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    # Get sort parameter from URL, default to "-date"
    sort_by = request.GET.get('sort', '-date')
    
    # Define allowed sort fields
    allowed_sort_fields = {
        'date': '-date',
        'price': 'price_hour',
        'price-desc': '-price_hour',
        'name': 'name',
        'name-desc': '-name'
    }
    
    # Use the requested sort field if valid, otherwise default to "-date"
    sort_field = allowed_sort_fields.get(sort_by, '-date')
    
    services = Service.objects.all().order_by(sort_field)
    return render(request, 'services/list.html', {
        'services': services,
        'current_sort': sort_by
    })


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


@login_required
def create(request):
    if not request.user.is_company:
        return redirect('/')
    
    company = Company.objects.get(user=request.user)
    choices = [(company.field, company.field)]
    if company.field == 'All in One':
        choices = Service.choices
    
    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=choices)
        if form.is_valid():
            service = Service.objects.create(
                company=company,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_hour=form.cleaned_data['price_hour'],
                field=form.cleaned_data['field']
            )
            return redirect(f'/services/{service.id}')
    else:
        form = CreateNewService(choices=choices)
    
    return render(request, 'services/create.html', {'form': form})


def service_field(request, field):
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


@login_required
def request_service(request, id):
    if not request.user.is_customer:
        return redirect('/')
    
    service = Service.objects.get(id=id)
    customer = Customer.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            requested_service = RequestedService.objects.create(
                customer=customer,
                service=service,
                address=form.cleaned_data['address'],
                hours=form.cleaned_data['hours']
            )
            return redirect(f'/customer/{request.user.username}')
    else:
        form = RequestServiceForm()
    
    return render(request, 'services/request_service.html', {'form': form, 'service': service})


def most_requested_services(request):
    # Get services ordered by number of requests
    services = Service.objects.annotate(
        request_count=Count('requestedservice')
    ).order_by('-request_count')[:10]  # Get top 10 most requested services
    return render(request, 'services/most_requested.html', {'services': services})