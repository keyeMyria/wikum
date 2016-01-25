from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import JsonResponse

from engine import *

from django.http import HttpResponse
from annoying.decorators import render_to


@render_to('website/index.html')
def index(request):
    return {'page': 'index'}


@render_to('website/comments.html')
def comments(request):
    url = request.GET['article']
    source = get_source(url)    
    article = get_article(url, source)
    
    posts = get_posts(article)
    
    threads = []
    
    for post in posts:
        replies = []
        c = Comment.objects.filter(reply_to_disqus=post.disqus_id).order_by('-likes')
        for i in c:
            replies2 = []
            t = Comment.objects.filter(reply_to_disqus=i.disqus_id).order_by('-likes')
            for u in t:
                replies3 = []
                v = Comment.objects.filter(reply_to_disqus=u.disqus_id).order_by('-likes')
                for x in v:
                    replies4 = []
                    a = Comment.objects.filter(reply_to_disqus=x.disqus_id).order_by('-likes')
                    for b in a:
                        replies5 = []
                        d = Comment.objects.filter(reply_to_disqus=b.disqus_id).order_by('-likes')
                        for e in d:
                            replies6 = []
                            f = Comment.objects.filter(reply_to_disqus=e.disqus_id).order_by('-likes')
                            for g in f:
                                replies7 = []
                                h = Comment.objects.filter(reply_to_disqus=g.disqus_id).order_by('-likes')
                                for i in h:
                                    replies7.append(i)
                                
                                post_info7 = (g, replies7)
                                replies6.append(post_info7)
                            
                            post_info6 = (e, replies6)
                            replies5.append(post_info6)
                            
                        post_info5 = (b, replies5)
                        replies4.append(post_info5)
                        
                    post_info4 = (x, replies4)
                    replies3.append(post_info4)
                    
                post_info3 = (u, replies3)
                replies2.append(post_info3)
                
            post_info2 = (i, replies2)
            replies.append(post_info2)
        
        post_info = (post, replies)
        threads.append(post_info)
            
    
    return {'article': article,
            'source': source,
            'posts': threads,
            'page': 'comments'}
    

@render_to('website/visualization.html')
def visualization(request):
    url = request.GET['article']
    article = Article.objects.get(url=url)
    return {'article': article,
            'source': article.source}


def recurse_viz(posts):
    children = []
    for post in posts:
        v1 = {'name': post.text, 'size': post.likes}
        c1 = Comment.objects.filter(reply_to_disqus=post.disqus_id).order_by('-likes')
        if c1.count() == 0:
            vals = []
        else:
            vals = recurse_viz(c1)
        v1['children'] = vals
        children.append(v1)
    return children
        
    

def viz_data(request):
    article_id = request.GET['article_id']
    
    a = Article.objects.get(id=article_id)
    
    val = {'name': '<P><h2>%s</h2></p><P><a href="%s">Read the article in the %s</a></p>' % (a.title, a.url, a.source.source_name),
           'size': 400,
           'article': True,
           'children': []}

    posts = a.comment_set.filter(reply_to_disqus=None).order_by('-likes')[0:10]
    val['children'] = recurse_viz(posts)
    return JsonResponse(val)
    
    
    
    
    
    