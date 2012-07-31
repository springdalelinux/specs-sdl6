%define         rc_subver     rc5

Summary:        ASCII art library
Name:           aalib
Version:        1.4.0
Release:        0.18.%{rc_subver}%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://aa-project.sourceforge.net/aalib/
Source0:        http://download.sourceforge.net/aa-project/%{name}-1.4%{rc_subver}.tar.gz
Patch0:         aalib-aclocal.patch
Patch1:         aalib-config-rpath.patch
Patch2:         aalib-1.4rc5-bug149361.patch
Patch3:         aalib-1.4rc5-rpath.patch
Patch4:		aalib-1.4rc5-x_libs.patch
Patch5:		aalib-1.4rc5-libflag.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  slang-devel libXt-devel gpm-devel ncurses-devel
BuildRequires:	autoconf libtool

%description
AA-lib is a low level gfx library just as many other libraries are. The
main difference is that AA-lib does not require graphics device. In
fact, there is no graphical output possible. AA-lib replaces those
old-fashioned output methods with a powerful ASCII art renderer. The API
is designed to be similar to other graphics libraries.

%package libs
Summary:        Library files for aalib
Group:          System/Libraries
Obsoletes:	aalib < 1.4.0-0.14
%description libs
This package contains library files for aalib.

%package devel
Summary:        Development files for aalib
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires(post):  /sbin/install-info
Requires(postun): /sbin/install-info

%description devel
This package contains header files and other files needed to develop
with aalib.


%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1 -b .bug149361
%patch3 -p1 -b .rpath
%patch4 -p1 -b .x_libs
%patch5 -p0 -b .libflag
# included libtool is too old, we need to rebuild
autoreconf -v -f -i

%build
%configure --disable-static  --with-curses-driver=yes --with-ncurses

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
rm -f $RPM_BUILD_ROOT{%{_libdir}/libaa.la,%{_infodir}/dir}

# clean up multilib conflicts
touch -r NEWS $RPM_BUILD_ROOT%{_bindir}/aalib-config $RPM_BUILD_ROOT%{_datadir}/aclocal/aalib.m4



%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/libaa.info %{_infodir}/dir 2>/dev/null || :

%preun devel
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/libaa.info %{_infodir}/dir \
    2>/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/aafire
%{_bindir}/aainfo
%{_bindir}/aasavefont
%{_bindir}/aatest
%{_mandir}/man1/aafire.1*

%files libs
%defattr(-,root,root,-)
%doc README COPYING ChangeLog NEWS
%{_libdir}/libaa.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/aalib-config
%{_mandir}/man3/*
%{_libdir}/libaa.so
%{_includedir}/aalib.h
%{_infodir}/aalib.info*
%{_datadir}/aclocal/aalib.m4

%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-0.18.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-0.17.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 18 2008 Caolán McNamara <caolanm@redhat.com> 1.4.0-0.16.rc5
- rebuild for new libgpm

* Mon Mar 24 2008 Garrick Staples <garrick@usc.edu> 1.4.0-0.15.rc5
- remove unnecessary link bloat from aalib-config
- libs package doesn't need to require base package
- move docs to libs package

* Thu Feb 14 2008 Garrick Staples <garrick@usc.edu> 1.4.0-0.14.rc5
- fix multilib conflicts by splitting out libs package and fix
  timestamps and aalib-config

* Wed Aug 15 2007 Garrick Staples <garrick@usc.edu> 1.4.0-0.13.rc5
- correct License: tag

* Fri May  4 2007 Bill Nottingham <notting@redhat.com> 1.4.0-0.12.rc5
- remove some dainbramage in ltconfig so it builds shared libs on ppc64

* Thu Oct 19 2006 Garrick Staples <garrick@usc.edu> 1.4.0-0.11.rc5
- incorrect subversion in previous two changelog entries

* Thu Oct 19 2006 Garrick Staples <garrick@usc.edu> 1.4.0-0.10.rc6
- Rebuild with ncurses support

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-0.8.rc6
- FE6 Rebuild

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-0.8.rc5
- Taking over as maintainer since Anvil has other priorities
- Long long due rebuild with new gcc for FC-5 (bug 185870)
- Add %%{?dist} tag
- Make release field comply with the Package Naming guidelines for
  pre releases. Luckily according to rpm 8 > rc5 so this can be done.
- Fix some rpmlint warnings
- Fix (remove) use of rpath

* Mon Nov 28 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.4.0-0.rc5.7
- Fix modular X dependencies.
- Rebuild against new slang.
- Disable static lib, not shipping it anyway.
- Prune unneeded libs from aalib-config (and corresponding deps from -devel).
- Don't use %%exclude.

* Mon Nov 21 2005 Warren Togami <wtogami@redhat.com> - 1.4.0-0.rc5.6
- remove .a
- XFree86-devel -> libX11-devel

* Fri Jul  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.4.0-0.rc5.5
- fix missing return value (#149361)

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.4.0-0.rc5.4
- rebuilt

* Thu Dec 16 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 1.4.0-0.rc5.3
- If Epoch is dropped, %%epoch must not be used anywhere else.

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 1.4.0-0.rc5.2
- Bump release for compatibility (still, it'll break *sigh*).
- Fix possible non zero exit status from %%install.
- Fix owning the entire man3/ directory.
- Pending possible changes : --with-ncurses & ncurses-devel build dep.

* Fri Jul 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.4.0-0.fdr.0.9.rc5
- Fix underquoted definition in aalib.m4 to appease aclocal >= 1.8.
- Avoid rpath in aalib-config.
- Split Requires for post and postun into two to work around a rpm bug.
- Other minor specfile improvements.

* Thu Aug 21 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.8.rc5
- devel package now requires info
- Rewrote scriplets
- buildroot -> RPM_BUILD_ROOT
- Moved info files into devel package

* Tue Aug  5 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.7.rc5
- Removed '-p /sbin/ldconfig' in post scriptlet

* Thu Apr 10 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.6.rc5
- Added missing gpm-devel *Requires

* Mon Apr  7 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.5.rc5
- Moved configure from prep to build section.
- Modified post* and pre* scriplets

* Thu Apr  3 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.4.rc5
- Fix things between exclude, rm -f, lib*.la, and infodir/dir things
- Added URL in Source0.

* Thu Apr  3 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.3.rc5
- Modified devel Requires:
- Removed gcc as requirement

* Wed Apr  2 2003 Dams <anvil[AT]livna.org> 0:1.4.0-0.fdr.0.2.rc5
- Applied spec modifications from Adrian Reber

* Tue Apr  1 2003 Dams <anvil[AT]livna.org>
- Initial build.
