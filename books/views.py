from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin   # new
from .models import Book
from django.db.models import Q  # new

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = "book_list"       # 指定在模板中使用的上下文变量的名称
    template_name = "books/book_list.html"
    login_url = "account_login"     # new

class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):  # new
    model = Book
    context_object_name = "book"
    template_name = "books/book_detail.html"
    login_url = "account_login"     # new   
    permission_required = "books.special_status"    # new
    queryset = Book.objects.all().prefetch_related("reviews__author")   # new
    # '__'表示查找

class SearchResultsListView(LoginRequiredMixin, ListView):  # new
    model = Book
    context_object_name = "book_list"
    template_name = "books/search_results.html"
    # queryset = Book.objects.filter(title__icontains="beginners")    # new

    def get_queryset(self):    # new
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

