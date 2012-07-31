# local installation point for modules
%define localmoduledir /usr/local/share/Modules/modulefiles
%define optmoduledir /opt/share/Modules/modulefiles

Name:           environment-modules
Version:        3.2.7b
Epoch:		1
Release:        7.3%{?dist}
Summary:        Provides dynamic modification of a user's environment

Group:          System Environment/Base
License:        GPLv2+
URL:            http://modules.sourceforge.net/
Source0:        http://downloads.sourceforge.net/modules/modules-%{version}.tar.bz2
Source1:        modules.sh
Source2:        createmodule.sh
Source10:	modulecmd.tcl
Source11:	modulecmd.tcl.old
Source12:	modulecmd.tcl.original
Source13:	modulecmd.tcl.original.new
Patch0:         environment-modules-3.2.7-bindir.patch
Patch1:         environment-modules-3.2.7-manpath.patch
Patch10:	modules-pbstweak.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  tcl-devel, tclx-devel, libX11-devel
BuildRequires:  man
#For ps in startup script
Requires:       procps
Requires:	tcl, tclx

%description
The Environment Modules package provides for the dynamic modification of
a user's environment via modulefiles.

Each modulefile contains the information needed to configure the shell
for an application. Once the Modules package is initialized, the
environment can be modified on a per-module basis using the module
command which interprets modulefiles. Typically modulefiles instruct
the module command to alter or set shell environment variables such as
PATH, MANPATH, etc. modulefiles may be shared by many users on a system
and users may have their own collection to supplement or replace the
shared modulefiles.

Modules can be loaded and unloaded dynamically and atomically, in an
clean fashion. All popular shells are supported, including bash, ksh,
zsh, sh, csh, tcsh, as well as some scripting languages such as perl.

Modules are useful in managing different versions of applications.
Modules can also be bundled into metamodules that will load an entire
suite of different applications.

NOTE: You will need to get a new shell after installing this package to
have access to the module alias.


%prep
%setup -q -n modules-3.2.7
%patch0 -p1 -b .bindir
%patch1 -p1 -b .manpath
%patch10 -p1 -b .pbstweak

%build
export CPPFLAGS=-DMANPATH=\'\"`manpath`\"\'
%configure --disable-versioning \
           --prefix=%{_datadir} \
           --exec-prefix=%{_datadir}/Modules \
           --with-module-path=%{_sysconfdir}/modulefiles

#           --with-debug=42 --with-log-facility-debug=stderr
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cp -p %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/modules.sh
cp -p %SOURCE2 $RPM_BUILD_ROOT%{_datadir}/Modules/bin
ln -s %{_datadir}/Modules/init/csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/modules.csh
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modulefiles

mv  $RPM_BUILD_ROOT%{_bindir}/modulecmd $RPM_BUILD_ROOT%{_bindir}/modulecmd.bin
install -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/modulecmd

cat >> $RPM_BUILD_ROOT/%{_datadir}/Modules/init/.modulespath <<ENDLOCALMODULESPATH
%{localmoduledir}
%{optmoduledir}
ENDLOCALMODULESPATH

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.GPL README TODO
%{_sysconfdir}/modulefiles
%{_sysconfdir}/profile.d/*
%{_bindir}/modulecmd*
%{_datadir}/Modules/
%{_mandir}/man1/module.1.gz
%{_mandir}/man4/modulefile.4.gz


%changelog
* Fri Jul 23 2010 Josko Plazonic <plazonic@math.princeton.edu>
- use tcl version plus a tweak or two

* Thu Jan 7 2010 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-7
- Add patch to set a sane default MANPATH
- Add createmodule.sh utility script for creating modulefiles
 
* Mon Nov 30 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-6
- Add Requires: propcs (bug #54272)

* Mon Oct 26 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-5
- Don't assume different shell init scripts exist (bug #530770)

* Fri Oct 23 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-4
- Don't load bash init script when bash is running as "sh" (bug #529745)

* Mon Oct 19 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-3
- Support different flavors of "sh" (bug #529493)

* Wed Sep 23 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-2
- Add patch to fix modulecmd path in init files

* Wed Sep 23 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-1
- Update to 3.2.7b

* Mon Sep 21 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7-1
- Update to 3.2.7, fixes bug #524475
- Drop versioning patch fixed upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 3 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-6
- Change %%patch -> %%patch0

* Fri Mar 14 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-5
- Add BR libX11-devel so modulecmd can handle X resources

* Wed Mar  5 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-4
- Add patch to fix extraneous version path entry properly
- Use --with-module-path to point to /etc/modulefiles for local modules,
  this also fixes bug #436041

* Sat Feb  9 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-3
- Rebuild for gcc 3.4

* Thu Jan 03 2008 - Alex Lancaster <alexlan at fedoraproject.org> - 3.2.6-2
- Rebuild for new Tcl (8.5).

* Fri Nov  2 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-1
- Update to 3.2.6

* Tue Aug 21 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.5-2
- Update license tag to GPLv2

* Fri Feb 16 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.5-1
- Update to 3.2.5

* Wed Feb 14 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.4-2
- Rebuild for Tcl downgrade

* Fri Feb 09 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.4-1
- Update to 3.2.4

* Wed Dec 20 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-3
- Add --with-version-path to set VERSIONPATH (bug 220260)

* Tue Aug 28 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-2
- Rebuild for FC6

* Fri Jun  2 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-1
- Update to 3.2.3

* Fri May  5 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.2-1
- Update to 3.2.2

* Fri Mar 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-1
- Update to 3.2.1

* Thu Feb  9 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0p1-1
- Update to 3.2.0p1

* Fri Jan 27 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0-2
- Add profile.d links

* Tue Jan 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0-1
- Fedora Extras packaging
