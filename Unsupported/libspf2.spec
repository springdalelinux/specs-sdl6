# NOTE THAT THE TEST SUITE IS CURRENTLY BROKEN
# USE rpmbuild --with checks TO SEE THIS FOR YOURSELF

# Each change to the spec requires a bump to version/release of both library and perlmod
%define library_version 1.2.9
%define library_release 1%{?dist}
%define perlmod_version 0.01
%define perlmod_release 2%{?dist}

# graphviz needed to build API docs, only available from Fedora 3, RHEL 4
%if 0%{?fedora} >= 3 || 0%{?rhel} >= 4
%define build_apidocs 1
%else
%define build_apidocs 0
%endif

# Use rpmbuild --with checks to try running the broken test suite (disabled by default)
%{!?_without_checks:	%{!?_with_checks: %define _without_checks --without-checks}}
%{?_with_checks:	%define enable_checks 1}
%{?_without_checks:	%define enable_checks 0}

# Macros that need defining for older distributions
%{!?perl_vendorarch: %define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)}
%{!?__id_u: %define __id_u %([ -x /bin/id ]&&echo /bin/id||([ -x /usr/bin/id ]&&echo /usr/bin/id||echo /bin/true)) -u}

Name:		libspf2
Version:	%{library_version}
Release:	%{library_release}
Summary:	An implementation of the SPF specification
License:	BSD and LGPLv2+
Group:		System Environment/Libraries
Url:		http://www.libspf2.org/
Source0:	http://www.libspf2.org/spf/libspf2-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if %{build_apidocs}
# For API docs
BuildRequires:	doxygen, graphviz
%endif
# For perl bindings (Makefile.PL claims Mail::SPF is needed, but it isn't)
BuildRequires:	perl(ExtUtils::MakeMaker)
# For perl test suite
BuildRequires:	perl(Test::Pod), perl(String::Escape)
# POD Coverage is non-existent, causes test suite to fail
BuildConflicts:	perl(Test::Pod::Coverage)
# Perl module fails the standard test suite
BuildConflicts:	perl(Mail::SPF::Test)

%description
libspf2 is an implementation of the SPF (Sender Policy Framework)
specification as found at:
http://www.ietf.org/internet-drafts/draft-mengwong-spf-00.txt
SPF allows email systems to check SPF DNS records and make sure that
an email is authorized by the administrator of the domain name that
it is coming from. This prevents email forgery, commonly used by
spammers, scammers, and email viruses/worms.

A lot of effort has been put into making it secure by design, and a
great deal of effort has been put into the regression tests.

%package devel
Summary:	Development tools needed to build programs that use libspf2
Group:		Development/Libraries
Version:	%{library_version}
Release:	%{library_release}
Requires:	%{name} = %{version}-%{release}

%description devel
The libspf2-devel package contains the header files and static
libraries necessary for developing programs using the libspf2 (Sender
Policy Framework) library.

If you want to develop programs that will look up and process SPF records,
you should install libspf2-devel.

%if %{build_apidocs}
API documentation is in the separate libspf2-apidocs package.

%package apidocs
Summary:	API documentation for the libspf2 library
Group:		Documentation
Version:	%{library_version}
Release:	%{library_release}
Requires:	libspf2-devel = %{version}-%{release}

%description apidocs
The libspf2-apidocs package contains the API documentation for creating
applications that use the libspf2 (Sender Policy Framework) library.
%endif

