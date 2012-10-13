# Updated to cabal2spec-0.22.2 and ghc-rpm-macros-0.8.1

%global pkg_name darcs

%global common_summary Haskell %{pkg_name} library

%global common_description Darcs is a revision control system, along the lines of CVS\
or arch. That means that it keeps track of various revisions\
and branches of your project, allows for changes to\
propagate from one branch to another. Darcs is intended to\
be an ``advanced'' revision control system. Darcs has two\
particularly distinctive features which differ from other\
revision control systems: 1) each copy of the source is a\
fully functional branch, and 2) underlying darcs is a\
consistent and powerful theory of patches.

# Haskell library dependencies:
%global ghc_pkg_deps ghc-hashed-storage-devel, ghc-haskeline-devel, ghc-html-devel, ghc-parsec-devel, ghc-regex-compat-devel, ghc-zlib-devel

%global ghc_pkg_c_deps curl-devel

%bcond_without shared
%bcond_without hscolour

# debuginfo is not useful for ghc
%global debug_package %{nil}

Name:           %{pkg_name}
Version:        2.4.4
Release:        3%{?dist}
Summary:        David's advanced revision control system

Group:          Development/Tools
License:        GPLv2+
URL:            http://www.darcs.net/
Source0:        http://hackage.haskell.org/packages/archive/%{name}/%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# fedora ghc archs:
ExclusiveArch:	%{ix86} x86_64 ppc alpha
Obsoletes:      darcs-server < 2.2.1-6
BuildRequires:  ghc, ghc-doc, ghc-prof
BuildRequires:  ghc-rpm-macros >= 0.8.1
%if %{with hscolour}
BuildRequires:  hscolour
%endif
%{?ghc_pkg_deps:BuildRequires:  %{ghc_pkg_deps}, %(echo %{ghc_pkg_deps} | sed -e "s/\(ghc-[^, ]\+\)-devel/\1-doc,\1-prof/g")}
%{?ghc_pkg_c_deps:BuildRequires:  %{ghc_pkg_c_deps}}
# for make check
BuildRequires:  which

%description
%{common_description}


%prep
%setup -q


%build
%ghc_lib_build


%check
%cabal test


%install
rm -rf $RPM_BUILD_ROOT
%ghc_lib_install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
cp -p contrib/darcs_completion $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/darcs


%clean
rm -rf $RPM_BUILD_ROOT


%ghc_binlib_package -o 2.4.4-4


%files
%defattr(-,root,root,-)
%doc COPYING NEWS contrib/_darcs.zsh
%dir %{_sysconfdir}/bash_completion.d
%config(noreplace) %{_sysconfdir}/bash_completion.d/darcs
%{_bindir}/darcs
# workaround Cabal-1.8 bug (http://hackage.haskell.org/trac/hackage/ticket/641)
%attr(644,root,root) %{_mandir}/man1/darcs.1*


%changelog
* Mon Jul 19 2010 Jens Petersen <petersen@redhat.com> - 2.4.4-3
- rebuild for newer regex-compat from haskell-platform-2010.2.0.0
- update to cabal2spec-0.22.1:
  - bcond for hscolour
  - add doc obsoletes version

* Sun Jun 27 2010 Jens Petersen <petersen@redhat.com> - 2.4.4-2
- sync cabal2spec-0.22.1

* Thu Jun  3 2010 Jens Petersen <petersen@redhat.com> - 2.4.4-1
- update to 2.4.4

* Tue May 18 2010 Jens Petersen <petersen@redhat.com> - 2.4.3-1
- update to 2.4.3

* Thu Apr 29 2010 Jens Petersen <petersen@redhat.com> - 2.4.1-2
- rebuild against ghc-6.12.2

* Wed Apr 14 2010 Jens Petersen <petersen@redhat.com> - 2.4.1-1
- update to 2.4.1 bugfix release
- darcs-2.4-issue458.sh-attr.patch was upstreamed

