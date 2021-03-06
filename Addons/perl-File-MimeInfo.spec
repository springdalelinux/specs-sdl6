Name:           perl-File-MimeInfo
Version:        0.15
Release:        7%{?dist}
Summary:        Determine file type and open application
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/File-MimeInfo/
Source0:        http://www.cpan.org/authors/id/P/PA/PARDUS/File-MimeInfo/File-MimeInfo-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Module::Build) perl(Test::More) perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(File::BaseDir) perl(File::DesktopEntry)
# needed for some tests otherwise there are warnings
BuildRequires:  shared-mime-info 
# there is also a mimeinfo.cache file created by desktop-file-utils
# needed. It won't be there if building in a chroot, even if 
# desktop-file-utils is installed if desktop-file-utils was never run.
Requires:       shared-mime-info
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module can be used to determine the mime type of a file. It tries to
implement the freedesktop specification for a shared MIME database.

%prep
%setup -q -n File-MimeInfo-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{_bindir}/mimeopen
%{_bindir}/mimetype
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.15-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.15-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.15-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.15-2
- rebuild for new perl

* Thu Feb 14 2008 Patrice Dumas <pertusus@free.fr> 0.15-1
- update to 0.15, remove upstreamed no-ask patch

* Wed Aug  8 2007 Patrice Dumas <pertusus@free.fr> 0.14-1
- update to 0.14

* Thu Nov 16 2006 Patrice Dumas <pertusus@free.fr> 0.13-3
- add a Requires on shared-mime-info (Bug #215972)

* Wed Oct 11 2006 Patrice Dumas <pertusus@free.fr> 0.13-2
- add an option to launch mimeopen non interactively

* Wed Oct 11 2006 Patrice Dumas <pertusus@free.fr> 0.13-1
- Specfile autogenerated by cpanspec 1.69.
