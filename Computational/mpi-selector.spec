Summary: Provides site-wide and per-user MPI implementation selection
Name: mpi-selector
Version: 1.0.2
Release: 1%{?dist}
License: BSD
Group: System Environment/Base
Source: mpi-selector-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf
BuildArch: noarch

%description
A simple tool that allows system administrators to set a site-wide
default for which MPI implementation is to be used, but also allow
users to set their own default MPI implementation, thereby overriding
the site-wide default.

The default can be changed easily via the mpi-selector command --
editing of shell startup files is not required.

%prep
%setup -q

%build
# We have to rebuild the configure file because the one that ships with
# the tarball is broken and ignores our configure directives
autoconf
# There's very little to do in this section: configure and make
%configure --localstatedir=%{_localstatedir}/lib --with-shell-startup-dir=/etc/profile.d
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
# Remove the execute bits from the shell files, they aren't needed
chmod -x ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/*
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}/data

%clean
rm -rf $RPM_BUILD_ROOT 

%files
%defattr(-, root, root, -)
%doc README LICENSE
%{_bindir}/mpi-selector
%{_bindir}/mpi-selector-menu
%{_mandir}/man1/mpi-selector.*
%{_mandir}/man1/mpi-selector-menu.*
%{_sysconfdir}/profile.d/mpi-selector.sh
%{_sysconfdir}/profile.d/mpi-selector.csh
%dir %{_localstatedir}/lib/%{name}


%changelog
* Fri Apr 17 2009 Doug Ledford <dledford@redhat.com> - 1.0.2-1
- Update to ofed 1.4.1-rc3 version
- Related: bz459652

* Wed Sep 17 2008 Doug Ledford <dledford@redhat.com> - 1.0.1-1
- Update to latest upstream version
- Resolves: bz462585

* Wed Apr 02 2008 Doug Ledford <dledford@redhat.com> - 1.0.0-2
- Make the package a noarch package

* Tue Apr 01 2008 Doug Ledford <dledford@redhat.com> - 1.0.0-1
- Initial import into Red Hat repo management

* Wed Feb 14 2007 Jeff Squyres <jsquyres@cisco.com>
- First version
