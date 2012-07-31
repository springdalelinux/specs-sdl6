Name:           perl-Curses
Version:        1.28
Release:        1%{?dist}
Summary:        Perl bindings for ncurses

Group:          Development/Libraries
License:        GPL+
URL:            http://search.cpan.org/dist/Curses/
Source0:        http://search.cpan.org/CPAN/authors/id/G/GI/GIRAFFED/Curses-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ncurses-devel perl-devel perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Perl bindings for ncurses, bringing terminal-independent character
handling capabilities to Perl.


%prep
%setup -q -n Curses-%{version}
test -f hints/c-linux.ncursesw.h || cp hints/c-linux.ncurses.h hints/c-linux.ncursesw.h
sed -i -e 's|/usr/local/bin/perl|%{__perl}|' demo*
sed -i -e 's|/usr//bin/perl|%{__perl}|' demo*

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" \
   PANELS MENUS FORMS
make %{?_smp_mflags}

# A note about the following alarming output...
#
#  WARNING: Your Curses form.h file appears to be in the default
#  system search path, which will not work for us because of
#  the conflicting Perl form.h file.  This means your 'make' will
#  probably fail unless you fix this, as described in the INSTALL
#  file.
#
#... can be ignored because /usr/include/form.h is a symlink to
#/usr/include/ncurses/form.h, which the Makefile.PL finds and
#uses quite happily.


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

#Remove exec perm for file aimed to be bundled as %%doc
chmod -x demo*

%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Copying Artistic README demo*
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Curses.pm
%{_mandir}/man3/*.3*


%changelog
* Tue May 11 2010 Steve Traylen <steve.traylen@cern.ch> - 1.28-1
- Update to 1.28.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 kwizart < kwizart at gmail.com > - 1.27-1
- Update to 1.27
- Remove exec perm for demo* provided as %%doc - Fix #510186

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.20-3
- rebuild for new perl

* Thu Feb 14 2008 Garrick Staples <garrick@usc.edu> 1.20-2
- forgot to update tarball, building

* Thu Feb 14 2008 Garrick Staples <garrick@usc.edu> 1.20-1
- bump to 1.20

* Fri Aug 17 2007 Garrick Staples <garrick@usc.edu> 1.16-4
- fix /usr//bin/perl, bz#253336

* Thu Aug 16 2007 Garrick Staples <garrick@usc.edu> 1.16-3
- need BR: perl(Test::More)

* Thu Aug 16 2007 Garrick Staples <garrick@usc.edu> 1.16-2
- rebuild

* Thu Aug 16 2007 Garrick Staples <garrick@usc.edu> 1.16-1
- bump to 1.16
- correct License: tag
- need BR: perl-devel

* Sun Aug 27 2006 Garrick Staples <garrick@usc.edu> 1.15-1
- bump to 1.15

* Sun Aug 27 2006 Garrick Staples <garrick@usc.edu> 1.14-2
- rebuild

* Sun Aug 27 2006 Garrick Staples <garrick@usc.edu> 1.14-1
- bump to 1.14
- FC6 mass rebuild

* Fri Apr 21 2006 Garrick Staples <garrick@usc.edu> 1.13-3
- add a note about the falsely alarming warning
- don't remove execute bit from demos

* Thu Apr 20 2006 Garrick Staples <garrick@usc.edu> 1.13-2
- spec cleanups
- add doc files

* Wed Apr 19 2006 Garrick Staples <garrick@usc.edu> 1.13-1
- Initial spec file
