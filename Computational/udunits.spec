Name: udunits
Version: 1.12.11
Release: 1%{?dist}
Summary: A library for manipulating units of physical quantities
License: MIT
Group: System Environment/Libraries
URL: http://www.unidata.ucar.edu/software/udunits/
Source0: ftp://ftp.unidata.ucar.edu/pub/udunits/udunits-%{version}.tar.gz
Source1: udunits-wrapper.inc
Patch0: udunits-1.12.11-linuxfixes.patch
Patch1: udunits-1.12.11-64bit.patch
BuildRequires: gcc-gfortran, gcc-c++, groff, byacc
BuildRequires: perl(ExtUtils::MakeMaker)

%description
The Unidata units utility, udunits, supports conversion of unit specifications 
between formatted and binary forms, arithmetic manipulation of unit 
specifications, and conversion of values between compatible scales of 
measurement. A unit is the amount by which a physical quantity is measured. For 
example:

                  Physical Quantity   Possible Unit
                  _________________   _____________
                        time              weeks
                      distance         centimeters
                        power             watts

This utility works interactively and has two modes. In one mode, both an input 
and output unit specification are given, causing the utility to print the 
conversion between them. In the other mode, only an input unit specification is 
given. This causes the utility to print the definition -- in standard units -- 
of the input unit.

%package devel
Group: Development/Libraries
Summary: Headers and libraries for udunits
Requires: %{name} = %{version}-%{release}
Provides: %{name}-static = %{version}-%{release}

%description devel
This package contains the files needed for compiling programs using
the udunits library.

%package -n perl-udunits
Summary: Perl module for udunits
Group: System Environment/Libraries
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: %{name}

%description -n perl-udunits
A perl module for udunits.

%prep
%setup -q
%patch0 -p1 -b .linuxfixes
# Yes, this is a dirty hack.
%ifarch x86_64 ppc64 sparc64 s390x
%patch1 -p1
%endif

%build
export CFLAGS="%{optflags} -fPIC"
export CXXFLAGS="%{optflags} -fPIC"
cd src/
export LD_MATH=-lm 
%configure
make all 

%install
cd src/
make PREFIX=%{_prefix} datadir=%{_sysconfdir} sysconfigdir=%{_sysconfdir} DESTDIR=%{buildroot} install
cp -p COPYRIGHT README RELEASE_NOTES VERSION ../
rm -rf %{buildroot}%{_mandir}/man3f

# Handle multilib
# Rename udunits.inc to udunits-<arch>.inc to avoid file conflicts on multilib systems and install wrapper include file
# udunits-wrapper.inc as udunits.inc
%ifarch %{ix86} x86_64 ia64 sparc sparcv9 sparc64 s390 s390x ppc ppc64
basearch=%{_arch}
# always use i386 for iX86
%ifarch %{ix86}
basearch=i386
%endif
%ifarch sparcv9
basearch=sparc
%endif
%ifarch sparc64
basearch=sparc64
%endif
# Rename files and install wrappers
mv %{buildroot}%{_includedir}/udunits.inc %{buildroot}%{_includedir}/udunits-${basearch}.inc
install -m644 %{SOURCE1} %{buildroot}%{_includedir}/udunits.inc
%endif

find %{buildroot} \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;

%files
%defattr(-,root,root)
%doc COPYRIGHT README RELEASE_NOTES VERSION
%{_bindir}/udunits
%{_mandir}/man1/udunits.1.gz
%config(noreplace) %{_sysconfdir}/udunits.dat

%files devel
%defattr(-,root,root)
%{_includedir}/udunits.h
%{_includedir}/udunits*.inc
%{_libdir}/libudport.a
%{_libdir}/libudunits.a
%{_mandir}/man3/udunits.3.gz
%{_mandir}/man3/udunits.3f.gz

%files -n perl-udunits
%defattr(-,root,root)
%{perl_vendorarch}/UDUNITS.pm
%{perl_vendorarch}/auto/UDUNITS/UDUNITS.bs
%{perl_vendorarch}/auto/UDUNITS/UDUNITS.so
%{perl_vendorarch}/auto/UDUNITS/autosplit.ix
%dir %{perl_vendorarch}/auto/UDUNITS/
%{_mandir}/man1/udunitsperl.1.gz

%changelog
* Thu Jul  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12.11-1
- update to 1.2.11
- add -static Provides to -devel

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.12.9-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.12.9-6
- rebuild against perl 5.10.1

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12.9-5
- fix upstream URL

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.9-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 28 2009 Karsten Hopp <karsten@redhat.com> 1.12.9-3.1
- apply multilib patch on s390x, too

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12.9-2
- missing BR: byacc

* Fri Sep 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12.9-1
- update to 1.12.9

* Mon Mar 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12.4-15
- ia64 doesn't need lib64 hack

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12.4-14
- Rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.12.4-13
- Autorebuild for GCC 4.3

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-12
- multilib enable

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-11.3
- add BR: perl(ExtUtils::MakeMaker)

* Mon Aug 27 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-11.2
- rebuild for BuildID

* Mon Aug  6 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-11.1
- fix license (MIT)

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-11
- bump for FC-6

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-10
- bump for FC-5

* Sat Jul  9 2005 Ed Hill <ed@eh3.com> 1.12.4-9
- use -fPIC for all arches and remove redundant man3f entry

* Mon May  9 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-8
- remove hardcoded dist tags

* Fri May  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-7
- fix BuildRequires for the FC-3 spec (gcc-g77 vs gcc-gfortran)

* Fri Apr 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-6.fc4
- use dist tag

* Sat Apr 16 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-5
- x86_64 needs -fPIC

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-4
- use perl macros

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-3
- Corrected license
- Add BuildRequires: groff
- Add perl MODULE_COMPAT requires for perl-udunits
- Roll in fixes from Ed Hill's package
- Make -devel package

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-2
- minor spec cleanup

* Fri Mar 25 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.12.4-1
- inital package for Fedora Extras
