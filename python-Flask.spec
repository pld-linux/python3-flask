#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	Flask
Summary:	A microframework based on Werkzeug, Jinja2 and good intentions
Name:		python-%{module}
Version:	0.8
Release:	0.1
License:	BSD
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/F/Flask/%{module}-%{version}.tar.gz
# Source0-md5:	a5169306cfe49b3b369086f2a63816ab
URL:		http://flask.pocoo.org/
BuildRequires:	python-Jinja2 >= 2.4
BuildRequires:	python-Werkzeug >= 0.6.1
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-Jinja2 >= 2.4
Requires:	python-Werkzeug >= 0.6.1
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Flask is a microframework for Python based on Werkzeug, Jinja 2 and
good intentions.

%prep
%setup -q -n %{module}-%{version}

%build
%{__python} setup.py build

%{?with_tests:%{__python} setup.py test}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES README
%{py_sitescriptdir}/flask
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
