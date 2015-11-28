# TODO
# - patch to use system .mo directly

# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define		subver	a1
%define		rel		2
%define 	module	colander
Summary:	A simple schema-based serialization and deserialization library
Name:		python-%{module}
Version:	1.0
Release:	0.%{subver}.%{rel}
License:	BSD-derived (http://www.repoze.org/LICENSE.txt)
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/c/colander/colander-%{version}%{subver}.tar.gz
# Source0-md5:	999f209bf6757b4e7045b3b56591a0eb
URL:		http://docs.pylonsproject.org/projects/colander/
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with tests}
BuildRequires:	python-translationstring
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An extensible package which can be used to:
- deserialize and validate a data structure composed of strings,
  mappings, and lists.
- serialize an arbitrary data structure to a data structure composed
  of strings, mappings, and lists.

%prep
%setup -q -n %{module}-%{version}%{subver}

%build
%py_build

%{?with_tests:%{__python} setup.py test}

%install
rm -rf $RPM_BUILD_ROOT
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/tests
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/locale/%{module}.pot
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/locale/*/LC_MESSAGES/%{module}.po

install -d $RPM_BUILD_ROOT%{_localedir}
mv $RPM_BUILD_ROOT{%{py_sitescriptdir}/%{module}/locale/*,%{_localedir}}
rmdir $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/locale
# TODO: patch that the symlink won't be needed
ln -s %{_localedir} $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/locale

mv $RPM_BUILD_ROOT%{_localedir}/{de_DE,de}
mv $RPM_BUILD_ROOT%{_localedir}/{zh,zh_CN}

%find_lang %{module}

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{module}.lang
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.txt
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%{py_sitescriptdir}/%{module}-%{version}*.egg-info
%{py_sitescriptdir}/%{module}/locale
