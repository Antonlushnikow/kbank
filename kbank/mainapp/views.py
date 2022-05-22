import django.views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    ListView,
)
from django.views.generic.edit import FormMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status

from .models import Article, Category, Comment, Notification
from authapp.models import KbankUser
from .forms import ArticleCreateForm, ArticleEditForm, CommentForm
from .serializers import CommentSerializer
from authapp.permissions import Privileged
from .utils import PersonalNotification

from django.db.models import Count
from django.utils.text import slugify

TOP_ARTICLE_COUNT = 5
SORTING_METHODS = {
    'old': 'publish_date',
    'new': '-publish_date',
    'likes': 'likes',
}


class ArticlesListView(ListView):
    """
    Контроллер вывода списка статей на главной странице
    """
    model = Article
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticlesListView, self).get_context_data()
        top_articles = [
                           item for item in Article.objects.filter(is_visible=True).annotate(count=Count('likes')).order_by('-count') if item.is_last_month
                       ][:TOP_ARTICLE_COUNT]
        context['top_articles'] = top_articles
        return context

    def get_queryset(self):
        return Article.objects.filter(is_visible=True).order_by('-publish_date')


class ArticleCreateView(CreateView):
    """
    Контроллер создания статьи
    """
    model = Article
    template_name = 'mainapp/create-article.html'
    form_class = ArticleCreateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/auth/login')

        if request.user.is_blocked:
            return HttpResponseNotFound(f'Пользователь заблокирован до {request.user.block_expires}')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleCreateView, self).get_context_data()
        context['title'] = 'новая статья'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        item = form.save()
        self.pk = item.pk

        body = f"Необходима проверка статьи {self.request.POST['title']} пользователя {self.request.user}"
        url = reverse('articles:article', kwargs={'pk': self.pk})
        notification = PersonalNotification(
            body=body,
            title="модерация",
            request=self.request,
            url=url,
            scope="moderators",
        )
        notification.create()

        # notification for user
        PersonalNotification(
            body='Ваша статья отправлена на модерацию. После того, как статья пройдет проверку и будет опубликована, Вы получите уведомление.',
            title="модерация",
            request=self.request,
            url=url,
        ).create()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articles:article', kwargs={'pk': self.pk})


class ArticleReadView(FormMixin, DetailView):
    """
    Контроллер вывода статьи по номеру
    """
    model = Article
    template_name = 'mainapp/article.html'
    form_class = CommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleReadView, self).get_context_data()
        context['title'] = 'статья'
        context['form'] = CommentForm(initial={'article': self.object, 'author': self.request.user})
        return context

    def get_object(self, queryset=None):
        obj = get_object_or_404(Article, pk=self.kwargs['pk'])
        obj.views += 1
        obj.save()
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['sorting_method'] = 'publish_date'
        if 'sort' in request.GET:
            if request.GET['sort'] in SORTING_METHODS:
                context['sorting_method'] = SORTING_METHODS[request.GET['sort']]
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # создание комментария

        if request.user.is_blocked:
            return HttpResponseNotFound(f'Пользователь заблокирован до {request.user.block_expires}')
        self.object = self.get_object()

        if '@moderator' in request.POST['body']:
            article = get_object_or_404(Article, pk=kwargs['pk'])
            body = f"{request.user} пожаловался на {article.title}"
            url = request.path
            notification = PersonalNotification(
                body=body,
                title="жалоба",
                request=request,
                url=url,
                scope="moderators",
            )
            notification.create()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        if 'parent' in self.request.POST:
            comment = get_object_or_404(Comment, pk=self.request.POST['parent'])
            form.instance.parent = comment
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articles:article', kwargs={'pk': self.object.id})


class ArticleEditView(UpdateView):
    """
    Контроллер редактирования статьи
    """
    model = Article
    template_name = 'mainapp/edit-article.html'
    form_class = ArticleEditForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleEditView, self).get_context_data()
        context['title'] = 'редактирование статьи'
        return context

    def form_valid(self, form):
        item = form.save()
        self.pk = item.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articles:article', kwargs={'pk': self.pk})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if Article.objects.get(pk=kwargs['pk']).author.id == request.user.id \
                    or request.user.is_superuser or request.user.is_moderator:
                return super(ArticleEditView, self).dispatch(request, *args, **kwargs)
        return HttpResponseRedirect('/')


class CategoryListView(ListView):
    """
    Контроллер вывода статей по категории
    """
    model = Article
    template_name = 'mainapp/list-articles.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        context['title'] = category.title
        return context

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Article.objects.filter(category=category, is_visible=True).order_by('-publish_date')


