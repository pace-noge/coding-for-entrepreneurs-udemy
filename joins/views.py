from django.shortcuts import render, HttpResponseRedirect
from .forms import EmailForm, JoinForm
from .models import Join
import uuid


def get_ip(request):
    try:
        x_forwarded = request.META.get("HTTP_X_FORWARDED")
        if x_forwarded:
            ip = x_forwarded.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip


def get_ref_id():
    ref_id = str(uuid.uuid4())[:11].replace('-', '').lower()
    try:
        id_exists = Join.objects.get(ref_id=ref_id)
        get_ref_id()
    except:
        return ref_id


def share(request, ref_id):
    context = {"ref_id":ref_id}
    template = "home.html"
    return render(request, template, context)


def home(request):
    form = JoinForm(request.POST or None)
    if form.is_valid():
        new_join = form.save(commit=False)
        email = form.cleaned_data["email"]
        new_join_old, created = Join.objects.get_or_create(email=email)
        if created:
            new_join_old.ip_address = get_ip(request)
            new_join_old.ref_id = get_ref_id()
            new_join_old.save()
        #redirect
        return HttpResponseRedirect("/%s" % (new_join_old.ref_id))

    context = {"form": form}
    template = "home.html"
    return render(request, template, context)