%package -n perl-Mail-SPF_XS
Summary:	An XS implementation of Mail::SPF
Group:		Development/Libraries
License:	GPL+ or Artistic
Version:	%{perlmod_version}
Release:	%{perlmod_release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-Mail-SPF_XS
This is an interface to the C library libspf2 for the purpose of
testing. While it can be used as an SPF implementation, you can also
use Mail::SPF, which is a little more perlish.

%package progs
Summary:	Programs for making SPF queries using libspf2
Group:		Applications/Internet
Version:	%{library_version}
Release:	%{library_release}
Requires:	%{name} = %{version}-%{release}

Requires(post): /usr/sbin/alternatives
Requires(preun): /usr/sbin/alternatives
Requires(postun): /usr/sbin/alternatives, /usr/bin/readlink

%description progs
Programs for making SPF queries and checking their results using libspf2.

%prep
%setup -q -n libspf2-%{version}

%build
# The configure script checks for the existence of __ns_get16 and uses the
# system-supplied version if found, otherwise one from src/libreplace.
# However, this function is marked GLIBC_PRIVATE in recent versions of glibc
# and shouldn't be called even if the configure script finds it. So we make
# sure that the configure script always uses the version in src/libreplace.
# This prevents us getting an unresolvable dependency in the built RPM.
ac_cv_func___ns_get16=no
export ac_cv_func___ns_get16

%configure --enable-perl --disable-dependency-tracking

# Kill bogus RPATHs
%{__sed} -i 's|^sys_lib_dlsearch_path_spec="/lib /usr/lib|sys_lib_dlsearch_path_spec="/%{_lib} %{_libdir}|' libtool

%{__make} %{?_smp_mflags}

%if %{build_apidocs}
# Generate API docs
%{__sed} -i -e 's/\(SHORT_NAMES[[:space:]]*=[[:space:]]*\)NO/\1YES/' Doxyfile
/usr/bin/doxygen
%endif

%install
%{__rm} -rf %{buildroot}
%{__make} \
	DESTDIR=%{buildroot} \
	PERL_INSTALL_ROOT=$(%{__grep} DESTDIR perl/Makefile &> /dev/null && echo "" || echo %{buildroot}) \
	INSTALLDIRS=vendor \
	INSTALL="%{__install} -p" \
	install

# Clean up after impure perl installation
/usr/bin/find %{buildroot} \( -name perllocal.pod -o -name .packlist \) -exec %{__rm} {} ';'
/usr/bin/find %{buildroot} -type f -name '*.bs' -a -size 0 -exec %{__rm} -f {} ';'
/usr/bin/find %{buildroot} -depth -type d -exec /bin/rmdir {} 2>/dev/null ';'
%{__chmod} -R u+w %{buildroot}/*

# Don't want statically-linked binaries
%{__rm} -f %{buildroot}%{_bindir}/spf*_static

# Rename binaries that will be accessed via alternatives
%{__mv} -f %{buildroot}%{_bindir}/spfquery	%{buildroot}%{_bindir}/spfquery.libspf2
%{__mv} -f %{buildroot}%{_bindir}/spfd		%{buildroot}%{_bindir}/spfd.libspf2

%check
%if %{enable_checks}
%{__make} -C tests check
%endif
LD_PRELOAD=$(pwd)/src/libspf2/.libs/libspf2.so %{__make} -C perl test

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post progs
/usr/sbin/alternatives --install %{_bindir}/spfquery spf %{_bindir}/spfquery.libspf2 20 \
	--slave %{_bindir}/spfd spf-daemon %{_bindir}/spfd.libspf2
exit 0

%preun progs
if [ $1 = 0 ]; then
	/usr/sbin/alternatives --remove spf %{_bindir}/spfquery.libspf2
fi
exit 0

%postun progs
if [ "$1" -ge "1" ]; then
	spf=`readlink /etc/alternatives/spf`
	if [ "$spf" == "%{_bindir}/spfquery.libspf2" ]; then
		/usr/sbin/alternatives --set spf %{_bindir}/spfquery.libspf2
	fi
fi
exit 0

%triggerpostun -- libspf2-progs <= 1.0.4-3
/usr/sbin/alternatives --auto spf

%files
%defattr(-,root,root,-)
%{_libdir}/libspf2.so.*
%doc README INSTALL LICENSES TODO
#%doc docs/*.txt

%files devel
%defattr(-,root,root,-)
%{_includedir}/spf2/spf*.h
%{_libdir}/libspf2.so
%exclude %{_libdir}/libspf2.a
%exclude %{_libdir}/libspf2.la

%if %{build_apidocs}
%files apidocs
%defattr(-,root,root,-)
%doc doxygen/html
%endif

%files progs
%defattr(-,root,root,-)
%{_bindir}/spfd.libspf2
%{_bindir}/spfquery.libspf2
%{_bindir}/spftest
%{_bindir}/spf_example

%files -n perl-Mail-SPF_XS
%defattr(-,root,root,-)
%{perl_vendorarch}/Mail/
%{perl_vendorarch}/auto/Mail/
%{_mandir}/man3/Mail::SPF_XS.3pm*

%changelog
* Mon Nov 10 2008 Paul Howarth <paul@city-fan.org> 1.2.9-1
- New upstream version 1.2.9
- Perl module has changed but its version number hasn't
- docs directory no longer included in release tarball

* Wed Oct 15 2008 Paul Howarth <paul@city-fan.org> 1.2.8-1
- New upstream version 1.2.8, includes fix for CVE-2008-2469
  (buffer overflows handling DNS responses)
- Drop all patches, all included upstream (or equivalent fixes)
- Fix bogus RPATHs on x86_64
- Enable perl bindings (in perl-Mail-SPF_XS subpackage)
- No upstream Changelog anymore
- Add buildreqs doxygen and graphviz for building API docs, which are large
  and now in an -apidocs subpackage (Fedora 3, RHEL 4 onwards)
- Add buildreq perl(ExtUtils::MakeMaker) for perl bindings
- Add buildreqs perl(Test::Pod) and perl(String::Escape) for perl module test
  suite
- BuildConflict with perl(Mail::SPF::Test) and perl(Test::Pod::Coverage) as
  the associated tests are beyond simple repair

* Thu Jul 31 2008 Paul Howarth <paul@city-fan.org> 1.2.5-4
- Incorporate patches for res_ninit() setup and malloc() usage from
  Johann Klasek <johann AT klasek DOT at>
  (see http://milter-greylist.wikidot.com/libspf2)
- Clarify license as BSD OR LGPL (v2.1 or later)
- Add dist tag so that we can build distro-specific RPM packages instead of a
  single generic package; the benefit of this is that recent distributions can
  take advantages of improvements in their compilers
- Use regular %%configure macro to pick up distro-specific compiler flags
- Don't package static library (--disable-static configure option is broken)
- Dispense with pointless provide of `spf'

* Mon Feb 12 2007 Paul Howarth <paul@city-fan.org> 1.2.5-3
- Cosmetic spec file cleanup
- Use patch instead of scripted edit to remove bogus include file reference
- Patch to make 64-bit clean
  (http://permalink.gmane.org/gmane.mail.spam.spf.devel/1212)
- Remove buildroot unconditionally in %%clean and %%install
- Don't include libtool archive in -devel package
- Disable running of test suite by default

* Wed Aug  3 2005 Paul Howarth <paul@city-fan.org> 1.2.5-2
- Workaround for %%check with rpm-build <= 4.1.1
- Remove reference to not-installed spf_dns_internal.h in spf_server.h
- Minimize rpmlint issues

* Thu Feb 24 2005 Paul Howarth <paul@city-fan.org> 1.2.5-1
- Update to 1.2.5
- Patches removed; now included upstream

* Sun Feb 20 2005 Paul Howarth <paul@city-fan.org> 1.2.1-1
- Update to 1.2.1
- Remove case-sensitivity patch
- spf_example_2mx no longer included

* Sun Feb 20 2005 Paul Howarth <paul@city-fan.org> 1.0.4-9
- Enhance detection of Mandrake build system
- Add support for building compat-libspf2 package
- alternatives is a prerequisite for the -progs subpackage only

* Thu Oct 28 2004 Paul Howarth <paul@city-fan.org> 1.0.4-8
- Downgrade alternatives priority to 20 so that other implementations
  of spfquery will be preferred; there is still a case-sensitivity bug
  in libspf2 and no sign of an imminent fix

* Mon Aug 16 2004 Paul Howarth <paul@city-fan.org> 1.0.4-7
- Configure fix to find -lresolv on x64_64
- Portability fixes for x64_64

* Sun Aug  1 2004 Paul Howarth <paul@city-fan.org> 1.0.4-6
- Fix case-sensitivity bug.

* Wed Jul 28 2004 Paul Howarth <paul@city-fan.org> 1.0.4-5
- Revert -pthread option as it didn't improve anything.

* Tue Jul 27 2004 Paul Howarth <paul@city-fan.org> 1.0.4-4
- Use `alternatives' so that the spfquery and spfd programs can co-exist
  with versions from other implementations.
- Ensure thread-safe operation by building with -pthread.

* Thu Jul 15 2004 Paul Howarth <paul@city-fan.org> 1.0.4-3
- Install the libtool library in the devel package so that
  dependent libraries are found properly.
- Use the libtool supplied with the package rather than the
  system libtool.

* Tue Jul 13 2004 Paul Howarth <paul@city-fan.org> 1.0.4-2
- Cosmetic changes for building on Mandrake Linux
- Require rpm-build >= 4.1.1 for building to avoid strange error messages
  from old versions of rpm when they see %%check
- Require glibc-devel and make for building
- Require perl for building with checks enabled
- Improved description text for the packages

* Fri Jul 09 2004 Paul Howarth <paul@city-fan.org> 1.0.4-1
- Update to 1.0.4
- Added facility to build without running test suite
  (rpmbuild --without checks)

* Sat Jul 03 2004 Paul Howarth <paul@city-fan.org> 1.0.3-1
- Initial RPM build.
