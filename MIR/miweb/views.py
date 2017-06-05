# coding:utf-8
import json
import re
from itertools import chain
import compare

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

import generateinvitenum
import generatepicid
import uploadpic
#import searchdatabase
import os
from models import Img, Userallinfo, Invitecode, Imgcomment, Imgupload, Newsbox, Friend, Piccollection, Collection, FriendGroup,Article,Hotwords
from .forms import NameForm, SearchForm, InfoForm, SignupForm, UploadForm,SafeForm, ReviewForm,ChangeForm


# Create your views here.
def home_views(request):
    if not request.user.is_authenticated():
        loginorout = True
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            id = user.user_name
            name = user.user_nicheng
            loginorout = False
        except:
            mess = "未知错误"
    imgdatatop10 = Img.objects.all().order_by('-view')[:10]
    imguploaddatatop10 = Imgupload.objects.all().order_by('-view')[:10]
    return render(request, 'miweb/home.html', locals())


def base(request):
    return render(request, 'miweb/base.html', locals())


def login_views(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            mess = ""
            inputemail = form.cleaned_data['your_email']
            inputpassword = form.cleaned_data['your_password']
            try:
                us = Userallinfo.objects.get(user_email=inputemail)
            except:
                mess = "该邮箱未注册！"
                return render(request, 'miweb/login.html', locals())
            user = authenticate(username=us.user_name, password=inputpassword)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    mess = "用户被禁止登陆！"
                    return render(request, 'miweb/login.html', locals())
        else:
            mess = "填写不完整！"
        return render(request, 'miweb/login.html', locals())
    else:
        return render(request, 'miweb/login.html', locals())


def logout_views(request):
    logout(request)
    return HttpResponseRedirect('/')


def resultsimage_views(request):
    if not request.user.is_authenticated():
        loginorout = True
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            loginorout = False
        except:
            mess = "未知错误"
    ONE_PAGE_OF_DATA = 10
    if request.method == 'POST':
        image = request.FILES.get('stfile')
        path, result = compare.com(image)
        #request.session['search_img'] = path
        #result_img_upload = []
        posts = []
        for img in result:
            record = Img.objects.get(abid=img[1])
            posts.append(record)
        for img in posts:
            img.cansee = True
        '''
        try:
            curPage = int(request.GET.get('curPage', 1))
            allPage = int(request.GET.get('allPage', 1))
            pageType = str(request.GET.get('pageType',''))
        except ValueError:
            curPage = 1
            allPage = 1
            pageType = ''
        if pageType == 'pageDown':
            curPage += 1
        elif pageType == 'pageUp':
            curPage -= 1
        startPos = (curPage - 1) * ONE_PAGE_OF_DATA
        #print(startPos)
        endPos = startPos + ONE_PAGE_OF_DATA
        #print(endPos)
        posts = imgdata[startPos:endPos]
        #print(posts)
        if(len(posts) == 0):
            isnullmess = 1#不为空
        else:
            isnullmess = 0#不为空
        #print(isnullmess)
        if curPage == 1 and allPage == 1:
            allPostCounts = len(imgdata)
            allPage = allPostCounts / ONE_PAGE_OF_DATA
            remainPost = allPostCounts % ONE_PAGE_OF_DATA
            if remainPost > 0:
                allPage += 1
        disPages = allPage - curPage
        if curPage < 3:
            if allPage < 5:
                pagelist = range(1, allPage+1)
            else:
                pagelist = range(1, 6)
        elif disPages < 3:
            if allPage < 5:
                pagelist = range(1, allPage+1)
            else:
                pagelist = range(allPage-4, allPage+1)
        else:
            pagelist = range(curPage-2, curPage+3)
        '''
    return render(request, 'miweb/results.html', locals())


def results_views(request):
    if not request.user.is_authenticated():
        loginorout = True
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            loginorout = False
        except:
            mess = "未知错误"
    ONE_PAGE_OF_DATA = 10
    level = ''
    if request.method == 'POST':
        your_choice = request.POST.get('artiorimg', 1)
        if your_choice == u"图像":
            form = SearchForm(request.POST)
            if form.is_valid():
                mess = "nice"
                search_content = form.cleaned_data['your_search']
                try:#判断是否存在
                    hotwords = Hotwords.objects.get(hotwords=search_content,type='0')
                    print '1111111'
                    hotwords.view = hotwords.view+1
                    hotwords.save()
                except:#不存在则创建热词项目 0为图像1为文章
                    Hotwords.objects.create(hotwords=search_content,view=1,type='0')
                request.session['search_content'] = search_content
                levelchoic = request.POST.getlist('checkbox')
                for j in levelchoic:
                    level = level + j
                print levelchoic
                print level
                if len(levelchoic) == 0:
                    imgdata_search = Img.objects.filter(abstract__contains=search_content)
                    for i in imgdata_search:
                        i.cansee = True
                    imguploaddata_search = Imgupload.objects.filter(abstract__contains=search_content)
                    for i in imguploaddata_search:
                        if i.protectlevel[0] == 'A':
                            i.cansee = True
                        elif i.protectlevel[0] == 'B':
                            try:
                                ownpic = i.nameid
                                Friend.objects.get(user_name=user.user_name,friendname=ownpic)
                                i.cansee = True
                            except:
                                i.cansee = False
                        elif i.protectlevel[0] == 'E':
                            i.cansee = False
                        try:
                            user = Userallinfo.objects.get(user_name = request.user.username)
                            if user.user_name == i.nameid:
                                i.cansee = True
                        except:
                            pass
                    imgdata = list(chain(imgdata_search, imguploaddata_search))
                    print imgdata_search
                    print imguploaddata_search
                    print imgdata
                else:
                    print 'asdkjgasdijhapsiodug'
                    n = 0
                    imgdata = []
                    for i in levelchoic:
                        imgdata_search = Img.objects.filter(abstract__contains=search_content).filter(rank=i)
                        for h in imgdata_search:
                            h.cansee = True
                        imgdata = list(chain(imgdata, imgdata_search))
                    for i in levelchoic:
                        imguploaddata_search = Imgupload.objects.filter(abstract__contains=search_content).filter(rank=i)
                        for h in imguploaddata_search:
                            if h.protectlevel[0] == 'A':
                                h.cansee = True
                            elif h.protectlevel[0] == 'B':
                                try:
                                    ownpic = h.nameid
                                    Friend.objects.get(user_name=user.user_name,friendname=ownpic)
                                    h.cansee = True
                                except:
                                    h.cansee = False
                            elif h.protectlevel[0] == 'E':
                                h.cansee = False
                            if user.user_name == h.nameid:
                                h.cansee = True
                        imgdata = list(chain(imgdata, imguploaddata_search))
                #print imgdata
                try:
                    curPage = int(request.GET.get('curPage', 1))
                    allPage = int(request.GET.get('allPage', 1))
                    pageType = str(request.GET.get('pageType',''))
                except ValueError:
                    curPage = 1
                    allPage = 1
                    pageType = ''
                if pageType == 'pageDown':
                    curPage += 1
                elif pageType == 'pageUp':
                    curPage -= 1
                startPos = (curPage - 1) * ONE_PAGE_OF_DATA
                #print(startPos)
                endPos = startPos + ONE_PAGE_OF_DATA
                #print(endPos)
                posts = imgdata[startPos:endPos]
                #print(posts)
                if(len(posts) == 0):
                    isnullmess = 1#不为空
                else:
                    isnullmess = 0#不为空
                #print(isnullmess)
                if curPage == 1 and allPage == 1:
                    allPostCounts = len(imgdata)
                    allPage = allPostCounts / ONE_PAGE_OF_DATA
                    remainPost = allPostCounts % ONE_PAGE_OF_DATA
                    if remainPost > 0:
                        allPage += 1
                disPages = allPage - curPage
                if curPage < 3:
                    if allPage < 5:
                        pagelist = range(1, allPage+1)
                    else:
                        pagelist = range(1, 6)
                elif disPages < 3:
                    if allPage < 5:
                        pagelist = range(1, allPage+1)
                    else:
                        pagelist = range(allPage-4, allPage+1)
                else:
                    pagelist = range(curPage-2, curPage+3)
                #print pagelist
            else:
                mess = "error"
                isnullmess = 2
            hotword = Hotwords.objects.filter(type='0').order_by('-view')[:5]
            return render(request, 'miweb/results.html', locals())
        elif your_choice == u"资讯":
            form = SearchForm(request.POST)
            if form.is_valid():
                mess = "nice"
                try:
                    '''try:
                        search_content = form.cleaned_data['your_search']
                        search_content = str(search_content.encode('utf-8'))
                        idnum, tags = searchdatabase.searcharticle(search_content)
                        print idnum
                    except:
                        print '出现异常'
                    articledata = []
                    for id in idnum:
                        print id[0]
                        ids = int(id[0])
                        article = Article.objects.get(id=ids)

                        articledata.append(article)
                    print '444444444'
                    for tag in tags:
                        tag = ('').join(tag)
                        print tag
                        try:#判断是否存在
                            hotwords = Hotwords.objects.get(hotwords=tag,type='1')
                            hotwords.view = hotwords.view+1
                            hotwords.save()
                        except:#不存在则创建热词项目 0为图像1为文章
                            Hotwords.objects.create(hotwords=tag,view=1,type='1')
                    '''
                    search_content = form.cleaned_data['your_search']
                    search_content = str(search_content.encode('utf-8'))
                    try:#判断是否存在
                        hotwords = Hotwords.objects.get(hotwords=search_content,type='1')
                        hotwords.view = hotwords.view+1
                        hotwords.save()
                    except:#不存在则创建热词项目 0为图像1为文章
                        Hotwords.objects.create(hotwords=search_content,view=1,type='1')
                    articledata = Article.objects.filter(abstract__contains=search_content)
                except:
                    print '出现异常'

                request.session['search_content'] = search_content
                try:
                    curPage = int(request.GET.get('curPage', 1))
                    allPage = int(request.GET.get('allPage', 1))
                    pageType = str(request.GET.get('pageType',''))
                except ValueError:
                    curPage = 1
                    allPage = 1
                    pageType = ''
                if pageType == 'pageDown':
                    curPage += 1
                elif pageType == 'pageUp':
                    curPage -= 1
                startPos = (curPage - 1) * ONE_PAGE_OF_DATA
                #print(startPos)
                endPos = startPos + ONE_PAGE_OF_DATA
                #print(endPos)
                posts = articledata[startPos:endPos]
                #print(posts)
                if(len(posts) == 0):
                    isnullmess = 1#为空
                else:
                    isnullmess = 0#不为空
                #print(isnullmess)
                if curPage == 1 and allPage == 1:
                    allPostCounts = len(articledata)
                    allPage = allPostCounts / ONE_PAGE_OF_DATA
                    remainPost = allPostCounts % ONE_PAGE_OF_DATA
                    if remainPost > 0:
                        allPage += 1
                disPages = allPage - curPage
                if curPage < 3:
                    if allPage < 5:
                        pagelist = range(1, allPage+1)
                    else:
                        pagelist = range(1, 6)
                elif disPages < 3:
                    if allPage < 5:
                        pagelist = range(1, allPage+1)
                    else:
                        pagelist = range(allPage-4, allPage+1)
                else:
                    pagelist = range(curPage-2, curPage+3)
                #print pagelist
            else:
                mess = "error"
                isnullmess = 2
            hotword = Hotwords.objects.filter(type='1').order_by('-view')[:5]
            return render(request, 'miweb/article.html', locals())
    elif request.method == 'GET':
        level = request.GET.get('level','A')
        levelchoic = list(level)
        try:
            search_content = request.GET.get('search', '')
            aori = request.GET.get('aori', '')
        except ValueError:
            pass
        if aori == '0':#图片检索
            if len(levelchoic) == 0:
                imgdata_search = Img.objects.filter(abstract__contains=search_content)
                for i in imgdata_search:
                    i.cansee = True
                imguploaddata_search = Imgupload.objects.filter(abstract__contains=search_content)
                for i in imguploaddata_search:
                    if i.protectlevel[0] == 'A':
                        i.cansee = True
                    elif i.protectlevel[0] == 'B':
                        try:
                            ownpic = i.nameid
                            Friend.objects.get(user_name=user.user_name,friendname=ownpic)
                            i.cansee = True
                        except:
                            i.cansee = False
                    elif i.protectlevel[0] == 'E':
                        i.cansee = False
                    try:
                        user = Userallinfo.objects.get(user_name = request.user.username)
                        if user.user_name == i.nameid:
                            i.cansee = True
                    except:
                        pass
                imgdata = list(chain(imgdata_search, imguploaddata_search))
                print imgdata_search
                print imguploaddata_search
                print imgdata
            else:
                print 'asdkjgasdijhapsiodug'
                n = 0
                imgdata = []
                for i in levelchoic:
                    imgdata_search = Img.objects.filter(abstract__contains=search_content).filter(rank=i)
                    for h in imgdata_search:
                        h.cansee = True
                    imgdata = list(chain(imgdata, imgdata_search))
                for i in levelchoic:
                    imguploaddata_search = Imgupload.objects.filter(abstract__contains=search_content).filter(rank=i)
                    for h in imguploaddata_search:
                        if h.protectlevel[0] == 'A':
                            h.cansee = True
                        elif h.protectlevel[0] == 'B':
                            try:
                                ownpic = h.nameid
                                Friend.objects.get(user_name=user.user_name,friendname=ownpic)
                                h.cansee = True
                            except:
                                h.cansee = False
                        elif h.protectlevel[0] == 'E':
                            h.cansee = False
                        if user.user_name == h.nameid:
                            h.cansee = True
                    imgdata = list(chain(imgdata, imguploaddata_search))
            try:
                curPage = int(request.GET.get('curPage', 1))
                allPage = int(request.GET.get('allPage', 1))
                pageType = str(request.GET.get('pageType', ''))
            except ValueError:
                curPage = 1
                allPage = 1
                pageType = ''
            if pageType == 'pageDown':
                curPage += 1
            elif pageType == 'pageUp':
                curPage -= 1
            elif pageType == 'pageTo':
                pass
            startPos = (curPage - 1) * ONE_PAGE_OF_DATA
            endPos = startPos + ONE_PAGE_OF_DATA
            posts = imgdata[startPos:endPos]
            if curPage == 1 and allPage == 1:
                allPostCounts = len(imgdata)
                allPage = allPostCounts / ONE_PAGE_OF_DATA
                remainPost = allPostCounts % ONE_PAGE_OF_DATA
                if remainPost > 0:
                    allPage += 1
            disPages = allPage - curPage
            if curPage < 3:
                if allPage < 5:
                    pagelist = range(1, allPage+1)
                else:
                    pagelist = range(1, 6)
            elif disPages < 3:
                if allPage < 5:
                    pagelist = range(1, allPage+1)
                else:
                    pagelist = range(allPage-4, allPage+1)
            else:
                pagelist = range(curPage-2, curPage+3)
            return render(request, 'miweb/results.html', locals())
        elif aori == '1':#资讯检索
            articledata = Article.objects.filter(keyword__contains=search_content)
            try:
                curPage = int(request.GET.get('curPage', 1))
                allPage = int(request.GET.get('allPage', 1))
                pageType = str(request.GET.get('pageType', ''))
            except ValueError:
                curPage = 1
                allPage = 1
                pageType = ''
            if pageType == 'pageDown':
                curPage += 1
            elif pageType == 'pageUp':
                curPage -= 1
            elif pageType == 'pageTo':
                pass
            startPos = (curPage - 1) * ONE_PAGE_OF_DATA
            endPos = startPos + ONE_PAGE_OF_DATA
            posts = articledata[startPos:endPos]
            if curPage == 1 and allPage == 1:
                allPostCounts = len(articledata)
                allPage = allPostCounts / ONE_PAGE_OF_DATA
                remainPost = allPostCounts % ONE_PAGE_OF_DATA
                if remainPost > 0:
                    allPage += 1
            disPages = allPage - curPage
            if curPage < 3:
                if allPage < 5:
                    pagelist = range(1, allPage+1)
                else:
                    pagelist = range(1, 6)
            elif disPages < 3:
                if allPage < 5:
                    pagelist = range(1, allPage+1)
                else:
                    pagelist = range(allPage-4, allPage+1)
            else:
                pagelist = range(curPage-2, curPage+3)
            return render(request, 'miweb/article.html', locals())
    else:
        mess = "wrong"
        return render(request, 'miweb/results.html', locals())


def personinfo(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            loginorout = False
        except:
            mess = "未知错误"
    userid = user.user_name
    user_infoall = Userallinfo.objects.get(user_name=userid)
    sex = user_infoall.user_sex
    if sex == '1':
        male = "active"
        female = ""
    else:
        male = ""
        female = "active"
    print male
    email = user_infoall.user_email
    info = user_infoall.user_info
    job = user_infoall.user_place
    phone = user_infoall.user_phone
    if request.method == "POST":
        xinxi = InfoForm(request.POST)
        if xinxi.is_valid():
            print xinxi.cleaned_data
            newnicheng = xinxi.cleaned_data['your_name']
            newphone = xinxi.cleaned_data['your_phone']
            newinfo = xinxi.cleaned_data['your_info']
            newjob = xinxi.cleaned_data['your_place']
            user_infoall.user_phone = newphone
            user_infoall.user_info = newinfo
            user_infoall.user_nicheng = newnicheng
            user_infoall.user_place = newjob
            sexchange = request.POST.get('your_sex')
            if sexchange is None:
                user_infoall.user_sex = sex
            else:
                user_infoall.user_sex = sexchange
            user_infoall.save()
            if user_infoall.user_sex == '1':
                male = "active"
                female = ""
            else:
                male = ""
                female = "active"
            mess = "（更新成功！）"
            name = user_infoall.user_nicheng
            email = user_infoall.user_email
            info = user_infoall.user_info
            job = user_infoall.user_place
            phone = user_infoall.user_phone
            return render(request, 'miweb/personinfo.html', locals())
        else:
            mess = "（修改失败，填写不完整！）"
            return render(request, 'miweb/personinfo.html', locals())
    else:
        return render(request, 'miweb/personinfo.html', locals())


def personnews(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            loginorout = False
        except:
            mess = "未知错误"
    return render(request, 'miweb/personnews.html', locals())


def safepass(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            loginorout = False
        except:
            mess = "未知错误"
    dl = False
    if request.method == "POST":
        ur = SafeForm(request.POST)
        if ur.is_valid():
            old_password = ur.cleaned_data['old_password']
            new_password = ur.cleaned_data['new_password']
            new_two_password = ur.cleaned_data['new_two_password']
            print old_password,new_password,new_two_password
            check_user = authenticate(username=user.user_name, password=old_password)
            if check_user:
                if old_password != new_password and new_password == new_two_password:
                    check_user.set_password(new_password)
                    check_user.save()
                    mess = "修改成功,请重新登陆"
                    dl = True
                else:
                    mess = "新密码有误"
            else:
                mess = "原密码有误"
        else:
            mess = "信息填写不完整"
    return render(request, 'miweb/safepass.html', locals())


def personcollect(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            loginorout = False
        except:
            mess = "未知错误"
    return render(request, 'miweb/personcollect.html', locals())


def personfriends(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            loginorout = False
        except:
            mess = "未知错误"
    return render(request, 'miweb/personfriends.html', locals())


def personsearch(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            loginorout = False
        except:
            mess = "未知错误"
    return render(request, 'miweb/personsearch.html', locals())


def advices(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            loginorout = False
        except:
            mess = "未知错误"
    return render(request, 'miweb/advices.html', locals())


def about(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            loginorout = False
        except:
            mess = "未知错误"
    return render(request, 'miweb/about.html', locals())


def details(request, pic_id):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect("/miweb/login")
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            loginorout = False
        except:
            mess = "未知错误"
    search_content = request.session.get('search_content', default="")
    abidstr = str(pic_id)
    ly = re.findall(r'([A-Z])', abidstr)[0]
    collectionid = 0
    if ly == 'N': #爬虫
        mess_ly = True
        img = Img.objects.get(abid = pic_id)
        pname = "未知"
    else:#用户上传
        img = Imgupload.objects.get(abid = pic_id)
        mess_ly = False
        pname = img.picname
    img.view += 1
    img.save()
    try:
        picable = Piccollection.objects.get(collectionid=collectionid,picnum=pic_id,coll_name=userid)
        if picable.isdelete == True:
            collectornot = '1'
        else:
            collectornot = '0'
    except:
        collectornot = '1'
    return render(request, 'miweb/details.html', locals())


def con_details(request):#右上角消息通知，最新创建的五个和创建消息时间距当前时间为多少
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            #print userid
            loginorout = False
        except:
            mess = "未知错误"
    response_data = []
    if request.method == "POST":
        posttag = request.POST['dtag']
        poststatus = request.POST['dstatus']
        if posttag == "0":#查询图片有几条评论
            if poststatus == "0":
                dpicid = request.POST['dpicid']
                ns = Imgcomment.objects.filter(abid=dpicid)
                for i in ns:
                    newsdata = {}
                    nicheng = i.name
                    newsdata['nicheng'] = nicheng
                    newsdata['anwser'] = i.anwser
                    newsdata['moditime'] = str(i.answertime)
                    newsdata['anwid'] = i.id
                    response_data.append(newsdata)
            else:
                pass
        elif posttag == "1":#对评论进行操作
            if poststatus == "0":#为图片添加评论
                dpicid = request.POST['dpicid']
                dpostcomment = request.POST['dcommnet']
                print(dpostcomment)
                newabid = dpicid
                newname = name + "(#" + userid[-5:] + ")"
                newnameid = userid
                newcomment = dpostcomment
                newagree = 0
                #latest_post = Imgcomment.objects.filter(abid=dpicid).order_by('-prior')[:1][0]
                #newprior = latest_post.prior + 1
                newprior = 0
                newanswertime = timezone.now()
                try:
                    imgc = Imgcomment(abid=newabid, name=newname, anwser=newcomment, agree=newagree, prior=newprior, answertime=newanswertime, nameid=newnameid, isdelete=False)
                    imgc.save()
                    abidstr = str(dpicid)
                    ly = re.findall(r'([A-Z])', abidstr)[0]
                    if ly == 'N':  # 爬虫
                        img = Img.objects.get(abid=dpicid)
                    else:  # 用户上传
                        img = Imgupload.objects.get(abid=dpicid)
                        dpostownid = img.nameid
                        dpostownnicheng = img.author
                        #发消息给图片所有者
                        ncontent = dpicid + ":" + dpostcomment
                        Newsbox.objects.create(newstag=3,newsstatus=0,newscontent=ncontent,newsfrom=userid,newsfromname=name,newsto=dpostownid,newstoname=dpostownnicheng,isdelete=False,newstime=str(timezone.now()))
                    img.comment += 1
                    img.save()
                    newsdata = {}
                    newsdata['dok'] = 0
                    newsdata['dmess'] = "发表评论成功！"
                    response_data.append(newsdata)
                except:
                    newsdata = {}
                    newsdata['dok'] = 1
                    newsdata['dmess'] = "错误异常！"
                    response_data.append(newsdata)
            elif poststatus == "1":#为评论添加评论
                pass
            elif poststatus == "2":#删除评论
                pass
            elif poststatus == "3":#给评论点赞
                pass
    else:
        newsdata = {}
        newsdata['key'] = 5
        newsdata['value'] = "OK"
        response_data.append(newsdata)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def upload(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            job = user.user_place
            author = name + "(#" + user.user_name[-5:] + ")"
            loginorout = False
        except:
            mess = "未知错误"
    picid = generatepicid.genepicid()
    if request.method == "POST":
        uf = UploadForm(request.POST,request.FILES)
        if uf.is_valid():
            newpicname = uf.cleaned_data['pic_name']
            newcode = picid
            #newfilename
            newauthor = name + "(#" + user.user_name[-5:] + ")"
            newnameid = user.user_name
            newtool = uf.cleaned_data['pic_tool']
            newabstract = uf.cleaned_data['pic_abstract']
            newcontent = uf.cleaned_data['pic_content']
            newjob = uf.cleaned_data['pic_job']
            newkeywords = ""
            newcheck = False
            newview = 0
            newcomment =0
            #now = int(time.time())
            #timeArray = time.localtime(now)
            #newcreatetime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            #newmoditime = newcreatetime
            newcreatetime = timezone.now()
            newmoditime = newcreatetime
            namelist = uploadpic.handle_uploaded_file(request.FILES['pic_way'])
            plevel = request.POST.get("plevel", 'A')
            protectword = plevel + ';'
            iu = Imgupload(filename=namelist[1], loadway=namelist[0], picname=newpicname, author=newauthor, tool=newtool, abstract=newabstract, content=newcontent, createtime=newcreatetime, moditime=newmoditime, keywords=newkeywords, check=newcheck, view=newview, comment=newcomment, abid=newcode, nameid=newnameid, authorjob=newjob, protectlevel=protectword)
            iu.save()
            mess = "上传成功！"
        else:
            mewss = "填写不完整"
    return render(request, 'miweb/uploadcentre.html', locals())


def signup_views(request):
    if request.method == "POST":
        ur = SignupForm(request.POST)
        if ur.is_valid():
            email = ur.cleaned_data['your_email']
            usernicheng = ur.cleaned_data['your_name']
            password = ur.cleaned_data['your_password']
            inputcode = ur.cleaned_data['your_invitecode']
            print ur.cleaned_data
            try:
                uus = User.objects.get(email=email)
                mess = "该邮箱已被注册！"
                print mess
                return render(request, 'miweb/signup.html', locals())
            except:
                print "该邮箱可用"
            username = generateinvitenum.geneusernum()
            print username
            try:
                ic = Invitecode.objects.get(code=inputcode)
            except:
                mess = "请核对邀请码！"
                print mess
                return render(request, 'miweb/signup.html', locals())
            User.objects.create_user(username, email, password)
            a = Userallinfo(user_name=username, user_email=email, user_sex=0, user_phone=0, user_info=0, user_nicheng=usernicheng)
            a.save()
            ic.caninvitenum -= 1
            ic.save()
            if ic.caninvitenum == 0:
                ic.delete()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    mess = "error"
            else:
                mess = "error"
            return render(request, 'miweb/signupsucc.html', locals())
        else:
            mess = "填写有误！"
            return render(request, 'miweb/signup.html', locals())
    else:
        form = SignupForm()
    return render(request, 'miweb/signup.html', locals())


def success_views(request):
    return render(request, 'miweb/signupsucc.html', locals())


def worklog(request):
    return render(request, 'miweb/worklog.html', locals())


def change(request, pic_id):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            loginorout = False
        except:
            mess = "未知错误"
    try:
        imgup = Imgupload.objects.get(abid=pic_id)
        imgup.sele = imgup.protectlevel[0]
    except:
        pass
    if request.method == 'POST':
        cf = ChangeForm(request.POST)
        if cf.is_valid():
            newpicname = cf.cleaned_data['pic_name']
            newjob = cf.cleaned_data['pic_job']
            newabstract = cf.cleaned_data['pic_abstract']
            newcontent = cf.cleaned_data['pic_content']
            imgup.picname = newpicname
            imgup.abstract = newabstract
            imgup.content = newcontent
            imgup.authorjob = newjob
            #now = int(time.time())
            #timeArray = time.localtime(now)
            #newmoditime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            newmoditime = timezone.now()
            imgup.moditime = newmoditime
            plevel = request.POST.get("plevel", 'A')
            protectword = plevel + ';'
            imgup.protectlevel = protectword
            imgup.save()
            mess = "修改成功！"
        else:
            mess = "信息不完整！"
    return render(request, 'miweb/change.html', locals())


def con_friend(request):
    if request.method == "POST":
        postcontent = request.POST['content']
        posttag = request.POST['tag']
        postfromid = request.POST['fromid']
        postfromname = request.POST['fromname']
        print posttag, postcontent, postfromid
        #添加到消息箱里
        try:
            uus = Userallinfo.objects.get(user_email=postcontent)
            ncontent = "add friend"
            try:
                Friend.objects.get(user_name=postfromid, friendname=uus.user_name)
                response_data = {}
                response_data['result'] = 'fail'
                response_data['message'] = "该用户已是你好友！"
            except:
                try:
                    print '123'
                    Newsbox.objects.get(newstag=1, newsstatus=0, newscontent=ncontent, newsfrom=postfromid, newsfromname=postfromname, newsto=uus.user_name, newstoname=uus.user_nicheng)
                    print '345'
                    response_data = {}
                    response_data['result'] = 'fail'
                    response_data['message'] = "已发送过好友请求！"
                except:
                    nb = Newsbox(newstag=1, newsstatus=0, newscontent=ncontent, newsfrom=postfromid, newsfromname=postfromname, newsto=uus.user_name, newstoname=uus.user_nicheng, newstime = str(timezone.now()))
                    nb.save()
                    response_data = {}
                    response_data['result'] = 'succ'
                    response_data['message'] = "成功发送请求！"
        except:
            response_data = {}
            response_data['result'] = 'fail'
            response_data['message'] = '请求添加好友用户不存在！'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def con_news(request):
    response_data = []
    if request.method == "POST":
        posttag = request.POST['ntag']
        poststatus = request.POST['nstatus']
        postuserid = request.POST['userid']
        if posttag == "0":#未处理信息
            if poststatus == "0":#好友信息
                ns = Newsbox.objects.filter(newsstatus=0).filter(newstag=1).filter(newsto=postuserid).filter(isdelete=False)
                if len(ns) == 0:
                    newsdata = {}
                    newsdata['userid'] = 0
                    newsdata['username'] = "无任何未处理消息"
                    response_data.append(newsdata)
                else:
                    for i in ns:
                        newsdata = {}
                        newsdata['userid'] = i.newsfrom
                        newsdata['username'] = i.newsfromname
                        response_data.append(newsdata)
                        print(response_data)
            elif poststatus == "1":#非好友消息
                ns = Newsbox.objects.filter(newsstatus=0).filter(newsto=postuserid).filter(isdelete=False).exclude(newstag=1).exclude(newstag=8).exclude(newstag=2)#未处理通知信息
                if len(ns) == 0:
                    newsdata = {}
                    newsdata['userid'] = 0
                    newsdata['username'] = "无任何未阅读通知信息"
                    response_data.append(newsdata)
                else:
                    for i in ns:
                        newsdata = {}
                        newsdata['userid'] = i.newsfrom
                        newsdata['username'] = i.newsfromname
                        if i.newstag == 3:#图片被评论
                            newsdata['mess'] = "3"
                            newsc = i.newscontent
                            idpoint = newsc.find(":")
                            newsdata['mess1'] = newsc[:idpoint]#图片id
                            try:
                                pnid = newsc[:idpoint]
                                iu = Imgupload.objects.get(abid=pnid)
                                newsdata['mess3'] = iu.picname
                            except:
                                newsdata['mess3'] = "未知图片"
                                newsdata['mess1'] = ""
                            newsdata['mess2'] = "评论了你的"
                            newsdata['mess4'] = i.id
                            response_data.append(newsdata)
                        elif i.newstag == 4:#图片被收藏
                            newsdata['mess'] = "4"
                            newsdata['mess1'] = i.newscontent#图片id
                            try:
                                iu = Imgupload.objects.get(abid=i.newscontent)
                                newsdata['mess3'] = iu.picname
                            except:
                                newsdata['mess3'] = "未知图片"
                                newsdata['mess1'] = ""
                            newsdata['mess2'] = "收藏了你的"
                            newsdata['mess4'] = i.id#消息的id
                            response_data.append(newsdata)
            elif poststatus == "2":#系统消息
                ns = Newsbox.objects.filter(newsstatus=0).filter(newsto=postuserid).filter(isdelete=False).filter(newstag=2 or 8)  # 未处理系统消息
                if len(ns) == 0:
                    newsdata = {}
                    newsdata['userid'] = 0
                    newsdata['username'] = "无任何未阅读系统信息"
                    response_data.append(newsdata)
                else:
                    for i in ns:
                        newsdata = {}
                        newsdata['userid'] = i.newsfrom
                        newsdata['username'] = i.newsfromname
                        if i.newstag == 2:  # 图片被审核
                            newsdata['mess'] = "3"
                            newsc = i.newscontent
                            idpoint = newsc.find(":")
                            newsdata['mess1'] = newsc[:idpoint]  # 图片id
                            try:
                                pnid = newsc[:idpoint]
                                iu = Imgupload.objects.get(abid=pnid)
                                newsdata['mess3'] = iu.picname
                            except:
                                newsdata['mess3'] = "未知图片"
                                newsdata['mess1'] = ""
                            newsdata['mess2'] = "审核了你的"
                            newsdata['mess4'] = i.id
                            response_data.append(newsdata)
                        elif i.newstag == 4:  # 评论被删除
                            pass
        elif posttag == "1":#已处理信息
            if poststatus == "0":  # 好友信息
                ns = Newsbox.objects.filter(newstag=1).filter(newsto=postuserid).filter(isdelete=False).exclude(newsstatus=0)
                if len(ns) == 0:
                    newsdata = {}
                    newsdata['userid'] = 0
                    newsdata['username'] = "无任何已处理消息"
                    response_data.append(newsdata)
                else:
                    for i in ns:
                        newsdata = {}
                        newsdata['userid'] = i.newsfrom
                        newsdata['username'] = i.newsfromname
                        if i.newsstatus == 1:
                            newsdata['mess'] = "您已同意"
                            newsdata['mess2'] = "向您发来的好友请求"
                        elif i.newsstatus == 2:
                            newsdata['mess'] = "您已拒绝"
                            newsdata['mess2'] = "向您发来的好友请求"
                        elif i.newsstatus == 3:
                            newsdata['mess'] = "您的好友请求被"
                            newsdata['mess2'] = "拒绝"
                        elif i.newsstatus == 4:
                            newsdata['mess'] = "您的好友请求被"
                            newsdata['mess2'] = "同意"
                        response_data.append(newsdata)
            elif poststatus == "1":
                ns = Newsbox.objects.filter(newsstatus=1).filter(newsto=postuserid).filter(isdelete=False).exclude(newstag=1).exclude(newstag=8).exclude(newstag=2)  # 已处理回复信息
                if len(ns) == 0:
                    newsdata = {}
                    newsdata['userid'] = 0
                    newsdata['username'] = "无任何已阅读通知信息"
                    response_data.append(newsdata)
                else:
                    for i in ns:
                        newsdata = {}
                        newsdata['userid'] = i.newsfrom
                        newsdata['username'] = i.newsfromname
                        if i.newstag == 3:#图片被评论
                            newsdata['mess'] = "3"
                            newsc = i.newscontent
                            idpoint = newsc.find(":")
                            newsdata['mess1'] = newsc[:idpoint]#图片id
                            try:
                                pnid = newsc[:idpoint]
                                iu = Imgupload.objects.get(abid=pnid)
                                newsdata['mess3'] = iu.picname
                            except:
                                newsdata['mess3'] = "未知图片"
                                newsdata['mess1'] = ""
                            newsdata['mess2'] = "评论了你的"
                            newsdata['mess4'] = i.id
                            response_data.append(newsdata)
                        elif i.newstag == 4:#图片被收藏
                            newsdata['mess'] = "4"
                            newsdata['mess1'] = i.newscontent#图片id
                            try:
                                iu = Imgupload.objects.get(abid=i.newscontent)
                                newsdata['mess3'] = iu.picname
                            except:
                                newsdata['mess3'] = "未知图片"
                                newsdata['mess1'] = ""
                            newsdata['mess2'] = "收藏了你的"
                            newsdata['mess4'] = i.id#消息的id
                            response_data.append(newsdata)
            elif poststatus == "2":#系统消息
                ns = Newsbox.objects.filter(newsstatus=1).filter(newsto=postuserid).filter(isdelete=False).filter(newstag=2 or 8)  # 未处理系统消息
                print len(ns)
                if len(ns) == 0:
                    newsdata = {}
                    newsdata['userid'] = 0
                    newsdata['username'] = "无任何已阅读系统信息"
                    response_data.append(newsdata)
                else:
                    for i in ns:
                        newsdata = {}
                        newsdata['userid'] = i.newsfrom
                        newsdata['username'] = i.newsfromname
                        if i.newstag == 2:  # 图片被审核
                            newsdata['mess'] = "3"
                            newsc = i.newscontent
                            idpoint = newsc.find(":")
                            newsdata['mess1'] = newsc[:idpoint]  # 图片id
                            try:
                                pnid = newsc[:idpoint]
                                iu = Imgupload.objects.get(abid=pnid)
                                newsdata['mess3'] = iu.picname
                            except:
                                newsdata['mess3'] = "未知图片"
                                newsdata['mess1'] = ""
                            newsdata['mess2'] = "审核了你的"
                            newsdata['mess4'] = i.id
                            response_data.append(newsdata)
                        elif i.newstag == 4:  # 评论被删除
                            pass
            elif poststatus == "2":#系统消息
                ns = Newsbox.objects.filter(newsstatus=1).filter(newsto=postuserid).filter(isdelete=False).exclude(newstag=1).exclude(newstag=3).exclude(newstag=4).exclude(newstag=5).exclude(newstag=6).exclude(newstag=7)  # 未处理系统消息
                if len(ns) == 0:
                    newsdata = {}
                    newsdata['userid'] = 0
                    newsdata['username'] = "无任何已阅读系统信息"
                    response_data.append(newsdata)
                else:
                    for i in ns:
                        newsdata = {}
                        newsdata['userid'] = i.newsfrom
                        newsdata['username'] = i.newsfromname
                        if i.newstag == 2:  # 图片被审核
                            newsdata['mess'] = "3"
                            newsc = i.newscontent
                            idpoint = newsc.find(":")
                            newsdata['mess1'] = newsc[:idpoint]  # 图片id
                            try:
                                pnid = newsc[:idpoint]
                                iu = Imgupload.objects.get(abid=pnid)
                                newsdata['mess3'] = iu.picname
                            except:
                                newsdata['mess3'] = "未知图片"
                                newsdata['mess1'] = ""
                            newsdata['mess2'] = "审核了你的"
                            newsdata['mess4'] = i.id
                            response_data.append(newsdata)
                        elif i.newstag == 4:  # 评论被删除
                            pass
        elif posttag == "2":#查询详情
            if poststatus == "3":#图片评论详情
                newsid = request.POST['newsid']
                try:
                    nbid = Newsbox.objects.get(id=newsid, isdelete=False)
                    newsc = nbid.newscontent
                    nbid.newsstatus = 1
                    nbid.save()
                    idpoint = newsc.find(":")
                    newsdata = {}
                    newsdata['mess'] = 0
                    newsdata['mess1'] = newsc[idpoint+1:]
                    response_data.append(newsdata)
                except:
                    newsdata = {}
                    newsdata['mess'] = 1
                    newsdata['mess1'] = "出现异常"
                    response_data.append(newsdata)
            elif poststatus == "4":#收藏图片详情
                newsid = request.POST['newsid']
                try:
                    nbid = Newsbox.objects.get(id=newsid, isdelete=False)
                    newsc = nbid.newscontent
                    nbid.newsstatus = 1
                    nbid.save()
                    idpoint = newsc.find(":")
                    newsdata = {}
                    newsdata['mess'] = 0
                    newsdata['mess1'] = "标记成功"
                    response_data.append(newsdata)
                except:
                    newsdata = {}
                    newsdata['mess'] = 1
                    newsdata['mess1'] = "出现异常"
                    response_data.append(newsdata)
            elif poststatus == "5":  # 图片审阅详情
                newsid = request.POST['newsid']
                try:
                    nbid = Newsbox.objects.get(id=newsid, isdelete=False)
                    newsc = nbid.newscontent
                    nbid.newsstatus = 1
                    nbid.save()
                    idpoint = newsc.find(":")
                    newsdata = {}
                    newsdata['mess'] = 0
                    newsdata['mess1'] = newsc[idpoint+1:]
                    response_data.append(newsdata)
                except:
                    newsdata = {}
                    newsdata['mess'] = 1
                    newsdata['mess1'] = "出现异常"
                    response_data.append(newsdata)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def con_test(request):
    response_data = []
    for i in range(0, 5):
        newsdata = {}
        newsdata['key'] = i
        newsdata['value'] = "OK"
        response_data.append(newsdata)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def upload_record(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            loginorout = False
        except:
            mess = "未知错误"

    return render(request, 'miweb/upload_record.html', locals())


def con_upload(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            loginorout = False
        except:
            mess = "未知错误"
    response_data = []
    if request.method == "POST":
        posttag = request.POST['utag']
        print posttag
        postuserid = userid
        postpage = int(request.POST['upage'])
        poststatus = request.POST['ustatus']
        print poststatus
        if posttag == "0":
            if poststatus == "0":
                ns = Imgupload.objects.filter(nameid=postuserid).filter(isdelete=False)
                for i in ns:
                    newsdata = {}
                    newsdata['nsid'] = i.abid
                    newsdata['nsname'] = i.picname
                    newsdata['nscreatetime'] = str(i.createtime)
                    newsdata['nsmoditime'] = str(i.moditime)
                    newsdata['nscheck'] = i.check
                    response_data.append(newsdata)
            else:
                pass
        elif posttag == "1":
            if poststatus == "0":
                print "sdsadsadadsad"
                postpicid = request.POST['upicid']
                print postpicid
                try:
                    deletedata = Imgupload.objects.get(abid=postpicid)
                    deletedata.isdelete = True
                    deletedata.save()
                except:
                    pass
                ns = Imgupload.objects.filter(nameid=postuserid).filter(isdelete=False)
                for i in ns:
                    newsdata = {}
                    newsdata['nsid'] = i.abid
                    newsdata['nsname'] = i.picname
                    newsdata['nscreatetime'] = str(i.createtime)
                    newsdata['nsmoditime'] = str(i.moditime)
                    newsdata['nscheck'] = str(i.check)
                    response_data.append(newsdata)
    else:
        newsdata = {}
        newsdata['key'] = 5
        newsdata['value'] = "OK"
        response_data.append(newsdata)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def review(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            loginorout = False
        except:
            mess = "未知错误"
    return render(request, 'miweb/review.html', locals())


def reviewdetails(request, pic_id):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            id = user.user_name
            loginorout = False
        except:
            mess = "未知错误"
    imginfo = Imgupload.objects.get(abid=pic_id)

    record = Imgupload.objects.filter(check=0).exclude(createtime__gte=imginfo.createtime)
    print record
    try:
        img = list(record)[-1]
        uabid = img.abid
        isnoneu = 1
    except:
        isnoneu = 0

    record = Imgupload.objects.filter(check=0).exclude(createtime__lte=imginfo.createtime)
    try:
        img = list(record)[0]
        dabid = img.abid
        isnoned = 1
    except:
        isnoned = 0

    if request.method == "POST":
        cadvice = ReviewForm(request.POST)
        if cadvice.is_valid():
            newcontent = cadvice.cleaned_data['review_idea']
            level = request.POST.get("level", 'D')
            newadvice = newcontent
            imginfo.check = 1
            imginfo.checkwords = newadvice
            imginfo.checkauthor = id
            imginfo.rank = level
            imginfo.save()
            newscontent = pic_id + ':' + newcontent
            Newsbox.objects.create(newstag=2,newsstatus=0,newscontent=newscontent,newsfrom='test',newsfromname='系统管理员',newsto=imginfo.nameid,newstoname=imginfo.author,isdelete=False,newstime=str(timezone.now()))
            mess = "发布成功"
        else:
            mess = "意见为空！"
    return render(request, 'miweb/reviewdetails.html', locals())


def con_review(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            print userid
            loginorout = False
        except:
            mess = "未知错误"
    response_data = []
    if request.method == "POST":
        posttag = request.POST['retag']
        print posttag
        postuserid = userid
        postpage = int(request.POST['repage'])
        poststatus = request.POST['restatus']
        print poststatus
        if posttag == "0":#未审阅记录
            if poststatus == "0":
                ns = Imgupload.objects.filter(check=0).filter(isdelete=False).order_by("-createtime")
                for i in ns:
                    newsdata = {}
                    newsdata['reid'] = i.abid
                    newsdata['rename'] = i.picname
                    newsdata['recreatedate'] = str(i.createtime)
                    newsdata['recheck'] = "未审阅"
                    newsdata['recheckauthor'] = ""
                    print i.abid
                    response_data.append(newsdata)
            elif poststatus == "1":
                ns = Imgupload.objects.filter(check=0).filter(isdelete=False).order_by("createtime")
                for i in ns:
                    newsdata = {}
                    newsdata['reid'] = i.abid
                    newsdata['rename'] = i.picname
                    newsdata['recreatedate'] = str(i.createtime)
                    newsdata['recheck'] = "未审阅"
                    newsdata['recheckauthor'] = ""
                    print i.abid
                    response_data.append(newsdata)
        elif posttag == '1':#该用户审阅过的记录
            if poststatus == "0":#上面是旧的
                nsi = Imgupload.objects.filter(check=1).filter(isdelete=False).order_by("-createtime")
                for q in nsi:
                    qnewsdata = {}
                    qnewsdata['reid'] = q.abid
                    qnewsdata['rename'] = q.picname
                    qnewsdata['recreatedate'] = str(q.createtime)
                    qnewsdata['recheck'] = "已审阅"
                    x = Userallinfo.objects.get(user_name=q.checkauthor)
                    print x.user_nicheng
                    qnewsdata['recheckauthor'] = x.user_nicheng
                    response_data.append(qnewsdata)
            elif poststatus == "1":#上面是新的
                nsi = Imgupload.objects.filter(check=1).filter(isdelete=False).order_by("createtime")
                for q in nsi:
                    qnewsdata = {}
                    qnewsdata['reid'] = q.abid
                    qnewsdata['rename'] = q.picname
                    qnewsdata['recreatedate'] = str(q.createtime)
                    qnewsdata['recheck'] = "已审阅"
                    x = Userallinfo.objects.get(user_name=q.checkauthor)
                    print x.user_nicheng
                    qnewsdata['recheckauthor'] = x.user_nicheng
                    response_data.append(qnewsdata)
        elif posttag == '2':#此用户审阅记录
            if poststatus == "0":#上面是旧的
                nsi = Imgupload.objects.filter(check=1).filter(checkwords=userid).filter(isdelete=False).order_by("-createtime")
                for q in nsi:
                    qnewsdata = {}
                    qnewsdata['reid'] = q.abid
                    qnewsdata['rename'] = q.picname
                    qnewsdata['recreatedate'] = str(q.createtime)
                    qnewsdata['recheck'] = "已审阅"
                    x = Userallinfo.objects.get(user_name=q.checkauthor)
                    print x.user_nicheng
                    qnewsdata['recheckauthor'] = x.user_nicheng
                    response_data.append(qnewsdata)
            elif poststatus == "1":#上面是新的
                nsi = Imgupload.objects.filter(check=1).filter(checkwords=userid).filter(isdelete=False).order_by("createtime")
                for q in nsi:
                    qnewsdata = {}
                    qnewsdata['reid'] = q.abid
                    qnewsdata['rename'] = q.picname
                    qnewsdata['recreatedate'] = str(q.createtime)
                    qnewsdata['recheck'] = "已审阅"
                    x = Userallinfo.objects.get(user_name=q.checkauthor)
                    print x.user_nicheng
                    qnewsdata['recheckauthor'] = x.user_nicheng
                    response_data.append(qnewsdata)
    else:
        newsdata = {}
        newsdata['key'] = 5
        newsdata['value'] = "OK"
        response_data.append(newsdata)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def con_collect(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            print userid
            loginorout = False
        except:
            mess = "未知错误"
    response_data = []
    if request.method == "POST":
        posttag = request.POST['cotag']
        poststatus = request.POST['costatus']
        print posttag
        postuserid = userid
        cid = 0
        if posttag == "0":#图片详细页面点击收藏
            postabid = request.POST['coabid']
            uord = list(postabid)[0]
            if poststatus == "0":#收藏
                try:
                    if uord == "N":#爬虫
                        picable = Img.objects.get(abid=postabid)
                    elif uord == "U":#上传
                        picable = Imgupload.objects.get(abid=postabid)
                    else:
                        pass
                    if picable.isdelete == False:
                        try:
                            coable = Collection.objects.get(collectionid=cid, creator=userid)
                        except:
                            Collection.objects.create(collectionid=cid, creator=userid,isdelete=False,createtime=str(timezone.now()),own_tag="默认图集",permission="A",share_num=0,agree_num=0,comment_num=0)
                        try:
                            piccc = Piccollection.objects.get(collectionid=cid, picnum=postabid, coll_name=userid)
                            piccc.isdelete = False
                            piccc.save()
                        except:
                            Piccollection.objects.create(collectionid=cid, picnum=postabid,isdelete=False, coll_name=userid)
                        #向信息箱里添加收藏信息
                        if uord == "U":
                            Newsbox.objects.create(newstag=4, newsstatus=0, newscontent=postabid, newsfrom=userid, newsfromname=name, newsto=picable.nameid, newstoname=picable.author, isdelete=False, newstime=str(timezone.now()) )
                        newsdata = {}
                        newsdata['able'] = '收藏成功'
                        response_data.append(newsdata)
                    else:
                        newsdata = {}
                        newsdata['able'] = '收藏失败:图片已删除'
                        response_data.append(newsdata)
                except:
                    newsdata = {}
                    newsdata['able'] = '收藏失败:出现异常错误'
                    response_data.append(newsdata)
            else:#取消收藏
                try:
                    picc = Piccollection.objects.get(collectionid=cid, picnum=postabid, owner_name=userid)
                    picc.isdelete = True
                    picc.save()
                    newsdata = {}
                    newsdata['able'] = '取消成功'
                    response_data.append(newsdata)
                except:
                    newsdata = {}
                    newsdata['able'] = '未收藏'
                    response_data.append(newsdata)
        elif posttag == '1':#显示收藏信息
            poststatus = request.POST['costatus']
            if poststatus == "0":
                ns = Piccollection.objects.filter(collectionid =cid).filter(coll_name=userid).filter(isdelete=False)
                for i in ns:
                    uord = list(i.picnum)[0]
                    if uord == "N":#爬虫
                        picable = Img.objects.get(abid=i.picnum)
                    elif uord == "U":#上传
                        picable = Imgupload.objects.get(abid=i.picnum)
                    newsdata = {}
                    newsdata['picid'] = i.picnum
                    if picable.picname == "":
                        newsdata['picname'] = "暂无"
                    else:
                        newsdata['picname'] = picable.picname
                    newsdata['picowner'] = picable.author
                    newsdata['piclevel'] = "未分级"
                    response_data.append(newsdata)
            else:
                pass
        elif posttag == '2':#对某条收藏信息进行更改
            poststatus = request.POST['costatus']
            if poststatus == "0":#删除某一条收藏信息
                postpicid = request.POST['copicid']
                postcollectid = request.POST['collectid']
                try:
                    deletedata = Piccollection.objects.get(picnum=postpicid,collectionid=postcollectid,owner_name=userid)
                    deletedata.isdelete = True
                    deletedata.save()
                    newsdata = {}
                    newsdata['able'] = '移除收藏图集成功'
                    response_data.append(newsdata)
                except:
                    newsdata = {}
                    newsdata['able'] = '未知错误'
                    response_data.append(newsdata)
    else:
        newsdata = {}
        newsdata['key'] = 5
        newsdata['value'] = "OK"
        response_data.append(newsdata)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def con_friendagree(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            loginorout = False
        except:
            mess = "未知错误"
    response_data = []
    if request.method == "POST":
        postagree = request.POST['fagree']
        postfromid = request.POST['fromid']
        print(postfromid)
        posttoid = userid
        print(posttoid)
        try:
            frompreson = Userallinfo.objects.get(user_name=postfromid)
            toperson = Userallinfo.objects.get(user_name=posttoid)
            if postagree == "1":#同意
                Friend.objects.create(user_name=postfromid, friendname=posttoid, tag='0', origin='0', beizhu='0')
                Friend.objects.create(user_name=posttoid, friendname=postfromid, tag='0', origin='0', beizhu='0')
                print 'ahgsssssssssssssssssssss'
                Newsbox.objects.create(newstag=1, newsstatus=4, newscontent="对方已添加你为好友", newsfrom=posttoid, newsfromname=toperson.user_nicheng,newsto=postfromid, newstoname=frompreson.user_nicheng, isdelete=False, newstime = str(timezone.now()))
                news = Newsbox.objects.get(newstag=1,newsstatus=0,newsfrom=postfromid,newsto=posttoid)
                news.newsstatus = 1
                news.newstime = str(timezone.now())
                news.save()
                newsdata = {}
                newsdata['agree'] = "0"
                response_data.append(newsdata)
            elif postagree == "0":#不同意:
                Newsbox.objects.create(newstag=1, newsstatus=3, newscontent="对方拒绝添加你为好友", newsfrom=posttoid, newsfromname=toperson.user_nicheng,newsto=postfromid, newstoname=frompreson.user_nicheng, newstime = str(timezone.now()))
                news = Newsbox.objects.get(newstag=1,newsstatus=0,newsfrom=postfromid,newsto=posttoid)
                news.newsstatus = 2
                news.newstime = str(timezone.now())
                news.save()
                newsdata = {}
                newsdata['agree'] = "1"
                response_data.append(newsdata)
        except:
            newsdata = {}
            newsdata['agree'] = "2"
            response_data.append(newsdata)
    else:
        newsdata = {}
        newsdata['agree'] = "1"
        response_data.append(newsdata)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def con_frienddata(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            loginorout = False
        except:
            mess = "未知错误"
    response_data = []
    if request.method == "POST":
        posttage = request.POST['ftag']
        poststatus = request.POST['fstatus']
        if posttage == '0':#获取好友信息
            if poststatus == '0':#获取分组信息
                fg = FriendGroup.objects.filter(authorid=userid)
                for i in fg:
                    newsdata = {}
                    newsdata['gid'] = i.authorgroupid
                    newsdata['gname'] = i.groupname
                    response_data.append(newsdata)
            elif poststatus == '1':#获取组内信息
                postfgid = request.POST['fgid']
                try:
                    gfriend = Friend.objects.filter(user_name=userid).filter(tag=postfgid)
                    print gfriend
                    if gfriend == []:#无好友
                        newsdata = {}
                        newsdata['fname'] = "0"
                        newsdata['fnicheng'] = "未添加好友"
                    else:#好友不为空
                        for i in gfriend:
                            nameid = i.friendname
                            try:
                                nicheng = Userallinfo.objects.get(user_name=nameid)
                                newsdata = {}
                                newsdata['fname'] = i.friendname
                                newsdata['fnicheng'] = nicheng.user_nicheng
                                response_data.append(newsdata)
                            except:
                                newsdata['fname'] = "1"
                                newsdata['fnicheng'] = ""
                                response_data.append(newsdata)
                except:
                    newsdata = {}
                    newsdata['fname'] = "2"
                    newsdata['fnicheng'] = "服务器异常"
                    response_data.append(newsdata)
        elif posttage == '1':#更改好友信息:
            if poststatus == '0':#更改分组信息
                pass
            else:#更改组内好友信息
                pass
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def begin(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            loginorout = False
        except:
            mess = "未知错误"
    return render(request, 'miweb/begin.html', locals())


def saferealname(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            loginorout = False
        except:
            mess = "未知错误"
    return render(request, 'miweb/saferealname.html', locals())


def invitecode(request):
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            loginorout = False
        except:
            mess = "未知错误"
    try:
        ic = Invitecode.objects.get(generateuser=user.user_name)
        cangenenum = False
        outputinvitenum = ic.caninvitenum
        outputcode = ic.code
    except:
        cangenenum = True
    if request.method == "POST":
        newcode = generateinvitenum.genenum()
        newgenerateuser = user.user_name
        newinvitenum = 5
        newic = Invitecode(code=newcode, caninvitenum=int(newinvitenum), generateuser=newgenerateuser)
        newic.save()
        ic = Invitecode.objects.get(generateuser=user.user_name)
        cangenenum = False
        outputinvitenum = ic.caninvitenum
        outputcode = ic.code
    return render(request, 'miweb/invitecode.html', locals())


def con_rightnews(request):#右上角消息通知，最新创建的五个和创建消息时间
    if not request.user.is_authenticated():
        loginorout = True
        return HttpResponseRedirect('/')
    else:
        try:
            user = Userallinfo.objects.get(user_name = request.user.username)
            name = user.user_nicheng
            userid = user.user_name
            print userid
            loginorout = False
        except:
            mess = "未知错误"
    response_data = []
    if request.method == "POST":
        posttag = request.POST['ntag']
        if posttag == "0":#显示五条消息
            news = Newsbox.objects.filter(newsto=userid).filter(isdelete=False).filter(newsstatus=0)
            friendnews = Newsbox.objects.filter(newstag=1).filter(newsto=userid).filter(isdelete=False).filter(newsstatus=0).order_by("-newstime")
            message = Newsbox.objects.filter(newsto=userid).filter(isdelete=False).filter(newsstatus=0).exclude(newstag=1).exclude(newstag=8).order_by("-newstime")
            wmessage = Newsbox.objects.filter(newstag=8).filter(newsto=userid).filter(isdelete=False).filter(newsstatus=0).order_by("-newstime")
            newsdata = {}
            newsdata['long'] = len(news)
            newsdata['friendnews'] = len(friendnews)
            newsdata['message'] = len(message)
            newsdata['wmessage'] = len(wmessage)
            response_data.append(newsdata)
            #if len(news) <= 5:
            #    for i in news:
            #        newsdata = {}#消息名字，来源
            #        newsdata['newsfrom'] = i.newsfromname
            #        newsdata['newstime'] = i.createtime
            #        response_data.append(newsdata)
            #else:
            #    n = 0
            #    for i in news:
            #        newsdata = {}  # 消息名字，来源
            #        newsdata['newsfrom'] = i.newsfromname
            #        newsdata['newstime'] = i.createtime
            #        response_data.append(newsdata)
            #        n = n+1
            #        if n >= 4:
            #            break
            #        else:
            #            pass
        else:
            pass
    else:
        newsdata = {}
        newsdata['key'] = 5
        newsdata['value'] = "OK"
        response_data.append(newsdata)
    return HttpResponse(json.dumps(response_data), content_type="application/json")