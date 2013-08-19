django-crxhost
==============

A reusable Django app that hosts chrome versioned extension/app packages, providing updates.xml and downloading service.


Features
========

* Auto-generate build number
* Multiple extensions/apps
* Nginx x-sendfile support

Usage
=====

1. Include crxhost/urls.py
2. `manage.py syncdb`
3. Name your package name-x.x.x.crx
4. Go to django admin. Add a new crxpackage. Select the package and upload. Other fields will get populated automatically.
5. Visit `{% url crx_updates_xml %}` for updates.xml

Configure
=========

in settings.py

* **CRX_SENDFILE**: Use sendfile instead of HttpResponse
* **CRX_GENERATE_VRESION**: Generate a build number according to the latest package and append it to the version number.
