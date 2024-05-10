from django.test import TestCase
from django.urls import reverse
from .models import Book, Review
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission   # new

class BookTests(TestCase):
    @ classmethod
    def setUpTestData(cls) -> None:
        cls.book = Book.objects.create(
            title = "Harry Potter",
            author = "JK Rowling",
            price = "25.00",
        )

        cls.special_permission = Permission.objects.get(
            codename = "special_status"
        )   # new

        cls.user = get_user_model().objects.create_user(
            username="reviewuser",
            email="reviewuser@email.com",
            password="testpass123",
        )

        cls.review = Review.objects.create(
            book=cls.book,
            author=cls.user,
            review="this is a test review",
        )
    
    def test_book_listing(self):
        self.assertEqual(self.book.title, "Harry Potter")
        self.assertEqual(self.book.author, "JK Rowling")
        self.assertEqual(self.book.price, "25.00")
    
    def test_book_list_view_for_logged_in_user(self):   # new
        self.client.login(email="reviewuser@email.com", password="testpass123")
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter")
        self.assertTemplateUsed(response, "books/book_list.html")

    def test_book_list_view_for_logged_out_user(self):  # new
        self.client.logout()
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "%s?next=/books/" % (reverse("account_login")))
        response = self.client.get(
            "%s?next=/books/" % (reverse("account_login")))
        self.assertContains(response, "Log In")

    def test_book_detail_view_with_permissions(self): # new
        self.client.login(email="reviewuser@email.com", password="testpass123")
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get("/books/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, "this is a test review")
        self.assertTemplateUsed(response, "books/book_detail.html")


    # def test_book_list_view(self):
    #     response = self.client.get(reverse("book_list"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Harry Potter")
    #     self.assertTemplateUsed(response, "books/book_list.html")

    # def test_book_detail_view(self):
    #     response = self.client.get(self.book.get_absolute_url())
    #     no_response = self.client.get("/books/12345/")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(no_response.status_code, 404)
    #     self.assertContains(response, "Harry Potter")
    #     self.assertTemplateUsed(response, "books/book_detail.html")
    #     self.assertContains(response, "this is a test review")      # new


        