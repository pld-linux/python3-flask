#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module	flask
Summary:	A microframework based on Werkzeug, Jinja2 and good intentions
Summary(pl.UTF-8):	Mikroszkielet oparty na Werkzeugu, Jinja2 i dobrych intencjach
Name:		python3-%{module}
Version:	3.1.2
Release:	1
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.python.org/simple/Flask
Source0:	https://files.pythonhosted.org/packages/source/F/Flask/flask-%{version}.tar.gz
# Source0-md5:	62ae81cf2e91a376af909a2bc8939e15
Patch0:		0001-Don-t-require-sphinxcontrib.log_cabinet-extension.patch
URL:		https://flask.palletsprojects.com/
%if %{with tests} && %(locale -a | grep -q '^C\.UTF-8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python3-build
BuildRequires:	python3-flit_core < 4
BuildRequires:	python3-installer
BuildRequires:	python3-devel >= 1:3.9
%if %{with tests}
BuildRequires:	python3-asgiref >= 3.2
BuildRequires:	python3-blinker >= 1.9.0
BuildRequires:	python3-click >= 8.1.3
# optional
#BuildRequires:	python3-dotenv
%if "%{_ver_lt %{py3_ver} 3.10}" == "1"
BuildRequires:	python3-importlib_metadata >= 3.6.0
%endif
BuildRequires:	python3-itsdangerous >= 2.2.0
BuildRequires:	python3-jinja2 >= 3.1.2
BuildRequires:	python3-markupsafe >= 2.1.1
BuildRequires:	python3-pytest
BuildRequires:	python3-werkzeug >= 3.1.0
%endif
%if %{with doc}
BuildRequires:	python3-pallets-sphinx-themes
BuildRequires:	python3-sphinx_tabs
BuildRequires:	sphinx-pdg-3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-asgiref >= 3.2
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Flask is a microframework for Python based on Werkzeug, Jinja 2 and
good intentions.

%description -l pl.UTF-8
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
%setup -q -n flask-%{version}
%patch -P 0 -p1

%build
%py3_build_pyproject

%if %{with tests} || %{with doc}
# one test and docs require package metadata
%{__python3} -m zipfile -e build-3/*.whl build-3-test
%endif

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-3-test \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/flask{,-3}

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.md
%attr(755,root,root) %{_bindir}/flask-3
%{py3_sitescriptdir}/flask
%{py3_sitescriptdir}/flask-%{version}.dist-info
%{_examplesdir}/python3-%{module}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,deploying,patterns,tutorial,*.html,*.js}
%endif
