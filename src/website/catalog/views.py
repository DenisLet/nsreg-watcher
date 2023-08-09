from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.db.models import Q

from .models import Registrator
from .forms import CompaniesSortForm


SORT_FIELD_NAMES = {
    'CN': 'name',
    'CI': 'city',
    'RE': 'pricereg',
    'PR': 'priceprolong',
    'PE': 'pricechange',

}


def registrator_list(request):
    if request.method == "POST":
        form = CompaniesSortForm(request.POST)
        if form.is_valid():
            sort_by = SORT_FIELD_NAMES.get(
                form.cleaned_data['sort_by'], 'name')
            search = form.cleaned_data['search']
            companies = Registrator.objects.order_by(sort_by)

    else:
        form = CompaniesSortForm()
        sort_by = 'name'
        search = ''

    if search:
        companies = Registrator.objects.filter(Q(name__contains=search) | Q(
            city__contains=search) | Q(pricereg__contains=search)).order_by(sort_by)
    else:
        companies = Registrator.objects.order_by(sort_by)
    return render(request, 'registrator-list.html', {'companies': companies, 'form': form})


def registrator_details(request, id):
    try:
        company = Registrator.objects.get(id=id)
    except Registrator.DoesNotExist:
        return HttpResponseNotFound(f"Компания с идентификатором {id} в базе не найдена.")
    return render(request, 'registrator-details.html', {'company': company})


def about(request):
    return render(request, 'about-us.html', )
