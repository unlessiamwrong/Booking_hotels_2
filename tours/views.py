from django.shortcuts import render


def main_view(request):
    return render(request, 'index.html')


def departure_view(request, departure):
    return render(request, 'departure.html')


def tour_view(request, id):
    return render(request, 'tour.html')


def custom_handler404(request, exception):
    return render(request, '404.html', status=400)


def custom_handler500(request):
    return render(request, '500.html', status=500)
