include:
  - uwsgi


app-pkgs:
  pkg.installed:
    - names:
      - python-virtualenv
      - python-dev
      - python-pip
      - libxml2-dev


/home/vagrant/.venvs/vsq13:
  virtualenv.manage:
    - requirements: /vagrant/requirements.txt
    - no_site_packages: true
    - clear: false
    - require:
      - pkg: app-pkgs

virtualenvwrapper:
  pip.installed:
    - name: virtualenvwrapper


/vagrant/log:
  file.directory:
    - mode: 755
    - makedirs: True

nginx:
  pkg:
    - latest
  service:
    - running
    - watch:
      - file: nginxconf

nginxconf:
  file.managed:
    - name: /etc/nginx/conf.d/vsq.conf
    - source: salt://webserver/nginx.conf
    - template: jinja
    - makedirs: True
    - mode: 755
