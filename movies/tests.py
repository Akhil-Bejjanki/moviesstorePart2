from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from cart.models import Order, Item
from .models import Movie, Review

class MovieStatsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', password = 'pass12345')
        self.admin = User.objects.create_superuser('admin', password = 'pass12345')
        self.movie_a = Movie.objects.create(name = 'Inception', price = 10, description='a', image='a.jpg')
        self.movie_b = Movie.objects.create(name = 'Avatar', price = 12, description='b', image='b.jpg')
    def purchase(self, movie, quantity):
        order = Order.objects.create(total=movie.price * quantity, user = self.user)
        Item.objects.create(price = movie.price, quantity = quantity, order = order, movie = movie)
    def get_stats(self):
        self.client.force_login(self.admin)
        return self.client.get(reverse('admin.movie_stats'))
    def test_requires_staff(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('admin.movie_stats'))
        self.assertEqual(response.status_code, 302)
    def test_same_movie_shows_in_both(self):
        Review.objects.create(comment = 'Great', movie=self.movie_a, user = self.user)
        self.purchase(self.movie_a, 1)
        data = self.get_stats().context['template_data']
        self.assertEqual(data['most_bought'], [self.movie_a])
        self.assertEqual(data['most_reviewed'], [self.movie_a])
    def test_different_movies_after_buying_another_twice(self):
        Review.objects.create(comment = 'Great', movie=self.movie_a, user = self.user)
        self.purchase(self.movie_a, 1)
        self.purchase(self.movie_b, 2)
        data = self.get_stats().context['template_data']
        self.assertEqual(data['most_bought'], [self.movie_b])
        self.assertEqual(data['most_reviewed'], [self.movie_a])
    
    def test_reviews_do_not_inflate_purchase_count(self):
        for comment in ['one', 'two', 'three']:
            Review.objects.create(comment=comment, movie=self.movie_a, user=self.user)
        self.purchase(self.movie_a, 1)
        data = self.get_stats().context['template_data']
        self.assertEqual(data['most_bought'][0].times_bought, 1)
        self.assertEqual(data['most_reviewed'][0].times_reviewed, 3)
        