from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from books.models import AdminBook
from common.forms import CommentForm


def home_page(request):
    monthly_books = AdminBook.get_monthly_books()
    context = {'monthly_books': monthly_books}

    return render(request, 'common/index.html', context)


class AdminBookDetailsView(DetailView):
    model = AdminBook
    template_name = "books/admin-book-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comment_form'] = CommentForm()
        context['comments']= self.object.comment_set.all()

        return context


@login_required
def comment_functionality(request, book_id: int):
    if request.POST:
        book = AdminBook.objects.get(pk=book_id)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_book = book
            comment.profile = request.user.profile
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + f'#{book_id}')

