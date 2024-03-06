from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """
    Модель для группы постов.
    Поля:
        title: Заголовок группы.
        slug: Уникальный идентификатор группы.
        description: Описание группы.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title[:50]


class Post(models.Model):
    """
    Модель для поста.
    Поля:
    - text: Текст поста.
    - pub_date: Дата и время публикации поста.
    - author: Автор поста (внешний ключ на модель пользователя).
    - image: Изображение поста.
    - group: Группа, к которой относится пост (внешний ключ на модель группы).
    """
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True
    )

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    """
    Модель для комментария к посту.
    Поля:
    - author: Автор комментария (внешний ключ на модель пользователя).
    - post: Пост, относящийся к комментарию (внешний ключ на модель поста).
    - text: Текст комментария.
    - created: Дата и время добавления комментария.
    """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    """
    Модель для подписки пользователя на других пользователей.
    Поля:
    - user: Пользователь, который подписывается
    (внешний ключ на модель пользователя).
    - following: Пользователь, на которого подписываются
    (внешний ключ на модель пользователя).
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        # Уникальная комбинация полей
        unique_together = ('user', 'following')

    def __str__(self):
        return f'{self.user} follows {self.following}'[:50]
