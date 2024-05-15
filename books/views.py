from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from .forms import ReviewForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin   # new
from .models import Book, Review
from django.db.models import Q  # new
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy

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

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            if request.user.has_perm('books.can_add_review'):
                review = form.save(commit=False)
                review.book = self.object
                review.author = self.request.user
                review.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                messages.error(request, 'You do not have permission to add a review. Upgrade your permissions to continue.')
                return HttpResponseRedirect(reverse('upgrade_to_premium') + f'?next={self.request.path}')

        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("book_detail", args=[str(self.object.id)])

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

class ReviewDeleteView(LoginRequiredMixin, View):
    def post(self, request, review_id):
        review = Review.objects.get(id=review_id)
        if request.user == review.author:
            review.delete()
        return HttpResponseRedirect(reverse('book_detail', args=[str(review.book_id)]))

