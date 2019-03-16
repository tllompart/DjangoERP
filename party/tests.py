from django.test import TestCase

# Create your tests here.


class TestPage(TestCase):
    def test_party_page(self):
        response = self.client.get('/party.html')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'party.html')
        self.assertContains(response, 'Party setup')
