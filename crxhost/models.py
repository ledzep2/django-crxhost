from django.db import models
from django.conf import settings

import datetime

import crxhost.utils as utils


class CRXId(models.Model):
    name = models.CharField(max_length = 255, blank = False, default = '', help_text = "CRX package name without version number")
    cid = models.CharField(max_length = 255, blank = True, help_text = "extension or app id")
    active = models.BooleanField(default = True, blank = True)

    def __unicode__(self):
        return self.name

class CRXPackage(models.Model):

    def crx_upload_path_gen(instance, filename):
        ret = utils.break_filename(filename)
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "%s-%s-%s.crx" % (ret['crxname'], ret['version'], now)
        return "%s/%s" % (ret['crxname'], filename)

    crx = models.ForeignKey(CRXId, blank = True, null = True)
    original_version = models.CharField(max_length = 32, blank = True, default = '', help_text = "The version number parsed from the filename of the uploaded package")
    generated_version = models.CharField(max_length = 32, blank = True, default = '', help_text = "The version number combining original_version and auto incremented build number")
    package = models.FileField(upload_to = getattr(settings, "CRX_UPLOAD_PATH", crx_upload_path_gen), blank = False)
    timestamp = models.DateTimeField(auto_now_add = True)
    active = models.BooleanField(default = True)

    def __unicode__(self):
        return u"%s-%s" % (unicode(self.crx), self.generated_version)

    def generate_version(self, original_version):
        if getattr(settings, "CRX_GENERATE_VERSION", True) == True:
            build = 1

            t = CRXPackage.objects.filter(crx = self.crx, original_version = original_version).values('generated_version').order_by('-id')
            if len(t):
                v = t[0]['generated_version']
                if v != original_version:
                    build = int(v.split('.')[-1]) + 1
            generated_version = '%s.%d' % (original_version, build)
        else:
            generated_version = original_version

        return generated_version

    def package_name(self):
        return "%s-%s.crx" % (self.crx.name, self.generated_version)

    def save(self, *args, **kwargs):
        attrs = utils.break_filename(self.package.name)
        if not self.crx:
            try:
                crx = CRXId.objects.get(name = attrs['crxname'])
            except CRXId.DoesNotExist:
                crx = CRXId(name = attrs['crxname'])
                crx.save()
            self.crx = crx

        self.original_version = self.original_version or attrs['version']

        if not self.generated_version:
            self.generated_version = self.generate_version(attrs['version'])

        super(CRXPackage, self).save(*args, **kwargs)

__all__ = ("CRXId", "CRXPackage")