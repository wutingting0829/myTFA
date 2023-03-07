from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


def user_directory_path(instance, filename):
    return 'posts/%Y/%m/%d/'.format(instance.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)


    # return the title of the post. 
    # if you don't do this, it will be post(1), post(2)...
    def __str__(self):
        return self.name


class Post(models.Model):

    
    # not only post all object but also published
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1)# create ForeighKey for Category table. 
    #'on_delete': In here we already took a connection between Post and Category. If now we delete a category which doesn't exist, then the database will be broken. 
    # Therefore, this function defines what we should do the post if we delete a category.
    # 'default=1': the post that we've already made they're going to be assigned to default which is going to be the ccategory default.

    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    image = models.ImageField(
        upload_to=user_directory_path, default='posts/default2.jpg')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=options, default='draft')
    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager, call the class # to bring the filter out the posts that are published, we're never going to return posts that aren't published.

    
    # to get the blog title so that can get the slug information
    def get_absolute_url(self):
        return reverse('blog:post_single', args=[self.slug])

    
    # define the ordering of that list or the list of post.
    # post的排序由時間由newest-->oldest
    class Meta:
        ordering = ('-publish',)

    
    # return the title of the post. 
    # if you don't do this, it will be post(1), post(2)...
    def __str__(self):
        return self.title


class Comment(MPTTModel):

    # evertyime we create new comment there's going to be an association between that comment and an item in the post table.
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    
    # others parameters
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)  # if you want to delete the comment, you could change the status from true to false.(true -> comments live; false -> comments won't e shown)

    class MPTTMeta:
        order_insertion_by = ['publish']


    # return the comment of the post by the author name. 
    def __str__(self):
        return self.name
