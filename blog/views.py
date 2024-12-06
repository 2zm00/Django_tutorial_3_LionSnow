from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Post
from .forms import CategoryForm, PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):    
    categories = Category.objects.all()
    posts = Post.objects.all()
    context = {'categories':categories,
               'posts':posts
               }
    return render(request, 'blog/index.html', context)

def category_list(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request, 'blog/category_list.html', context)

@login_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # 유효성 검증
        if form.is_valid():
            form.save()
            return redirect('blog:category_list')
        
    elif request.method == "GET": # form 입력하는 페이지는 표시
        categories = Category.objects.all()
        form = CategoryForm()  
    return render(request, 'blog/category_form.html', context={'form':form, 'categories':categories})
            
def post_detail(request, post_id):
    # post_id의 post를 보내주기
    post = Post.objects.get(pk=post_id) # 지금 보여주고자 하는 디테일 페이지의 정보
    posts = Post.objects.filter(category=post.category) # 현재 보는 내용에 추가로 다른 포스트들을 표현하기 위함
    categories = Category.objects.all() # 사이드바에 카테고리항목을 표시하기 위한
    context = {'post':post,'categories':categories, 'posts':posts}    
    return render(request, 'blog/post_detail.html', context)

def category_post_list(request, category_id):
    # category_id인 카테고리에 속한 포스트들의 리스트를 보여주기
    category = get_object_or_404(Category, id=category_id)
    categories = Category.objects.all()

    posts = Post.objects.filter(category=category)
    context = {'posts':posts, 'category':category, 'categories':categories}
    return render(request, 'blog/index.html', context)

@login_required
def post_write(request, category_id):
    # post 작성
    # 이전에 했던 question, **choice** 어떤것과 유사한가?
    # form 이용
    if request.method == 'GET':
        category = Category.objects.get(pk=category_id)
        categories = Category.objects.all()        
        form = PostForm()
        context={'form':form, 'categories':categories, 'category':category}
        return render(request=request, template_name='blog/post_form.html',context=context)
    # elif request.method=='POST':
    #     pass
    else: 
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # 아직 DB에 저장하지 않음
            category = Category.objects.get(pk=category_id)
            post.category = category  # 카테고리 설정
            # 추가적으로 작가 정보를 넣어야 됩니다!!
            # 어떻게 하면 될까요??
            # 11:40까지 해보겠습니다.
            # request.user에 유저정보가 담겨 있습니다.
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', post_id=post.id)
            # return redirect('blog:index')

@login_required
def post_edit(request, post_id):
    # post_id인 post의 내용을 편집하기
    # 작성 폼의 형태는 기본 post와 같지만
    # 이전의 내용이 담겨 있어야지 효과적인 편집이 가능하다
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'GET':
        form = PostForm(instance=post)
        context={'form':form}
        return render(request, 'blog/post_form.html', context )
    else:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save() # 내가 저장한 내용이 잘 보이는지 확인하고 싶습니다.
            return redirect('blog:post_detail', post_id=post.id)

def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('blog:index')