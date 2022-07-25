from copy import deepcopy
from random import sample

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from tours.data import departures, description, subtitle, title, tours


def main_view(request: WSGIRequest) -> HttpResponse:
    tours_copy_main = deepcopy(tours)
    for key, value in tours_copy_main.items():
        value['id'] = key
    random = sample(range(1, (len(tours))+1), 6)
    context = {'title': title, 'subtitle': subtitle, 'description': description, 'current_tours': []}
    for num in random:
        context['current_tours'].append(tours_copy_main[num])
    return render(request, 'index.html', context=context)


def departure_view(request: WSGIRequest, departure: str) -> HttpResponse:
    tours_copy_test = deepcopy(tours)
    context = {'current_tours': [], 'tours_prices': [], 'tours_nights': []}
    for tour_id, tour in tours_copy_test.items():
        tour['id'] = tour_id
        if tour['departure'] == departure:
            context['current_tours'].append(tours_copy_test[tour_id])
            context['tours_prices'].append(tour['price'])
            context['tours_nights'].append(tour['nights'])
    context['current_departure'] = departures[departure]
    context['tours_prices'].sort()
    context['tours_nights'].sort()
    return render(request, 'departure.html', context=context)


def tour_view(request: WSGIRequest, id: int) -> HttpResponse:
    tours_copy_tour = deepcopy(tours)
    for key, value in tours_copy_tour.items():
        value['id'] = key
    context = tours_copy_tour[id]
    context['departure_localized'] = departures[context['departure']]
    context['draw_stars'] = int(context['stars']) * '★'
    return render(request, 'tour.html', context=context)


def custom_handler404(request: WSGIRequest, exception) -> HttpResponse:
    return render(request, '404.html', status=400)


def custom_handler500(request: WSGIRequest) -> HttpResponse:
    return render(request, '500.html', status=500)
