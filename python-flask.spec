#
# Conditional build:
%bcond_without  doc             # don't build doc
%bcond_with  tests   # do not perform "make test"
%bcond_without  python2 # CPython 2.x module
%bcond_without  python3 # CPython 3.x module


%define 	module	flask
Summary:	A microframework based on Werkzeug, Jinja2 and good intentions
Name:		python-%{module}
Version:	0.10.1
Release:	3
License:	BSD
Group:		Development/Languages/Python
# https://pypi.python.org/packages/source/F/Flask/Flask-0.10.1.tar.gz
Source0:	http://pypi.python.org/packages/source/F/Flask/Flask-%{version}.tar.gz
# Source0-md5:	378670fe456957eb3c27ddaef60b2b24
URL:		http://flask.pocoo.org/
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	python-distribute
BuildRequires:	python-jinja2 >= 2.4
BuildRequires:	python-werkzeug >= 0.6.1
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219

%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-jinja2 >= 2.4
BuildRequires:	python3-modules
BuildRequires:	python3-werkzeug >= 0.6.1
%endif

Requires:	python-itsdangerous
Requires:	python-jinja2 >= 2.4
Requires:	python-modules
Requires:	python-werkzeug >= 0.6.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Flask is a microframework for Python based on Werkzeug, Jinja 2 and
good intentions.

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-itsdangerous
Requires:	python3-jinja2 >= 2.4
Requires:	python3-modules
Requires:	python3-werkzeug >= 0.6.1

%description -n python3-%{module}
Flask is a microframework for Python based on Werkzeug, Jinja 2 and
good intentions.

# %description -n python3-%{module} -l pl.UTF-8


%prep
%setup -q -n Flask-%{version}

%build
%if %{with python2}
# CC/CFLAGS is only for arch packages - remove on noarch packages
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
# CC/CFLAGS is only for arch packages - remove on noarch packages
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
        build --build-base build-2 \
        install --skip-build \
        --optimize=2 \
        --root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
        build --build-base build-3 \
        install --skip-build \
        --optimize=2 \
        --root=$RPM_BUILD_ROOT
%endif

# in case there are examples provided
%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
        | xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif



%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES README
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/Flask-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/Flask-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif
