from django.test import TestCase
from .models import Game, Event, KnownDistributor, Renter
from django.utils import timezone
from django.contrib.auth.models import User
# Create your tests here.


class EventModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.event = Event.objects.create(title='Event1', description='Description1')
        self.event.add_default_users()


    def test_event_creation(self):
        self.assertEqual(self.event.title, 'Event1')
        self.assertEqual(self.event.description, 'Description1')
        self.assertEqual(str(self.event), 'Event1')

    def test_event_users(self):
        self.assertEqual(self.event.allowed_users.count(), 2)
        self.assertTrue(self.event.allowed_users.filter(id=1).exists())
        self.assertTrue(self.event.allowed_users.filter(id=2).exists())

    def test_event_add_user(self):
        self.event.add_logged_in_user(self.user)
        self.assertEqual(self.event.allowed_users.count(), 3)
        self.assertTrue(self.event.allowed_users.filter(id=self.user.id).exists())


class GameModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.event = Event.objects.create(title='Event1', description='Description1')
        self.event.add_default_users()
        self.game = Game.objects.create(barcode='1234567890', title='Game1', distributor='Distributor1', event=self.event, quantity=10)


    def test_game_creation(self):
        self.assertEqual(self.game.barcode, '1234567890')
        self.assertEqual(self.game.title, 'Game1')
        self.assertEqual(self.game.distributor, 'Distributor1')
        self.assertEqual(self.game.event, self.event)
        self.assertEqual(self.game.quantity, 10)
        self.assertEqual(self.game.accessible, 10)
        self.assertEqual(self.game.avg_rating, 0)
        self.assertEqual(self.game.rating_count, 0)
        self.assertFalse(self.game.top)
    
    def test_game_rating(self):
        self.game.add_rating(5)
        self.assertEqual(self.game.avg_rating, 5)
        self.assertEqual(self.game.rating_count, 1)
        self.game.add_rating(3)
        self.assertEqual(self.game.avg_rating, 4)
        self.assertEqual(self.game.rating_count, 2)

    def test_game_renting_with_new_renter(self):
        RENTER_ID='123'
        self.game.add_renter('123')
        self.assertTrue(self.game.list_of_renters.filter(barcode=RENTER_ID).exists())
        self.assertEqual(self.game.accessible, 9)
        renter = Renter.objects.get(barcode=RENTER_ID)
        self.assertEqual(renter.how_many_games, 1)

    def test_game_renting_with_existing_renter(self):
        RENTER_ID='456'
        renter = Renter.objects.create(barcode=RENTER_ID)
        self.game.add_renter(RENTER_ID)
        self.assertTrue(self.game.list_of_renters.filter(barcode=RENTER_ID).exists())
        self.assertEqual(self.game.accessible, 9)
        renter = Renter.objects.get(barcode=RENTER_ID)
        self.assertEqual(renter.how_many_games, 1)
    
    def test_known_distributor(self):
        self.game.save()
        self.assertTrue(KnownDistributor.objects.filter(event=self.event, distributor='Distributor1').exists())