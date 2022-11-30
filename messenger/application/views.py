from django.contrib.auth import authenticate, login as login_user
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def home(request):
    return render(request, "home.html")


@require_http_methods(["GET", "POST"])
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        form = add_field_placeholders(form)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login_user(request, user)
                return redirect(reverse("home"))
        return render(
            request,
            "login.html",
            context={"login_form": form, "error": "Invalid username or password"},
        )
    form = AuthenticationForm()
    form = add_field_placeholders(form)
    return render(request, "login.html", context={"login_form": form})

def add_field_placeholders(form):
    for field_name, field in form.fields.items():
        form.fields[field_name].widget.attrs['placeholder'] = field.label
    return form

