from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404, render
from .forms import SearchForm, OrderForm, ReviewForm, ForgotPasswordForm, RegisterForm, loginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from django.views import View
from django.core.mail import send_mail


# Create your views here.
# def index(request):
#     top_list = Topic.objects.all().order_by('id')[:10]
#     return render(request, 'myapp/index.html', {'top_list': top_list})


class IndexView(View):
    def get(self, request):
        top_list = Topic.objects.all().order_by('id')[:10]
        try:
            current_user = Student.objects.get(id=request.user.id)
        except Student.DoesNotExist:
            current_user = None
        first_name = "User"
        if current_user:
            first_name = current_user.first_name

        return render(request, 'myapp/index.html', {'top_list': top_list, 'first_name':first_name})


def about(request):
    try:
        current_user = Student.objects.get(id=request.user.id)
    except Student.DoesNotExist:
        current_user = None
    first_name = "User"
    if current_user:
        first_name = current_user.first_name

    if 'about_visits' in request.COOKIES:
        visit_count = int(request.COOKIES['about_visits'])
        visit_count += 1
    else:
        visit_count = 1
        
    response = render(request, 'myapp/about.html', {'number_of_visits': visit_count,'first_name':first_name})
    response.set_cookie('about_visits', visit_count, max_age=300)

    return response


# def detail(request, topic_id):
#     topic = get_object_or_404(Topic, id=topic_id)
#     courses = Course.objects.filter(topic=Topic.objects.get(id=1))
#     return render(request, 'myapp/detail.html', {'topic': topic, 'courses': courses})


class DetailView(View):
    def get(self, request, topic_id):

        try:
            current_user = Student.objects.get(id=request.user.id)
        except Student.DoesNotExist:
            current_user = None
        first_name = "User"
        if current_user:
            first_name = current_user.first_name

        topic = get_object_or_404(Topic, id=topic_id)
        courses = Course.objects.filter(topic=Topic.objects.get(id=1))
        return render(request, 'myapp/detail.html', {'topic': topic, 'courses': courses,'first_name':first_name})


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
    try:
        current_user = Student.objects.get(id=request.user.id)
    except Student.DoesNotExist:
        current_user = None
    first_name = "User"
    if current_user:
        first_name = current_user.first_name

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
            return render(request, 'myapp/order_response.html', {'courses': courses, 'order': order,'first_name':first_name})
        else:
            return render(request, 'myapp/place_order.html', {'form':form,'first_name':first_name})

    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form,'first_name':first_name})


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
                return redirect('myapp:index')
            else:
                error_msg = "You must enter a rating between 1 and 5!"
                return render(request, 'myapp/review.html', {'form': form, 'error_msg': error_msg})
        else:
            return HttpResponse("Invalid Data")
    else:
        form = None
        error_msg = None
        try:
            current_user = Student.objects.get(id=request.user.id)
        except Student.DoesNotExist:
            current_user = None
        if current_user:
            level = current_user.level
            if current_user.level not in ('UG', 'PG'):
                error_msg = "Only Undergraduate or Postgraduate students can submit the review."
            else:
                form = ReviewForm()
        else:
            error_msg = "Please sign-in to submit a review."
        return render(request, 'myapp/review.html', {'form': form, 'error_msg': error_msg})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            if user:
                if user.is_active:
                    login(request, user)
                    last_login = datetime.now()
                    request.session['last_login'] = str(last_login)
                    return HttpResponseRedirect(reverse('myapp:myaccount'))
                else:
                    return HttpResponse('Your account is disabled.')
            else:
                return HttpResponse('Invalid login details.')
        else:
            return HttpResponse("Please enable cookies to continue")
    else:
        request.session.set_test_cookie()
        form = loginForm()
        return render(request, 'myapp/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


@login_required(login_url='/myapp/login')
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


def myOrder(request):
    try:
        if request.user.is_authenticated:
            student = Student.objects.get(id=request.user.id)
            if student:
                user = get_object_or_404(Student, pk=request.user.id)
                order_list = Order.objects.filter(student=student)
                if order_list.exists():
                    return render(request, 'myapp/myorder.html', {'user': user, 'order_list': order_list})
                else:
                    return HttpResponse("you have not ordered anything yet")
            else:
                return HttpResponse("User not found")
    except:
        return HttpResponse("you are not registered as a student")


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = Student.objects.get(username=username)
            except Student.DoesNotExist:
                user = None

            if user:
                email_address = user.email
                new_password = "{}1234".format(username)
                email_content = "Your new password is {}".format(new_password)
                message = "New password has been sent to your registered email address {}".format(email_address)
                send_mail(
                    subject='New Password',
                    message=email_content,
                    from_email="arpitkpatel29@gmail.com",
                    recipient_list=[email_address]
                )
                return render(request, 'myapp/forgot_password.html', {'form': form, 'message': message})
            else:
                message = "Provided Username does not exists"
                return render(request, 'myapp/forgot_password.html', {'form': form, 'message': message})
    else:
        form = ForgotPasswordForm()
        return render(request, 'myapp/forgot_password.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['registered_courses']
            topics = form.cleaned_data['interested_in']

            student = form.save(commit=False)
            student.set_password(form.cleaned_data['password1'])

            student.save()
            rg = student.registered_courses
            it = student.interested_in
            for t in topics:
                it.add(t)

            for c in courses:
                rg.add(c)

            form.save()
            return HttpResponseRedirect(reverse('myapp:login'))
        else:
            return render(request, 'myapp/register.html', {'form':form})
    else:
        form = RegisterForm()
        return render(request, 'myapp/register.html', {'form': form})