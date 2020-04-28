from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from social.models import FollowUser,MyPost,MyProfile,PostComment,MyPostLike
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from django.http.response import HttpResponseRedirect
# Create your views here.
class HomeView(TemplateView):
    template_name = "social/home.html"
    def get_context_data(self, **kwargs):
        context=TemplateView.get_context_data(self,**kwargs)
        followedList=FollowUser.objects.filter(followed_by=self.request.user.myprofile)
        followedList2=[]
        for e in followedList:
            followedList2.append(e.profile)
        si=self.request.GET.get("si")
        if si==None:
            si=""
        posts=MyPost.objects.filter(Q(uploaded_by__in=followedList2)).filter(Q(subject__icontains=si)|Q(msg__icontains=si)).order_by("-id")
        for p1 in posts:
            p1.liked=False
            ob=MyPostLike.objects.filter(post=p1,liked_by=self.request.user.myprofile)
            if ob:
                p1.liked=True
            ob=MyPostLike.objects.filter(post=p1)
            p1.likecount=ob.count()
        context["mypost_list"]=posts
        return context

class AboutView(TemplateView):
    template_name = "social/about.html"

class ContactView(TemplateView):
    template_name = "social/contact.html"
@method_decorator(login_required,name="dispatch")
class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields = ["name","age","address","status","gender","phone_no","description","pic"]
@method_decorator(login_required,name="dispatch")
class MyPostCreate(CreateView):
    model = MyPost
    fields = ["subject","msg","pic"]
    def form_valid(self, form):
        self.object=form.save()
        self.object.uploaded_by=self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
@method_decorator(login_required,name="dispatch")
class MyPostListView(ListView):
    model = MyPost
    def get_queryset(self):
        si=self.request.GET.get("si")
        if si==None:
            si=""
        return MyPost.objects.filter(Q(uploaded_by=self.request.user.myprofile)).filter(Q(subject__icontains=si)|Q(msg__icontains=si)).order_by("-id")
@method_decorator(login_required,name="dispatch")
class MyPostDetailView(DetailView):
    model = MyPost
@method_decorator(login_required,name="dispatch")
class MyPostDeleteView(DeleteView):
    model = MyPost

@method_decorator(login_required,name="dispatch")
class MyProfileListView(ListView):
    model = MyProfile
    def get_queryset(self):
        si=self.request.GET.get("si")
        if si==None:
            si=""
        ProfileList= MyProfile.objects.filter(Q(name__icontains=si)|Q(address__icontains=si)|Q(gender__icontains=si)|Q(status__icontains=si))
        for p1 in ProfileList:
            p1.followed=False
            ob=FollowUser.objects.filter(profile=p1,followed_by=self.request.user.myprofile)
            if ob:
                p1.followed=True
        return ProfileList
def follow(req,pk):
    user=MyProfile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user,followed_by=req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/myprofile")
def unfollow(req,pk):
    user=MyProfile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user,followed_by=req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/myprofile")
class MyProfileDetailView(DetailView):
    model = MyProfile
def like(req,pk):
    post=MyPost.objects.get(pk=pk)
    MyPostLike.objects.create(post=post,liked_by=req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/home")
def unlike(req,pk):
    post=MyPost.objects.get(pk=pk)
    MyPostLike.objects.filter(post=post,liked_by=req.user.myprofile).delete()
    return HttpResponseRedirect("/social/home")
