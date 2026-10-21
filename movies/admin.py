from django.contrib import admin
from django.db.models import Count
from django.shortcuts import render
from .models import Movie, Review, TopReviewer, MovieStats
from .admin_views import movie_stats
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class TopReviewerAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_content = None):
        top_user = (Review.objects.values('user__username')
                    .annotate(total_reviews = Count('id'))
                    .order_by('-total_reviews')
                    .first())
        
        context = {**self.admin_site.each_context(request), 'title': 'Top_Reviewer', 'top_user': top_user,}
        return render(request, 'admin/top_reviewer.html', context)


class MovieStatsAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context = None):
        return movie_stats(request)

    def has_add_permission(self, request):
        return False


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(TopReviewer, TopReviewerAdmin)
admin.site.register(MovieStats, MovieStatsAdmin)
