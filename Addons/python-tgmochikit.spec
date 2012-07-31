%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global srcname tgMochiKit

Name:           python-tgmochikit
Version:        1.4.2
Release:        2%{?dist}
Summary:        MochiKit JavaScript library packaged for TurboGears widgets

Group:          Development/Languages
# The getElementPosition function is under the BSD license (adapted from the YUI library)
# everything else is (MIT or AFL)
License:        BSD and (MIT or AFL)
URL:            http://docs.turbogears.org/%{srcname}
Source0:        http://pypi.python.org/packages/source/t/%{srcname}/%{srcname}-%{version}.tar.gz
Patch0: tgmochikit-license.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-nose
BuildRequires:  dos2unix
Requires: python-setuptools

%description
MochiKit is a highly-documented and well-tested suite of JavaScript libraries
that will help you get stuff done, fast.

tgmochikit packages the MochiKit library for use by TurboGears Widgets.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1 -b .licensing

dos2unix README.txt

%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%check
nosetests

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt ChangeLog
# For noarch packages: sitelib
%{python_sitelib}/*


%changelog
* Thu Dec 2 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4.2-2
- Fix mixed use of RPM_BUILD_ROOT env var and %%buildroot macro.
- Fix licensing as there's some BSD code as well.

* Thu Dec 2 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4.2-1
- Initial Fedora build
