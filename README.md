django-crxhost
==============

A reusable Django app that hosts chrome versioned extension/app packages, providing updates.xml and downloading service.


Features
========

* Multiple extensions/apps
* Nginx x-sendfile support
* Download count

Usage
=====

1. Include crxhost/urls.py
2. `manage.py syncdb`
3. Go to django admin. Add a new crxpackage. Select the package and upload. Other fields will get populated automatically.
4. Visit `{% url crx_updates_xml %}` for updates.xml

Configure
=========

in settings.py

* **CRX_SENDFILE**: Use sendfile instead of HttpResponse
