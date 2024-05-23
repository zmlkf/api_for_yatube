from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """
    Model for a group of posts.
    Fields:
        title: Group title.
        slug: Unique group identifier.
        description: Group description.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title[:50]


class Post(models.Model):
    """
    Model for a post.
    Fields:
    - text: Post text.
    - pub_date: Date and time of post publication.
    - author: Post author (foreign key to the user model).
    - image: Post image.
    - group: Group to which the post belongs (foreign key to the group model).
    """
    text = models.TextField()
    pub_date = models.DateTimeField('Publication date', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    """
    Model for a comment on a post.
    Fields:
    - author: Comment author (foreign key to the user model).
    - post: Post related to the comment (foreign key to the post model).
    - text: Comment text.
    - created: Date and time when the comment was added.
    """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Date added', auto_now_add=True, db_index=True)


class Follow(models.Model):
    """
    Model for a user following other users.
    Fields:
    - user: User who is following (foreign key to the user model).
    - following: User being followed (foreign key to the user model).
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        # Unique combination of fields
        unique_together = ('user', 'following')

    def __str__(self):
        return f'{self.user} follows {self.following}'[:50]
