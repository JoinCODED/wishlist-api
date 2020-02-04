from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date

from items.models import Item, FavoriteItem


class ItemListViewTest(APITestCase):
	def setUp(self):
		user = User.objects.create_user(username="laila", password="1234567890-=")
		self.item1 = {'image': 'foo.jpg', 'name': "yaaay", 'description': "yay object", 'added_by': user}
		self.item2 = {'image': 'foo.jpg', 'name':"booo" , 'description': "boo object", 'added_by': user}
		Item.objects.create(**self.item1)
		Item.objects.create(**self.item2)

	def test_url_works(self):
		response = self.client.get(reverse('api-list'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_list(self):
		response = self.client.get(reverse('api-list'))
		items = Item.objects.all()
		self.assertEqual(len(response.data), items.count())
		for index, item in enumerate(items):
			item = items[index]
			self.assertEqual(dict(response.data[index])['name'], item.name)

	def test_search(self):
		response = self.client.get(reverse('api-list'), {'search': 'y'})
		items = Item.objects.filter(name__icontains="y")
		self.assertEqual(len(response.data), items.count())
		for index, item in enumerate(items):
			item = items[index]
			self.assertEqual(dict(response.data[index])['name'], item.name)

	def test_ordering(self):
		response = self.client.get(reverse('api-list'), {'ordering': 'name'})
		items = Item.objects.order_by("name")
		self.assertEqual(len(response.data), items.count())
		for index, item in enumerate(items):
			item = items[index]
			self.assertEqual(dict(response.data[index])['name'], item.name)


	def test_details_url(self):
		response = self.client.get(reverse('api-list'))
		items = Item.objects.all()
		self.assertEqual(len(response.data), items.count())
		for index, item in enumerate(items):
			item = items[index]
			self.assertTrue(reverse('api-detail', args=[item.id]) in dict(response.data[index])['detail'])

	def test_user_serailized(self):
		response = self.client.get(reverse('api-list'))
		items = Item.objects.all()
		for index, item in enumerate(items):
			item = items[index]
			self.assertEqual(dict(response.data[index])['added_by'], {"first_name": item.added_by.first_name, "last_name": item.added_by.last_name})

	def test_favourited_field(self):
		response = self.client.get(reverse('api-list'))
		items = Item.objects.all()
		for index, item in enumerate(items):
			item = items[index]
			count = FavoriteItem.objects.filter(item=item).count()
			self.assertEqual(dict(response.data[index])['favourited'], count)


class ItemDetailViewTest(APITestCase):
	def setUp(self):
		user1 = User.objects.create_user(username="laila", password="1234567890-=")
		user2 = User.objects.create_user(username="laila2", password="1234567890-=")
		self.item1 = {'image': 'foo.jpg', 'name': "yaaay", 'description': "yay object", 'added_by': user1}
		self.item2 = {'image': 'foo.jpg', 'name':"booo" , 'description': "boo object", 'added_by': user2}
		Item.objects.create(**self.item1)
		Item.objects.create(**self.item2)


	def test_url_authorized(self):
		self.client.login(username="laila", password="1234567890-=")
		response = self.client.get(reverse('api-detail', args=[1]))
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_url_unauthorized(self):
		self.client.login(username="laila2", password="1234567890-=")
		response = self.client.get(reverse('api-detail', args=[1]))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


	def test_details(self):
		self.client.login(username="laila", password="1234567890-=")
		response = self.client.get(reverse('api-detail', args=[1]))
		self.assertEqual(dict(response.data)['name'], self.item1['name'])


	def test_users_sent(self):
		self.client.login(username="laila", password="1234567890-=")
		response = self.client.get(reverse('api-detail', args=[1]))
		people_count = FavoriteItem.objects.filter(item_id=1).count()
		self.assertEqual(len(dict(response.data)['favourited_by']), people_count)