class ArticleListAuthorView(ListView):
    """
    Контроллер вывода статей по авторам
    """
    model = Article
    template_name = 'mainapp/list-articles.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleListAuthorView, self).get_context_data()
        author = get_object_or_404(KbankUser, pk=self.kwargs['pk'])
        context['title'] = f'Статьи - {author.username}'
        return context

    def get_queryset(self):
        author = get_object_or_404(KbankUser, pk=self.kwargs['pk'])
        return Article.objects.filter(author=author, is_visible=True).order_by('-publish_date')


class LikeAPIView(APIView):
    """
    Представление лайков через API
    Абстрактный класс
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model = None

    def get(self, request, pk=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        user = self.request.user
        updated = False
        liked = False

        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True

        data = {
            'updated': updated,
            'liked': liked,
            'like_count': obj.likes.count(),
        }

        return Response(data)


class ArticleLikeAPIView(LikeAPIView):
    model = Article


class CommentLikeAPIView(LikeAPIView):
    model = Comment

    def get(self, request, pk=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        if not obj.is_visible:
            return HttpResponseNotFound('Page not found')
        return super().get(request, pk)


class CommentAPIView(APIView):
    """
    Представление комментариев через API
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [Privileged]
    model = Comment

    def get(self, request, pk=None):
        # получение комментария

        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        author = obj.author.username
        body = obj.body

        data = {
            'author': author,
            'body': body,
        }
        return Response(data)

    def patch(self, request, pk):
        # изменение комментария
        try:
            obj = get_object_or_404(self.model, pk=pk)
            serializer = CommentSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        except Exception as e:
            print('Cannot edit comment.', e.args)
            return Response(status=status.HTTP_400_BAD_REQUEST, data="wrong parameters")

    def delete(self, request, pk):
        try:
            obj = get_object_or_404(self.model, pk=pk)
            obj.delete()
        except Exception as e:
            print('Cannot delete comment', e.args)
        finally:
            return Response(status=status.HTTP_204_NO_CONTENT)


class CommentVisibleToggleAPI(APIView):
    """
    Показ/скрытие комментариев
    """
    model = Comment
    permission_classes = [Privileged]

    def get(self, request, pk=None):
        try:
            obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
            is_visible = obj.is_visible
            obj.is_visible = is_visible = False if is_visible else True
            obj.save()
            data = {
                'is_visible': is_visible,
            }
        except Exception as e:
            print('Cannot hide comment.', e.args)
            data = {
                'is_visible': False,
            }
        finally:
            return Response(data)


class ReportCommentAPI(APIView):
    """
    Reporting comment for moderation
    """
    model = Comment
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        try:
            obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
            obj.moderation_required = True
            obj.save()
            data = {
                'result': True,
            }
            # Уведомление для модераторов о поступлении новой жалобы на комментарий
            PersonalNotification(request=request,
                                 body='Поступил новый комментарий для модерации',
                                 scope='moderators', title='модерация',
                                 url=f'/article/{obj.article.pk}#comment-{pk}'
                                 ).create()

            # Уведомление для автора комментария о поступлении жалобы на его комментарий
            PersonalNotification(request=request,
                                 body='На ваш комментарий поступила жалоба! Обратите внимание!',
                                 users_group=[obj.author], title='жалоба',
                                 url=f'/article/{obj.article.pk}#comment-{pk}'
                                 ).create()

        except Exception as e:
            print('Cannot report comment.', e.args)
            data = {
                'result': False,
            }
        finally:
            return Response(data)


class NotificationsListView(LoginRequiredMixin, ListView):
    """
    Контроллер вывода списка уведомлений
    """
    model = Notification
    template_name = 'mainapp/notifications.html'
    context_object_name = 'notifications'
    paginate_by = 10
    login_url = reverse_lazy('auth:login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NotificationsListView, self).get_context_data()
        user = get_object_or_404(KbankUser, pk=self.request.user.pk)
        context['title'] = f'Уведомления - {user.username}'
        return context

    def get_queryset(self):
        user = get_object_or_404(KbankUser, pk=self.request.user.pk)
        return Notification.objects.filter(user=user).order_by('-created_date')


class NotificationReadToggleAPI(APIView):
    """
    Показ/скрытие комментариев
    """
    model = Notification
    permission_classes = [Privileged]

    def get(self, request, pk=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        is_read = obj.is_read
        obj.is_read = is_read = False if is_read else True
        obj.save()

        data = {
            'is_read': is_read,
        }

        return Response(data)


class TagListView(ListView):
    """
    Контроллер вывода статей по тегам
    """
    model = Article
    template_name = 'mainapp/list-articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Article.objects.filter(tags__slug=slug, is_visible=True).order_by('-publish_date')
