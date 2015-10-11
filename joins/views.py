from django.shortcuts import render, HttpResponseRedirect, Http404
from .forms import EmailForm, JoinForm
from .models import Join
import uuid
from django.contrib.sites.models import Site

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
    try:
        join_obj = Join.objects.get(ref_id=ref_id)
        obj = Join.objects.filter(friend=join_obj)
        count = join_obj.referral.all().count()
        context = {"ref_id": join_obj.ref_id, "count": count, "ref_url": "http://%s/?ref=%s" % (Site.objects.get_current().domain, join_obj.ref_id)}
        template = "share.html"
    except Exception, e:
        print str(e)
        raise Http404
    return render(request, template, context)


def home(request):
    try:
        refer_id = request.session['ref']
        obj = Join.objects.get(id=refer_id)
    except:
        obj = None

    form = JoinForm(request.POST or None)
    if form.is_valid():
        new_join = form.save(commit=False)
        email = form.cleaned_data["email"]
        new_join_old, created = Join.objects.get_or_create(email=email)
        if created:
            new_join_old.ip_address = get_ip(request)
            new_join_old.ref_id = get_ref_id()
            if obj :
                new_join_old.friend = obj
            new_join_old.save()
        #redirect
        return HttpResponseRedirect("/%s" % (new_join_old.ref_id))

    context = {"form": form}
    template = "home.html"
    return render(request, template, context)