from django.db import models
from django.conf import settings

import datetime, re, zipfile

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
        filename = "%s-%s.crx" % (filename, now)
        return "%s/%s" % (ret['crxname'], filename)

    crx = models.ForeignKey(CRXId, blank = True, null = True)
    version = models.CharField(max_length = 32, blank = True, default = '', help_text = "The version number parsed from the filename or manifest of the uploaded package")
    package = models.FileField(upload_to = getattr(settings, "CRX_UPLOAD_PATH", crx_upload_path_gen), blank = False)
    timestamp = models.DateTimeField(auto_now_add = True)
    downloaded = models.PositiveIntegerField(default = 0, blank = True)
    active = models.BooleanField(default = True)

    def __unicode__(self):
        return u"%s-%s" % (unicode(self.crx), self.version)

    def package_name(self):
        return "%s-%s.crx" % (self.crx.name, self.version)

    def save(self, *args, **kwargs):
        attrs = utils.break_filename(self.package.name)
        with zipfile.ZipFile(self.package, 'r') as f:
            manifest = f.read('manifest.json')
            ret = re.findall(r'"version"\:\s*"(.+)"', manifest)
            if ret and not ret[0].startswith('__'):
                attrs['version'] = ret[0]
            ret = re.findall(r'"name"\:\s*"(.+)"', manifest)
            if ret and not ret[0].startswith('__'):
                attrs['crxname'] = ret[0]

        if not self.crx:
            try:
                crx = CRXId.objects.get(name = attrs['crxname'])
            except CRXId.DoesNotExist:
                crx = CRXId(name = attrs['crxname'])
                crx.save()
            self.crx = crx

        self.version = self.version or attrs['version']

        super(CRXPackage, self).save(*args, **kwargs)

__all__ = ("CRXId", "CRXPackage")