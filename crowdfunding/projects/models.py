# builtin, importing the current user model defn in the project 
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
# builtin to access and use Django's configuration settings throughout the project
from django.conf import settings

User = get_user_model()

# project model
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)

    # when the related object is deleted, all the objects related to it will also be deleted automatically. 
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner_projects'
    )
    # liked_by = models.ManyToManyField(
    #     User, blank=True, null=True,
    #     related_name='liked_projects'
    # )
    # @property & annotations
    # insert this to count the sum the amount of pledges to calculate

    @property
    def sum_pledges(self):
        # use aggregate & sum together to create a calculation 
        # in this example we are adding all the pledges objects together
        pledge_sum = self.pledges.aggregate(sum=models.Sum("amount"))["sum"]
        # if no pledge then 0 
        if pledge_sum == None:
            return 0
        else:
            return pledge_sum

    @property
    def goal_balance(self):
        return self.goal - self.sum_pledges

    # code to return title name in the drop down
    def __str__(self):
        return self.title

# comments 
class Comment(models.Model):

    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    project = models.ForeignKey(
        'Project',  on_delete=models.CASCADE, related_name='comments')
    commentator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commentator_comment')


# pledges 
class Pledge(models.Model):
    date_pledged = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    comment = models.TextField()
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name='pledges')
    supporter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='supporter_pledges')


# categories model
class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# Favourites Model ***TO BE IMPLEMENTED*** '''
class Favourite(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner_favourites',)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='projects_favourites')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'project')
