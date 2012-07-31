Name:			splint
Version:		3.1.2
Release:		6%{?dist}
Summary:		An implementation of the lint program

Group:			Development/Tools
License:		GPLv2+
URL:			http://www.splint.org/
Source0:		http://www.splint.org/downloads/%{name}-%{version}.src.tgz
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	flex 

Obsoletes:		lclint <= 3.0.0
Provides:		lclint = %{version}-%{release}

%description
Splint is a tool for statically checking C programs for coding errors and
security vulnerabilities. With minimal effort, Splint can be used as a
better lint. If additional effort is invested adding annotations to programs,
Splint can perform even stronger checks than can be done by any standard lint.


%prep
%setup -q
chmod 644 doc/manual.pdf
cp -p src/.splintrc splintrc.demo

%build
%configure
# Parallel builds seem to fail
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README doc/manual.pdf splintrc.demo
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_datadir}/%{name}/


%changelog
* Sat Aug 22 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 3.1.2-6
- Specfile sanity revisited: proper Provides/Obsoletes on lclint
  and some other minor changes to make rpmlint silent

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 3.1.2-5
- Convert specfile to UTF-8.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1.2-2
- fix license tag

* Sat Jul 12 2008 Panu Matilainen <pmatilai@redhat.com> - 3.1.2-1
- update to 3.1.2

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.1.1-16
- Autorebuild for GCC 4.3

* Mon Sep 11 2006 Paul Nasrat <pnasrat@redhat.com> - 3.1.1-15
- Rebuild for FC6

* Wed May 31 2006 Paul Nasrat <pnasrat@redhat.com> - 3.1.1-14
- Add flex br

* Thu Apr 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.1.1-13
- Manual.pdf - file permissions corrected.
- Included a demo .splintrc file as doc (splintrc.demo == src/.splintrc).

* Mon Feb 13 2006 Paul Nasrat <pnasrat@redhat.com> - 3.1.1-12
- FC5 rebuild for new gcc

* Sun Jan 15 2006 Paul Nasrat <pnasrat@redhat.com> - 3.1.1-11
- Rebuild for FC5

* Thu Jul 28 2005 Paul Nasrat <pnasrat@redhat.com> - 3.1.1-10
- Turn off parallel builds

* Wed Jun 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.1.1-9
- Dist tag added.
- Specfile reformatted (compliance with the Fedora Extras template).

* Fri Jun 17 2005 Paul Nasrat <pnasrat@redhat.com> - 3.1.1-8
- Fedora Extras build

* Sat Mar 19 2005 Miloslav Trmac <mitr@redhat.com> - 3.1.1-7
- Bump revision for rebuild

* Sat Mar 19 2005 Miloslav Trmac <mitr@redhat.com> - 3.1.1-6
- Ship the manual in PDF instead of HTML with missing images (#62434)

* Fri Mar  4 2005 Jeff Johnson <jbj@redhat.com> 3.1.1-5
- rebuild with gcc4.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May  1 2003 Jeff Johnson <jbj@redhat.com> 3.1.1-1
- update to 3.1.1.

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 3.0.1.7-0.20030123
- rebuild

* Mon Nov 11 2002 Jeff Johnson <jbj@redhat.com> 3.0.1.6-4
- rebuild from cvs.
- update to 3.0.1.7 snapshot.
- avoid non-i386 horkage for now.

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Feb 26 2002 Nalin Dahyabhai <nalin@redhat.com> 3.0.1.6-2
- rebuild in new environment

* Tue Feb 12 2002 Jeff Johnson <jbj@redhat.com>
- update to splint-3.0.1.6.

* Sat Feb  9 2002 Jeff Johnson <jbj@redhat.com>
- update to splint-3.0.1.5.

* Thu Jan 17 2002 Jeff Johnson <jbj@redhat.com>
- update to splint-3.0.1.3.1.

* Mon Oct  8 2001 Jeff Johnson <jbj@redhat.com>
- update to 3.0.0.17.

* Thu Sep  6 2001 Jeff Johnson <jbj@redhat.com>
- update to 2.5r.

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Thu Feb 15 2001 Trond Eivind Glomsrød <teg@redhat.com>
- <time.h> fix

* Mon Dec 11 2000 Bill Nottingham <notting@redhat.com>
- fix build on ia64

* Mon Aug 21 2000 Jeff Johnson <jbj@redhat.com>
- set default configuration appropriately.

* Fri Jul 28 2000 Eric Veldhuyzen <eric@terra.nu>
- upgraded to 2.5q

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 17 2000 Tim Powers <timp@redhat.com>
- added defattr

* Wed Jul 12 2000 Tim Powers <timp@redhat.com>
- fixed build section so that it links with flex properly

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jun 7 2000 Tim Powers <timp@redhat.com>
- minor spec file cleanups, built for Powertools-7.0

* Fri May 26 2000 Eric Veldhuyzen <eric@terra.nu>
- upgraded to 2.5m
- reorganized specfile

* Sat Oct 31 1998 Justin Cormack <jpc1@doc.ic.ac.uk>

- found correct 2.4b source (was actually 2.3)
- no longer an emacs mode
- added documentation

* Wed Oct 14 1998 Justin Cormack <jpc1@doc.ic.ac.uk>
- fixed library directories not to point at buildroot

* Mon Oct 12 1998 Justin Cormack <jpc1@doc.ic.ac.uk>
- fixed executable

* Mon Jun 06 1998 Michael Maher <mike@redhat.com>
- fixed paths for executable link

* Mon May 17 1998 Michael Maher <mike@redhat.com>
- updated to newest version
- added buildroot
- added wmconfig

* Mon Feb 16 1998 Otto Hammersmith <otto@redhat.com>
- added Summary

* Tue Feb  3 1998 Otto Hammersmith <otto@redhat.com>
- %%doc'ed some stuff

* Mon Feb  2 1998 Otto Hammersmith <otto@redhat.com>
- made /usr/lib/lclint/bin a directory, not the executable

* Fri Jan 23 1998 Otto Hammersmith <otto@redhat.com>
- built the package
