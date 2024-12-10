from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView

from books.models import AdminBook
from common.forms import CommentForm
from common.models import Comment


def home_page(request):
    monthly_books = AdminBook.get_monthly_books()
    context = {'monthly_books': monthly_books}

    return render(request, 'common/index.html', context)


@permission_required('common.can_approve_comments', raise_exception=True)
def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if not comment.approved:
        comment.approved = True
        comment.save()
    return redirect('admin-book-details', pk=comment.to_book.id)


class AdminBookDetailsView(DetailView):
    model = AdminBook
    template_name = "books/admin-book-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comment_form'] = CommentForm()
        if self.request.user.has_perm('common.can_approve_comments'):
            context['comments'] = self.object.comment_set.all()
        else:
            context['comments'] = self.object.comment_set.filter(approved=True)
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

