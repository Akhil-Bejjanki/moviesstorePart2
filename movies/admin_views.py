from django.contrib import admin
from django.db.models import Count, Sum
from django.shortcuts import render
from .models import Movie

def top_movies(queryset, field):
    ranked = list(queryset.filter(**{field + '__gt' : 0}).order_by('-' + field, 'name'))
    if not ranked:
        return []
    top_value = getattr(ranked[0], field)
    return [movie for movie in ranked if (getattr(movie, field) == top_value)]

def movie_stats(request):
    bought = Movie.objects.annotate(times_bought = Sum('item__quantity', default = 0))
    reviewed = Movie.objects.annotate(times_reviewed=Count('review'))

    template_data = {}
    template_data['most_bought'] = top_movies(bought, 'times_bought')
    template_data['most_reviewed'] = top_movies(reviewed, 'times_reviewed')
    context = dict(admin.site.each_context(request), title = 'Movie Statistics', template_data = template_data)
    return render(request, 'admin/movie_stats.html', context)

