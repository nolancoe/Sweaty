from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, AccountSettingsForm, PasswordChangingForm, ProfilePageForm, AccountAuthenticationForm
from core.models import user_profile
from django.contrib.auth import login, authenticate, logout


class CreateProfilePageView(generic.CreateView):
    model = user_profile
    form_class = ProfilePageForm
    template_name = 'registration/create_user_profile_page.html'


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditProfilePageView(generic.UpdateView):
    model = user_profile
    template_name = 'registration/edit_profile_page.html'
    fields = ['gamertag', 'profile_pic']
    success_url = reverse_lazy('home')


def ShowProfilePageView(request, *args, **kwargs):
    """
    - Logic here is kind of tricky
        is_self
        is_friend
            -1: NO_REQUEST_SENT
            0: THEM_SENT_TO_YOU
            1: YOU_SENT_TO_THEM
    """
    context = {}
    user_id = kwargs.get("user_id")
    try:
        user_profile = user_profile.objects.get(pk=user_id)
    except:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = user_profile.id
        context['username'] = user_profile.username
        context['email'] = user_profile.email
        context['profile_pic'] = user_profile.profile_pic.url
        context['hide_email'] = user_profile.hide_email

        try:
            friend_list = FriendList.objects.get(user=user_profile)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=user_profile)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends'] = friends

        # Define template variables
        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # range: ENUM -> friend/friend_request_status.FriendRequestStatus
        friend_requests = None
        user = request.user_profile
        if user.is_authenticated and user != account:
            is_self = False
            if friends.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                # CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
                # CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                # CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

        elif not user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            except:
                pass

        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests
        context['BASE_URL'] = settings.BASE_URL
        return render(request, "registration/profile_page.html", context)


class ShowProfilePageView(DetailView):
    model = user_profile
    template_name = 'registration/profile_page.html'

    def get_context_data(self, *args, **kwargs):
        users = user_profile.objects.all()
        context = super(ShowProfilePageView,self).get_context_data( *args, **kwargs)

        page_user = get_object_or_404(user_profile, id=self.kwargs['pk'])

        context["page_user"] = page_user
        return context

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'registration/password_success.html', {})


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class AccountSettingsView(generic.UpdateView):
    model = user_profile
    template_name = 'registration/account_settings.html'
    fields = '__all__'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "registration/login.html", context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect

def logout_view(request):
    logout(request)
    return redirect("home")
