Summary: OpenDX Examples
Name: dx-samples
Version: 4.4.0
Release: 6%{?dist}
URL: http://www.opendx.org/
Group: Documentation
Source0: http://opendx.npaci.edu/source/dxsamples-%{version}.tar.gz
Patch0: %{name}-rpm.patch
Patch1: %{name}-nojava.patch
License: IBM
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: dx
BuildRequires: autoconf
BuildRequires: automake
Requires: dx

%description
Examples for OpenDX.

%prep
%setup -q -n dxsamples-%{version}
%patch0 -p1 -b .r
%patch1 -p1 -b .nojava

%build
autoreconf --force --install
%configure --without-javadx

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc ChangeLog
%defattr(644,root,root,755)
%{_datadir}/dx/samples

%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.4.0-4
- fix license tag

* Wed Sep 20 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-3
- fixed BuildRequires:

* Mon Sep 12 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-2
- fixed Requires:

* Sat Sep 02 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-1
- initial build
- don't include java samples for now
