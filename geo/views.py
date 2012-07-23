from django.http import HttpResponse
from django.utils import simplejson
from geo.models import Country, Street, City, Region

def autocomplete_countries(request):
    query = request.GET['query']
    countries = Country.objects.filter(name__startswith=query)
    return HttpResponse(simplejson.dumps([c.name for c in countries]))

def autocomplete_regions(request):
    query = request.GET['query']
    country = request.GET['country']
    regions = Region.objects.filter(name__startswith=query)
    if country:
        regions = regions.filter(country__name=country)
    return HttpResponse(simplejson.dumps([r.name for r in regions]))

def autocomplete_cities(request):
    query = request.GET['query']
    country = request.GET['country']
    region = request.GET['region']
    cities = City.objects.filter(name__startswith=query)
    if country:
        cities = cities.filter(region__country__name=country)
    if region:
        cities = cities.filter(region__name=region)
    return HttpResponse(simplejson.dumps([c.name for c in cities]))

def autocomplete_streets(request):
    query = request.GET['query']
    country = request.GET['country']
    region = request.GET['region']
    city = request.GET['city']
    streets = Street.objects.filter(name__startswith=query)
    if country:
        streets = streets.filter(city__region__country__name=country)
    if region:
        streets = streets.filter(city__region__name=region)
    if city:
        streets = streets.filter(city__name=region)
    return HttpResponse(simplejson.dumps([s.name for s in streets]))
