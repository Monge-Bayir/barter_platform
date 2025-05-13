from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Ad, ExchangeProposal

class AdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='testpass')

    def test_create_ad(self):
        ad = Ad.objects.create(
            user=self.user,
            title="Test Ad",
            description="Some description",
            category="Books",
            condition="new"
        )
        self.assertEqual(str(ad), "Test Ad")
        self.assertEqual(ad.condition, "new")

class ExchangeProposalModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.ad1 = Ad.objects.create(user=self.user1, title="Ad 1", description="desc", category="Cat", condition="new")
        self.ad2 = Ad.objects.create(user=self.user2, title="Ad 2", description="desc", category="Cat", condition="used")

    def test_create_exchange_proposal(self):
        proposal = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2, comment="Want to exchange")
        self.assertEqual(proposal.status, "pending")
        self.assertEqual(str(proposal), "Ad 1 → Ad 2 [pending]")

class AdViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='testpass')
        self.ad = Ad.objects.create(user=self.user, title="Test Ad", description="desc", category="Electronics", condition="new")

    def test_list_ads_view(self):
        response = self.client.get(reverse('ads:list_ads'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Ad")

    def test_ad_detail_view(self):
        response = self.client.get(reverse('ads:ad_detail', args=[self.ad.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ad.title)

    def test_create_ad_view_authenticated(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.post(reverse('ads:create_ad'), {
            'title': 'New Ad',
            'description': 'Desc',
            'category': 'Books',
            'condition': 'used',
        })
        self.assertEqual(response.status_code, 302)  # redirect

    def test_edit_ad_view(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.post(reverse('ads:edit_ad', args=[self.ad.pk]), {
            'title': 'Updated Title',
            'description': self.ad.description,
            'category': self.ad.category,
            'condition': self.ad.condition
        })
        self.assertEqual(response.status_code, 302)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Updated Title')

    def test_delete_ad_view(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.post(reverse('ads:delete_ad', args=[self.ad.pk]))
        self.assertRedirects(response, reverse('ads:list_ads'))
        self.assertFalse(Ad.objects.filter(pk=self.ad.pk).exists())

class ExchangeProposalViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.ad_sender = Ad.objects.create(user=self.user1, title="Sender Ad", description="desc", category="A", condition="new")
        self.ad_receiver = Ad.objects.create(user=self.user2, title="Receiver Ad", description="desc", category="B", condition="used")

    def test_create_proposal(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.post(reverse('ads:create_proposal', args=[self.ad_receiver.pk]), {
            'comment': 'Let\'s exchange'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_proposals_list(self):
        ExchangeProposal.objects.create(ad_sender=self.ad_sender, ad_receiver=self.ad_receiver)
        self.client.login(username='user1', password='testpass')
        response = self.client.get(reverse('ads:proposals_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Receiver Ad")