from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404, render
from .forms import SearchForm, OrderForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})


def about(request):
    if 'about_visits' in request.COOKIES:
        visit_count = int(request.COOKIES['about_visits'])
        visit_count += 1
    else:
        visit_count = 1
        
    response = render(request, 'myapp/about.html', {'number_of_visits': visit_count})
    response.set_cookie('about_visits', visit_count, max_age=300)
    return response


def detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    courses = Course.objects.filter(topic=Topic.objects.get(id=1))
    return render(request, 'myapp/detail.html', {'topic': topic, 'courses': courses})


def findcourses(request):
    # breakpoint()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            max_price = form.cleaned_data['max_price']

            if length == 0:
                courselist = Course.objects.filter(price__lte=max_price)
            else:
                courselist = Course.objects.filter(topic__length=length, price__lte=max_price)
            return render(request, 'myapp/results.html', {'courselist': courselist, 'name':name, 'length': length})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findcourses.html', {'form':form})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=False)
            student = order.student
            status = order.order_status
            order.save()
            form.save_m2m()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)
            return render(request, 'myapp/order_response.html', {'courses': courses, 'order': order})
        else:
            return render(request, 'myapp/place_order.html', {'form':form})

    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form})


def review_view(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                review = form.save(commit=False)
                course = review.course
                course.num_reviews = course.num_reviews + 1
                review.save()
                course.save()
                return index(request)
            else:
                error_msg = "You must enter a rating between 1 and 5!"
                return render(request, 'myapp/review.html', {'form': form, 'error_msg': error_msg})
        else:
            return HttpResponse("Invalid Data")
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                current_time = datetime.now()
                request.session['last_login'] = str(current_time.ctime())
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


def myaccount(request):
    try:
        current_user = Student.objects.get(id=request.user.id)
    except Student.DoesNotExist:
        current_user = None

    if current_user:
        registered_courses = current_user.registered_courses.all()
        interested_topics = current_user.interested_in.all()

        return render(request, 'myapp/myaccount.html', {'first_name': current_user.first_name,
                                                       'last_name': current_user.last_name,
                                                       'interested_topics': interested_topics,
                                                       'registered_courses': registered_courses})
    else:
        return HttpResponse("<p>You are not a registered student</p>")
