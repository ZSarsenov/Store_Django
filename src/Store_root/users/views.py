from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required


from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket

# контроллер для входа
def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print('POST')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context=context)


# контроллер для регистрации
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Вы успешно зарегестрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context=context)


# контроллер для профиля
@login_required()
def profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=user)

    # вариант решения номер #1
    baskets = Basket.objects.filter(user=user)
    total_quontity = sum(basket.quontity for basket in baskets)
    total_sum = sum(basket.sum() for basket in baskets)

    # вариант решения номер #2
    """total_quontity = 0
    total_sum = 0
    for basket in baskets:
        total_quontity += basket.quontity
        total_sum += basket.sum()"""

    context = {'form': form,
               'baskets': baskets,
               'total_quontity': total_quontity,
               'total_sum': total_sum
    }
    return render(request, 'users/profile.html', context=context)
