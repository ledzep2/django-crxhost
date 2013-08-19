from django.http import HttpResponse, Http404
from django.core.servers.basehttp import FileWrapper
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from .models import CRXPackage, CRXId

import os

def updates_xml(request):
    ret = []

    for crx in CRXId.objects.filter(active = True):

        objs = crx.crxpackage_set.filter(active = True).order_by("-timestamp")
        try:
            obj = objs[0]
            obj.cid = crx.cid;
            ret.append(obj)
        except:
            pass

    return render_to_response("crxhost/updates.xml", RequestContext(request, {
        "crxs": ret
    }), mimetype= 'text/xml')


def download(request, crxname, version):
    packages = CRXPackage.objects.filter(crx__name = crxname, generated_version = version)
    if not packages:
        raise Http404

    package = packages[0]
    if getattr(settings, "CRX_SENDFILE", False):
        response = HttpResponse(mimetype='application/x-chrome-extension')
        response['Content-Disposition'] = 'attachment; filename=%s' % package.package_name()
        response['X-Sendfile'] = package.package.path
    else:
        wrapper = FileWrapper(file(package.package.path, 'rb'))
        response = HttpResponse(wrapper, content_type = "application/x-chrome-extension")
        response['Content-Disposition'] = 'attachment; filename=%s' % package.package_name()
        response['Content-Length'] = os.path.getsize(package.package.path)

    return response