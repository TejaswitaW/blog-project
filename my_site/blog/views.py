from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Author,Post,Tag
from .forms import CommentForm

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = 'all_posts'

class SinglePostView(View):
    def is_stored_post(self,request,post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self,request,slug):
        post = Post.objects.get(slug=slug)
        
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request,post.id)
        }
        return render(request,'blog/post-detail.html',context)
    def post(self,request,slug):
        post = Post.objects.get(slug=slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # it has created comment instance,yet not hit the database
            comment = comment_form.save(commit=False)
            # we will create post and then save it
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))       
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request,post.id)
        }
        return render(request,'blog/post-detail.html',context)


    # def get_context_data(self, **kwargs):
    #     # getting existing context
    #     context = super().get_context_data(**kwargs)
    #     # tags should be fetched based on the posts 
    #     # we are fetching, self.object is instance of Post 
    #     # model
    #     context['post_tags'] = self.object.tags.all()
    #     context['comment_form'] = CommentForm()
    #     return context
class ReadLaterView(View):
    def get(self,request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context['posts'] = posts
            context["has_posts"] = True
        return render(request,"blog/stored-posts.html",context)
    def post(self,request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []
        # we want to add user selected post(id) in this list
        # post_id we are getting from post_id from form
        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:       
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        else:
            # removing from session
            stored_posts.remove(post_id)
        # after removing upating session data
        request.session["stored_posts"] = stored_posts
        # else redirecting to starting page
        return HttpResponseRedirect("/")