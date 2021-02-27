#
# Conditional build:
%bcond_without  doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module

%define 	module	flask
Summary:	A microframework based on Werkzeug, Jinja2 and good intentions
Summary(pl.UTF-8):	Mikroszkielet oparty na Werkzeugu, Jinja2 i dobrych intencjach
Name:		python-%{module}
Version:	1.1.2
Release:	2
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.python.org/simple/Flask
Source0:	https://files.pythonhosted.org/packages/source/F/Flask/Flask-%{version}.tar.gz
# Source0-md5:	0da4145d172993cd28a6c619630cc19c
Patch0:		0001-Don-t-require-sphinxcontrib.log_cabinet-extension.patch
URL:		https://flask.palletsprojects.com/
%if %{with tests} && %(locale -a | grep -q '^C\.UTF-8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-click >= 5.1
BuildRequires:	python-itsdangerous >= 0.24
BuildRequires:	python-jinja2 >= 2.10.1
BuildRequires:	python-pytest
BuildRequires:	python-werkzeug >= 0.15
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-click >= 5.1
BuildRequires:	python3-itsdangerous >= 0.24
BuildRequires:	python3-jinja2 >= 2.10.1
BuildRequires:	python3-pytest
BuildRequires:	python3-werkzeug >= 0.15
%endif
%endif
%if %{with doc}
BuildRequires:	python3-pallets-sphinx-themes
BuildRequires:	python3-sphinx_issues
BuildRequires:	sphinx-pdg-3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Flask is a microframework for Python based on Werkzeug, Jinja 2 and
good intentions.

%description -l pl.UTF-8
Flask to mikroszkielet dla Pythona oparty na modułach Werkzeug i
Jinja2 oraz dobrych intencjach.

%package -n python3-%{module}
Summary:	A microframework based on Werkzeug, Jinja2 and good intentions
Summary(pl.UTF-8):	Mikroszkielet oparty na Werkzeugu, Jinja2 i dobrych intencjach
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
Flask is a microframework for Python based on Werkzeug, Jinja 2 and
good intentions.

%description -n python3-%{module} -l pl.UTF-8
Flask to mikroszkielet dla Pythona oparty na modułach Werkzeug i
Jinja2 oraz dobrych intencjach.

%package apidocs
Summary:	Documentation for Python Flask package
Summary(pl.UTF-8):	Dokumentacja do pakietu Pythona Flask
Group:		Documentation

%description apidocs
Documentation for Python Flask package.

%description apidocs -l pl.UTF-8
Dokumentacja do pakietu Pythona Flask.

%prep
%setup -q -n Flask-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/flask{,-3}

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/flask{,-2}
ln -sf flask-2 $RPM_BUILD_ROOT%{_bindir}/flask

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.rst README.rst
%attr(755,root,root) %{_bindir}/flask
%attr(755,root,root) %{_bindir}/flask-2
%{py_sitescriptdir}/flask
%{py_sitescriptdir}/Flask-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.rst README.rst
%attr(755,root,root) %{_bindir}/flask-3
%{py3_sitescriptdir}/flask
%{py3_sitescriptdir}/Flask-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,deploying,patterns,tutorial,*.html,*.js}
%endif