* Fri Mar  5 2010 Jens Petersen <petersen@redhat.com> - 2.4-3
- make manpage attr 0644 to workaround Cabal bug (#570110)

* Fri Mar  5 2010 Jens Petersen <petersen@redhat.com> - 2.4-2
- obsolete darcs-server

* Mon Mar  1 2010 Jens Petersen <petersen@redhat.com> - 2.4-1
- new major upstream version 2.4
- darcs is now officially a cabal binlib package
- package with ghc-rpm-macros
- no longer BR autoconf, sendmail, ncurses-devel, zlib-devel
- add haskell deps: hashed-storage, haskeline, html, parsec, regex-compat, zlib
- server (subpackage) is gone
- add darcs-2.4-issue458.sh-attr.patch to workaround selinux output
- run check tests again
- replace AUTHORS with NEWS
- zsh completion filename changed

* Sun Sep 13 2009 Jens Petersen <petersen@redhat.com> - 2.2.1-5
- rebuild against ghc-6.10.4 which should fix --help hangs
- improve doc summary (#522899)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  2 2009 Jens Petersen <petersen@redhat.com> - 2.2.1-3
- drop post script since semanage now superfluous
- drop the unused alphatag for now
- simplify BRs

* Sat Apr 25 2009 Jens Petersen <petersen@redhat.com> - 2.2.1-2
- rebuild against ghc-6.10.3

* Tue Feb 24 2009 Jens Petersen <petersen@redhat.com> - 2.2.1-1
- update to 2.2.1
- own bash_completion.d (#487012)
- use ix86
- ChangeLog no longer included

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Jens Petersen <petersen@redhat.com> - 2.2.0-1
- update to 2.2.0
- update install targets

* Wed Dec 10 2008 Jens Petersen <petersen@redhat.com> - 2.1.2-1
- update to 2.1.2

* Tue Nov 11 2008 Jens Petersen <petersen@redhat.com> - 2.1.1-0.1.rc2
- update to 2.1.1rc2 which builds with ghc-6.10.1
- try to run all tests again

* Mon Sep 22 2008 Jens Petersen <petersen@redhat.com> - 2.0.2-3
- revert last change and require policycoreutils for post (mtasaka, #462221)

* Fri Sep 19 2008 Jens Petersen <petersen@redhat.com> - 2.0.2-2
- use full paths to selinux tools in %%post (Jon Stanley, #462221)

* Sat Jun 28 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 2.0.2-1
- split out the manual to a -doc rpm
- update to 2.0.2
- switch to make test
- remove skipping of tests - it doesn't appear to apply anymore

* Mon Jun 23 2008 Jens Petersen <petersen@redhat.com> - 2.0.0-1.fc10
- update to 2.0.0
- no longer require darcs-ghc-6_8-compat.patch and darcs-error_xml-missing.patch
- move utf-8 conversion to prep
- disable check for now
- manual is now doc and shell completion config lives in tools
- install bash completion

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.9-11
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.0.9-10
- add darcs and libxslt to darcs-server dependencies (#427489)
- add patch to fix missing install errors.xml (#427490)

* Fri Nov 30 2007 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.0.9-9
- add BuildRequires autoconf and use of autoconf in %%build to utilize
  the ghc 6.8 compatibility patches

* Thu Nov 29 2007 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.0.9-8
- add patches from darcs unstable branch to deal with ghc 6.8
  compatibility for rawhide

* Sun Nov 25 2007 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.0.9-7
- added alpha to ExcludeArch (#396501)
- cleanup rpmlint warnings
  - convert ISO-8859 text files to UTF-8
  - added %%doc files to -server subpackage
  - fixed quoting of %%macros in changelog comments

* Fri Sep 21 2007 Jens Petersen <petersen@redhat.com> - 1.0.9-6
- fix the "|| :" quoting in the post install script (#295351)

* Thu Sep 20 2007 Jens Petersen <petersen@redhat.com> - 1.0.9-5
- set selinux file-context for %%{_bindir}/darcs
  (reported by Jim Radford, #295351)

* Fri Aug 10 2007 Jens Petersen <petersen@redhat.com> - 1.0.9-4
- specify license is GPL 2 or later

* Wed Jun 27 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.0.9-3
- clean rpmlint warnings/errors 
  - move PreReq to Requires(post)
  - move make check to 'check' section
  - mark config files as such

* Wed Jun 27 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.0.9-2
- added ExcludeArch: ppc64

* Wed Jun 27 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.0.9-1
- update to 1.0.9

* Mon Feb 19 2007 Jens Petersen <petersen@redhat.com> - 1.0.9-0.1.rc2
- update to 1.0.9rc2 which builds with ghc66

* Fri Feb  2 2007 Jens Petersen <petersen@redhat.com> - 1.0.8-5
- rebuild for ncurses replacing termcap (#226754)

* Wed Nov  1 2006 Jens Petersen <petersen@redhat.com> - 1.0.8-4
- rebuild for new libcurl

* Thu Sep 28 2006 Jens Petersen <petersen@redhat.com> - 1.0.8-3
- rebuild for FC6
- enable make check

* Fri Jun 23 2006 Jens Petersen <petersen@redhat.com> - 1.0.8-2
- set unconfined_execmem_exec_t context to allow running under selinux targeted
  policy (#195820)

* Wed Jun 21 2006 Jens Petersen <petersen@redhat.com> - 1.0.8-1
- update to 1.0.8

* Sun May 14 2006 Jens Petersen <petersen@redhat.com> - 1.0.7-1
- update to 1.0.7
- fix typo of propagate in description (#189651)
- disable "make check" for now since it blows up in buildsystem

* Thu Mar  2 2006 Jens Petersen <petersen@redhat.com> - 1.0.6-1
- update to 1.0.6
  - darcs-createrepo is gone

* Thu Dec  8 2005 Jens Petersen <petersen@redhat.com> - 1.0.5-1
- 1.0.5 bugfix release

* Mon Nov 14 2005 Jens Petersen <petersen@redhat.com> - 1.0.4-1
- 1.0.4 release
  - skip tests/send.sh for now since it is failing in buildsystem

* Tue Jul  5 2005 Jens Petersen <petersen@redhat.com>
- drop superfluous doc buildrequires (Karanbir Singh, #162436)

* Fri Jul  1 2005 Jens Petersen <petersen@redhat.com> - 1.0.3-2
- fix buildrequires
  - add sendmail, curl-devel, ncurses-devel, zlib-devel, and
    tetex-latex, tetex-dvips, latex2html for doc generation

* Tue May 31 2005 Jens Petersen <petersen@redhat.com> - 1.0.3-1
- initial import into Fedora Extras
- 1.0.3 release
- include bash completion file in doc dir

* Sun May  8 2005 Jens Petersen <petersen@haskell.org> - 1.0.3-0.rc1.1
- 1.0.3rc1
  - build with ghc-6.4

* Wed Feb  8 2005 Jens Petersen <petersen@haskell.org> - 1.0.2-1
- update to 1.0.2

* Thu Jul 15 2004 Jens Petersen <petersen@haskell.org> - 0.9.22-1
- 0.9.22
- darcs-0.9.21-css-symlinks.patch no longer needed

* Thu Jun 24 2004 Jens Petersen <petersen@haskell.org> - 0.9.21-1
- update to 0.9.21
- replace darcs-0.9.13-mk-include.patch with darcs-0.9.21-css-symlinks.patch

* Wed Nov  5 2003 Jens Petersen <petersen@haskell.org>
- Initial packaging.
