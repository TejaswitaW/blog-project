from django.shortcuts import render
from datetime import date

all_posts = [
    {
        "slug":"hike-in-the-mountains-1",
        "image":"1.jpg",
        "author":"Max - 1",
        "date": date(2022,4,18),
        "title":"Mountain Hicking-1",
        "excerpt":"This is post excerpt, you will like it",
        "content": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Recusandae perspiciatis voluptas veniam vel voluptate porro quam ratione nostrum reprehenderit eligendi at inventore incidunt suscipit corporis aut sed, voluptates possimus architecto!",
    },
    {
        "slug":"hike-in-the-mountains-2",
        "image":"2.jpg",
        "author":"Max 2 ",
        "date": date(2019,4,18),
        "title":"Mountain Hicking-2",
        "excerpt":"This is post excerpt, you will like it",
        "content": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Recusandae perspiciatis voluptas veniam vel voluptate porro quam ratione nostrum reprehenderit eligendi at inventore incidunt suscipit corporis aut sed, voluptates possimus architecto!",
    },
    {
        "slug":"hike-in-the-mountains-3",
        "image":"3.jpg",
        "author":"Max 3 ",
        "date": date(2023,4,18),
        "title":"Mountain Hicking-3",
        "excerpt":"This is post excerpt, you will like it",
        "content": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Recusandae perspiciatis voluptas veniam vel voluptate porro quam ratione nostrum reprehenderit eligendi at inventore incidunt suscipit corporis aut sed, voluptates possimus architecto!",
    },
    {
        "slug":"hike-in-the-mountains-4",
        "image":"4.jpg",
        "author":"Max 4 ",
        "date": date(2024,4,18),
        "title":"Mountain Hicking-4",
        "excerpt":"This is post excerpt, you will like it",
        "content": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Recusandae perspiciatis voluptas veniam vel voluptate porro quam ratione nostrum reprehenderit eligendi at inventore incidunt suscipit corporis aut sed, voluptates possimus architecto!",
    },
]

def get_date(post):
    return post['date']
def starting_page(request):
    sorted_posts = sorted(all_posts,key=get_date)
    latest_posts = sorted_posts[-3:]
    return render(request,'blog/index.html',{
        "posts":latest_posts
    })
def posts(request):
    return render(request,'blog/all-posts.html',{ 
        "all_posts":all_posts
        })

def post_detail(request,slug):
    identified_post = next(post for post in all_posts if post['slug'] == slug)
    return render(request,'blog/post-detail.html',{'post':identified_post})