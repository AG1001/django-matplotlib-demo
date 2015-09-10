"""Views for the oil price prediction app."""

from django.shortcuts import render
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
import predict


def index(request):
  """Main page view."""
  context = {'region': 'WTI',
             'months': '3'}
  return render(request, 'forecast/main.html', context)


def plot_img(request, region, months):
  """View to return the image of the graph."""
  f = predict.Predict(region, int(months))
  canvas = FigureCanvasAgg(f)
  response = HttpResponse(content_type='image/png')
  canvas.print_png(response)
  return response


def forecast(request):
  """View called on forecast form submission."""
  region = request.POST['region']
  months = request.POST['months']
  context = {'region': region,
             'months': months,
             'plot_img': True}
  return render(request, 'forecast/main.html', context)
