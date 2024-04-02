import sys

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail  # importujemy biblioteke która wyśle maila
from django.contrib import messages


def post_list(request):
    posts = Post.published.all()
    # Dodanie stronnicowania/paginacji z 3 postami na stronę
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    # obsługa stron wykraczających poza zakres
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # jeśli zmienna page_number jest poza zakresem to wyświetl ostatnią stronę wyników
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # jeśli zmienna page_number nie jest liczbą to wyświetl pierwszą stronę wyników
        posts = paginator.page(1)

    return render(request,
                  'post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.all()
    comment_form = CommentForm()

    if request.user.is_authenticated:
        comment_form.fields['nick'].disabled = True
        comment_form.fields['nick'].initial = request.user.username

    return render(request,
                  'post/detail.html',
                  {'post': post, 'comment_form': comment_form, 'comments': comments})


def add_comment(request, post_id):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             pk=post_id)
    author = None
    nick = request.POST.get('nick')

    if request.user.is_authenticated:
        nick = request.user.username
        author = request.user

    form = CommentForm({'content': request.POST.get('content'), 'nick': nick})

    if form.is_valid():
        cd = form.cleaned_data
        comment = Comment(nick=cd['nick'], content=cd['content'], author=author, post=post)
        comment.save()
        messages.add_message(request, messages.SUCCESS, "Pomyślnie dodano komentarz")
    else:
        messages.add_message(request, messages.ERROR, "Wystąpiły błędy przy dodawaniu komentarza")
    return redirect(post.get_absolute_url())


# metoda osbługująca egzemplarz formularza i jego przesyłanie

def post_share(request, post_id):
    # Pobieramy post według identyfikatora
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':  # POST to nie nazwa posta/artykułu ale metody przesyłania danych z formularzy
        # Formularz został przesłąny
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Pomyślnie zweryfikowano poprawność pól formularza
            cd = form.cleaned_data
            # określamy jak ma wyglądać wiadomość
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} polecam Ci przeczytanie {post.title}'
            massage = f'Przeczytaj {post.title} pod adresem {post_url} \n Mój komentarz do artukułu: {cd["comments"]}'
            send_mail(subject, massage,
                      'kamil.nowak.testuj@gmail.com',
                      [cd['to']])
            sent = True  # zmiana flagi na wiadomość wysłaną
            # ... wysyłanie maila
    else:
        form = EmailPostForm()

    return render(request,
                  'post/share.html',
                  {'post': post, 'form': form, 'sent': sent})
