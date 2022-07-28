from random import sample

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from tours.data import departures, description, subtitle, title, tours


def main_view(request: WSGIRequest) -> HttpResponse:
    random_tours_id = sample(range(1, (len(tours))+1), 6)
    context = {'title': title, 'subtitle': subtitle, 'description': description, 'current_tours': {}}
    for tour_id in random_tours_id:
        context['current_tours'][tour_id] = tours[tour_id]
    return render(request, 'index.html', context=context)


def departure_view(request: WSGIRequest, departure: str) -> HttpResponse:
    context = {'current_tours': {}, 'tours_prices': [], 'tours_nights': []}
    for tour_id, tour in tours.items():
        if tour['departure'] == departure:
            context['current_tours'][tour_id] = tours[tour_id]
            context['tours_prices'].append(tour['price'])
            context['tours_nights'].append(tour['nights'])
    context['current_departure'] = departures[departure]
    context['tours_prices'].sort()  # Такой подход был выбран из-за того, что в DTL нет min, max.
    context['tours_nights'].sort()  # Поэтому заводится список, который сортируется и из него достаются |first и |last.
    return render(request, 'departure.html', context=context)


def tour_view(request: WSGIRequest, tour_id: int) -> HttpResponse:
    context = tours[tour_id]
    context['departure_localized'] = departures[context['departure']]
    context['draw_stars'] = int(context['stars']) * '★'
    return render(request, 'tour.html', context=context)


def custom_handler404(request: WSGIRequest, exception) -> HttpResponse:
    return render(request, '404.html', status=400)


def custom_handler500(request: WSGIRequest) -> HttpResponse:
    return render(request, '500.html', status=500)
