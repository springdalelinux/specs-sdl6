Name: gretl		
Version: 1.9.5	
Release:	1%{?dist}
Summary: A tool for econometric analysis	

Group: Applications/Engineering
License: GPLv3+ and BSD and MIT
URL: http://gretl.sourceforge.net/
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
#Licensing of plugins used in gretl
Source1: gretl_plugins.txt

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: desktop-file-utils
BuildRequires:	gtk2-devel
BuildRequires:	glib2-devel
BuildRequires:	blas-devel
BuildRequires:	fftw-devel
BuildRequires:	gettext
BuildRequires:	libxml2-devel
BuildRequires:	gtksourceview-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	lapack-devel
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	gmp-devel
BuildRequires:	mpfr-devel
BuildRequires:	gnuplot
BuildRequires: gnu-free-sans-fonts
BuildRequires: bitstream-vera-sans-mono-fonts
BuildRequires: bitstream-vera-sans-fonts

Requires: gnuplot
Requires: gtksourceview
Requires: gnu-free-sans-fonts
Requires: bitstream-vera-sans-mono-fonts
Requires: bitstream-vera-sans-fonts

%description
A cross-platform software package for econometric analysis, 
written in the C programming language.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the development files for %{name}.

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}
cp %{SOURCE1} %{_builddir}/%{name}-%{version}/gretl_plugins.txt



%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%find_lang %{name}
rm -rf %{buildroot}/%{_libdir}/libgretl*.la
rm -rf %{buildroot}/%{_libdir}/gretl-gtk2/*.la

#font installation
rm -rf %{buildroot}/%{_datadir}/%{name}/fonts/*
ln -s %{_datadir}/fonts/bitstream-vera/Vera.ttf %{buildroot}/%{_datadir}/%{name}/fonts/Vera.ttf
ln -s %{_datadir}/fonts/bitstream-vera/VeraMono.ttf %{buildroot}/%{_datadir}/%{name}/fonts/VeraMono.ttf
ln -s %{_datadir}/fonts/gnu-free/FreeSans.ttf %{buildroot}/%{_datadir}/%{name}/fonts/FreeSans.ttf

rm -rf %{buildroot}/%{_datadir}/%{name}/doc

desktop-file-install						\
--remove-category="Application;Science;Econometrics" \
--add-category="Education;Science;Math;Economy;"  \
--dir=%{buildroot}%{_datadir}/applications     \
%{buildroot}/%{_datadir}/applications/gretl.desktop



%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/gretl*
%{_libdir}/gretl-gtk2
%{_datadir}/%{name}/
%{_mandir}/man1/*.gz
%{_libdir}/libgretl-1.0.so.*
%{_datadir}/mime-info/gretl*
%{_datadir}/gtksourceview-1.0/language-specs/*.lang
%{_datadir}/pixmaps/*
%{_datadir}/applications/gretl*

%doc ChangeLog CompatLog README.audio README gretl_plugins.txt

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/gretl.pc
%{_libdir}/libgretl*.so
%{_includedir}/%{name}/


%changelog
* Sat Apr 23 2011 Johannes Lips <Johannes.Lips googlemail com> 1.9.5-1
- Update to recent upstream version

* Fri Feb 25 2011 Johannes Lips <Johannes.Lips googlemail com> 1.9.4-1
- Update to recent upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 30 2010 Johannes Lips <Johannes.Lips googlemail com> 1.9.3-1
- update to recent upstream version

* Mon Nov 08 2010 Johannes Lips <Johannes.Lips googlemail com> 1.9.2-1
- update to recent upstream version
- removed the patches because everything was fixed upstream

* Sat Sep 11 2010 Johannes Lips <Johannes.Lips googlemail com> 1.9.1-6
- added the patch from Peter Lemenkov to remove the plugin lad.c

* Sat Sep 11 2010 Johannes Lips <Johannes.Lips googlemail com> 1.9.1-5
- removed the bundled fonts and symlinked system fonts
- added gretl_plugins.txt regarding the license of gretl plugins
- changed the Group of the devel package to Development/Libraries

* Fri Sep 10 2010 Johannes Lips <Johannes.Lips googlemail com> 1.9.1-4
- removed *.la files, bundled fonts and doc directory
- fixed the .desktop file
- removed duplicate COPYING file
- added gtksourceview as a requirement
- added the licenses for Minpack (BSD), mpack (MIT), rq (MIT)

* Thu Sep 09 2010 Johannes Lips <Johannes.Lips googlemail com> 1.9.1-3
- removed the static library
- fixed the sourceforge url
- restructured the %%files section


* Thu Sep 09 2010 Johannes Lips <Johannes.Lips googlemail com> 1.9.1-2
- split into an extra devel package
- changed the license
- added the url to the upstream bugreport
- fixed the %%files section
- usage of the %%find_lang macro to package language files

* Sat Aug 28 2010 Johannes Lips <Johannes.Lips googlemail com> 1.9.1-1
- initial fedora spec 
