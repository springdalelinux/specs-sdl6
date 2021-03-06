Name:           perl-Sys-Mmap
Version:        0.16
Release:        7%{?dist}
Summary:        Use mmap to map in a file as a Perl variable
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Sys-Mmap/
Source0:        http://www.cpan.org/authors/id/T/TO/TODDR/Sys-Mmap-%{version}.tar.gz
BuildRequires:  perl(ExtUtils::MakeMaker) perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%{?perl_default_filter}

%description
The Mmap module lets you use mmap to map in a file as a perl variable rather
than reading the file into dynamically allocated memory.  Multiple programs may
map the same file into memory, and immediately see changes by each other.
Memory may be allocated not attached to a file, and shared with subprocesses.

%prep
%setup -q -n Sys-Mmap-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make test

%files
%defattr(-,root,root,-)
%doc Artistic Changes Copying README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Sys*
%{_mandir}/man3/*

%changelog
* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.14-7
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.14-6
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.14-5
- Perl mass rebuild

* Tue Jun 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.14-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.14-2
- Switch over to %%buildroot and %%optflags.  Who needs verbose screaming?

* Mon Jan 24 2011 Jason Tibbitts <tibbs@math.uh.edu> 0.14-1
- Specfile autogenerated by cpanspec 1.78.
- Initial tweaks before package submission.
