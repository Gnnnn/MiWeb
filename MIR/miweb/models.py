from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime
from django.core import validators

# Create your models here.


class Img(models.Model):
    filename = models.CharField(max_length=45)
    picname = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    tool = models.CharField(max_length=200)
    picurl = models.CharField(max_length=200)
    hosturl = models.CharField(max_length=200)
    abstract = models.CharField(max_length=1000)
    loadway = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    createtime = models.DateTimeField(auto_now_add=True)
    moditime = models.DateTimeField(auto_now=True)
    keywords = models.CharField(max_length=1000)
    check = models.BooleanField(default=False)
    view = models.IntegerField()
    comment = models.IntegerField()
    abid = models.CharField(max_length=45)
    checkauthor = models.CharField(max_length=100)
    checkwords = models.CharField(max_length=2000)
    rank = models.CharField(max_length=4)
    isdelete = models.BooleanField(default=False)



class Userallinfo(models.Model):
    user_email = models.EmailField(100)
    user_name = models.CharField(max_length=100)
    user_sex = models.CharField(max_length=100)
    user_phone = models.IntegerField(100)
    user_info = models.CharField(max_length=1000)
    user_place = models.CharField(max_length=1000)
    user_nicheng = models.CharField(max_length=200)


class Invitecode(models.Model):
    code = models.CharField(max_length=50)
    caninvitenum = models.IntegerField()
    generateuser = models.CharField(max_length=30)


class Imgcomment(models.Model):
    abid = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    anwser = models.CharField(max_length=2000)
    agree = models.IntegerField()
    prior = models.IntegerField()
    answertime = models.DateTimeField(auto_now_add=True)
    nameid = models.CharField(max_length=100)
    isdelete = models.BooleanField(default=False)


class Imgupload(models.Model):
    filename = models.CharField(max_length=45)
    loadway = models.FileField()
    picname = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    tool = models.CharField(max_length=200)
    abstract = models.CharField(max_length=1000)
    content = models.CharField(max_length=2000)
    createtime = models.DateTimeField(auto_now_add=True)
    moditime = models.DateTimeField()
    keywords = models.CharField(max_length=1000)
    check = models.IntegerField()
    view = models.IntegerField()
    comment = models.IntegerField()
    abid = models.CharField(max_length=45)
    checkwords = models.CharField(max_length=2000)
    nameid = models.CharField(max_length=100)
    authorjob = models.CharField(max_length=200)
    isdelete = models.BooleanField(default=False)
    checkauthor = models.CharField(max_length=100)
    protectlevel = models.CharField(max_length=200)
    rank = models.CharField(max_length=4)


class Newsbox(models.Model):
    newstag = models.IntegerField()
    newsstatus = models.IntegerField()
    newscontent = models.CharField(max_length=200)
    newsfrom = models.CharField(max_length=100)
    newsfromname = models.CharField(max_length=200)
    newsto = models.CharField(max_length=100)
    newstoname = models.CharField(max_length=200)
    isdelete = models.BooleanField(default=False)
    newstime = models.DateTimeField(auto_now_add=True)


class Friend(models.Model):
    user_name = models.CharField(max_length=45)
    friendname = models.CharField(max_length=45)
    tag = models.CharField(max_length=45)
    origin = models.CharField(max_length=200)
    beizhu = models.CharField(max_length=45)


class Piccollection(models.Model):
    collectionid = models.IntegerField()
    picnum = models.CharField(max_length=200)
    isdelete = models.BooleanField(default=False)
    coll_name = models.CharField(max_length=200)


class Sharecollection(models.Model):
    collectionid = models.IntegerField()
    owner_name = models.CharField(max_length=200)
    isdelete = models.BooleanField(default=False)


class Collection(models.Model):
    collectionid = models.IntegerField()
    creator = models.CharField(max_length=45)
    introduce = models.CharField(max_length=2000)
    createtime = models.DateTimeField(auto_now_add=True)
    own_tag = models.CharField(max_length=45)
    permission = models.CharField(max_length=4)
    share_num = models.IntegerField()
    agree_num = models.IntegerField()
    comment_num = models.IntegerField()
    isdelete = models.BooleanField(default=False)


class FriendGroup(models.Model):
    authorid = models.CharField(max_length=100)
    authorgroupid = models.IntegerField()
    groupname = models.CharField(max_length=100)


class Article(models.Model):
    title = models.CharField(max_length=200)
    keyword = models.CharField(max_length=4000)
    txtname = models.CharField(max_length=200)
    pic = models.CharField(max_length=1000)
    wzurl = models.CharField(max_length=200)
    fn = models.CharField(max_length=1000)
    source = models.CharField(max_length=200)
    keynum = models.IntegerField()
    origin = models.CharField(max_length=200)
    abstract = models.CharField(max_length=4000)


class Hotwords(models.Model):
    hotwords = models.CharField(max_length=200)
    view = models.IntegerField()
    type = models.CharField(max_length=200)


class img_feature_point(models.Model):
    img_id = models.CharField(max_length=100)
    img_type = models.IntegerField()
    img_feature1 = models.CharField(max_length=100)
    img_feature2 = models.CharField(max_length=100)
    img_feature3 = models.CharField(max_length=100)
    img_feature4 = models.CharField(max_length=100)
    img_feature5 = models.CharField(max_length=100)
    img_feature6 = models.CharField(max_length=100)
    img_feature7 = models.CharField(max_length=100)
    img_feature8 = models.CharField(max_length=100)