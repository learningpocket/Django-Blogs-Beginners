from blog.forms import ContactForm
from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import render,HttpResponse, redirect
from blog.models import Post
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError


# Create your views here.
def home(request):
    # return HttpResponse("Welcome to the blogPage")
    posts = Post.objects.filter(status=1).order_by('-created_on')

    paginator = Paginator(posts, 1)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    context ={'posts':posts, 'page':page}
    return render(request, 'blog/index.html', context)

def contact(request):
    # return HttpResponse("Welcome to the contactPage")

    if request.method == "POST":
        filled_form = ContactForm(request.POST)
        if filled_form.is_valid():
            savings= filled_form.save(commit=False)
            savings.save()
            filled_form.save_m2m()
            newForm = ContactForm
        messages.success(request, "Message successfully sent!")
        return render(request, 'blog/contact.html', {'contactform': newForm})
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'contactform': form})

# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)

#         if form.is_valid():

#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             message = form.cleaned_data['message']

#             try:
#                 send_mail("Thanks for contacting us", message, "baibhavmishra@gmail.com", [email])
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found')
#             return redirect('home')

#     form = ContactForm()
#     return render(request, 'blog/contact.html', {'form': form})


def detail(request, slug):

    post = Post.objects.filter(status=1,slug=slug).first()
    context = {'post':post}

    return render(request, 'blog/detail.html', context)


def search(request):
    query = request.GET['query']
    if len(query)>50:
        posts= Post.objects.none()

    else:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

    params = {'posts':posts, 'query':query}
    return render(request, 'blog/search.html', params)

def handleLogin(request):
    if request.method=="POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername, password = loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect("home")
        else:
            messages.warning(request, "Wrong credentials, PLease enter your credentials carefully.")
            return redirect("home")
    return HttpResponse("404-NOT FOUND")

    return HttpResponse("login")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("home")

def handleSignup(request):
    if request.method=="POST":
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #check for errorneous input
        if len(username)>10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')


        #create the user 
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " User account successfully created!")
        return redirect("home")
    else:
        return HttpResponse("404 Error")


