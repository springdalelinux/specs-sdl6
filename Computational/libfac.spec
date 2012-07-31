
Summary: An extension to Singular-factory
Name:    libfac
Version: 3.1.3
Release: 1%{?dist}

License: GPLv2 or GPLv3
Url:     http://www.mathematik.uni-kl.de/ftp/pub/Math/Singular/Libfac/
Source0: http://www.mathematik.uni-kl.de/ftp/pub/Math/Singular/Libfac/libfac-3-1-3.tar.gz 
Group:   System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# -debuginfo useless for (only) static libs
%define debug_package   %{nil}

BuildRequires: factory-static
BuildRequires: factory-devel >= %{version}

%description
Singular-libfac is an extension to Singular-factory which implements
factorization of polynomials over finite fields and algorithms for
manipulation of polynomial ideals via the characteristic set methods
(e.g., calculating the characteristic set and the irreducible
characteristic series).

%package devel 
Summary: An extension to Singular-factory
Obsoletes: %{name}-static < %{version}-%{release}
Provides:  %{name}-static = %{version}-%{release}
Group:   Development/Libraries
%description devel 
Singular-libfac is an extension to Singular-factory which implements
factorization of polynomials over finite fields and algorithms for
manipulation of polynomial ideals via the characteristic set methods
(e.g., calculating the characteristic set and the irreducible
characteristic series).


%prep
%setup -q -n %{name}-3-1-3


%build
%configure

# seeing wierd smp (OOM?) errors
make


%install
rm -rf %{buildroot} 

#make install DESTDIR=... fails
%makeinstall

# fix perms
chmod 644 %{buildroot}%{_libdir}/lib*.a


%clean
rm -rf %{buildroot} 


%files devel 
%defattr(-,root,root,-)
%doc 00README ChangeLog COPYING
%{_libdir}/lib*.a
%{_includedir}/*


%changelog
* Tue Mar 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 3.1.1-1
- libfac-3-1-1

* Wed Jan 20 2010 Rex Dieter <rdieter@fedoraproject.rog> - 3.1.0-4
- License: GPLv2 or GPLv3 (#557106)

* Tue Dec  8 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 3.1.0-3
- Explicitly BR factory-static in accordance with the Packaging
  Guidelines (factory-devel is still static-only).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Rex Dieter <rdieter@fedoraproject.org> 3.1.0-1
- libfac-3-1-0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Rex Dieter <rdieter@fedoraproject.org> 3.0.4-2
- drop --with-NOSTREAMIO

* Thu Oct 02 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.4-1
- libfac-3.0.4

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.3-2 
- respin (gcc43)

* Tue Dec 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.0.3-1
- libfac-3.0.3

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.0.2-1
- libfac-3.0.2
- disable -debuginfo (static lib only)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.5-9
- License: GPLv2
- -static -> -devel

* Mon Dec 18 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.5-8
- -devel -> -static

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-7
- respin

* Tue Jul 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-6
- fc6 respin

* Thu Mar 30 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.5-4
- BR: factory-devel >= 2.0.5-7

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.0.5-3
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Oct 1 2004 Rex Dieter <rexdieter at sf.net> 0:2.0.5-1
- 2.0.5

* Mon Nov 17 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.3.b
- update macros
- fix perms on %%_libdir/lib*.a
- try without --with-NOSTREAMIO

* Fri Nov 14 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.2.b
- License: GPL with restrictions
- fixup autoconf usage
- remove cvs tags

* Fri Oct 03 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.1.b
- fix autoconf
- update macros for Fecora Core support.

* Thu Sep 11 2003 Rex Dieter <rexdieter at sf.net> 0:2.0.4-0.fdr.0.b
- first try.
- no shared libs, but make (only) -devel package to signify it's purpose

