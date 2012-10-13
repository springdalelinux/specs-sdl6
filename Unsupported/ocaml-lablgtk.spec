%define debug_package %{nil}

Name:           ocaml-lablgtk
Version:        2.14.0
Release:        3%{?dist}

Summary:        Objective Caml interface to gtk+

Group:          System Environment/Libraries
License:        LGPLv2 with exceptions

URL:            http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgtk.html
Source:         http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/dist/lablgtk-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch:    sparc64 s390 s390x

Obsoletes:      lablgtk <= 2.6.0-7
Provides:       lablgtk = 2.6.0-7

BuildRequires:  ncurses-devel
BuildRequires:  gnome-panel-devel
BuildRequires:  gtk2-devel
BuildRequires:  gtkglarea2-devel
BuildRequires:  gtkspell-devel
BuildRequires:  libXmu-devel
BuildRequires:  libglade2-devel
BuildRequires:  libgnomecanvas-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  librsvg2-devel
BuildRequires:  ocaml >= 3.10.1
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-lablgl-devel >= 1.03
BuildRequires:  ocaml-ocamldoc
BuildRequires:  zlib-devel
BuildRequires:  gtksourceview-devel


%define _use_internal_dependency_generator 0
%define __find_requires /usr/lib/rpm/ocaml-find-requires.sh -i GtkSourceView_types -i GtkSourceView2_types
%define __find_provides /usr/lib/rpm/ocaml-find-provides.sh


%description
LablGTK is is an Objective Caml interface to gtk+.

It uses the rich type system of Objective Caml 3 to provide a strongly
typed, yet very comfortable, object-oriented interface to gtk+. This
is not that easy if you know the dynamic typing approach taken by
gtk+.


%package doc
Group:          System Environment/Libraries
Summary:        Documentation for LablGTK
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n lablgtk-%{version}

# version information in META file is wrong
perl -pi -e 's|version="1.3.1"|version="%{version}"|' META


%build
%configure --with-gl --enable-debug
perl -pi -e "s|-O|$RPM_OPT_FLAGS|" src/Makefile
make world
make doc CAMLP4O="camlp4o -I %{_libdir}/ocaml/camlp4/Camlp4Parsers"


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/lablgtk2
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
make install \
     BINDIR=$RPM_BUILD_ROOT%{_bindir} \
     LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
     INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/lablgtk2 \
     DLLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
cp META $RPM_BUILD_ROOT%{_libdir}/ocaml/lablgtk2

# Remove unnecessary *.ml files (ones which have a *.mli).
pushd $RPM_BUILD_ROOT%{_libdir}/ocaml/lablgtk2
for f in *.ml; do \
  b=`basename $f .ml`; \
  if [ -f "$b.mli" ]; then \
    rm $f; \
  fi; \
done
popd

# Remove .cvsignore files from examples directory.
find examples -name .cvsignore -exec rm {} \;


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYING CHANGES
%dir %{_libdir}/ocaml/lablgtk2
%{_libdir}/ocaml/lablgtk2/*.cmi
%{_libdir}/ocaml/lablgtk2/*.cma
%{_libdir}/ocaml/lablgtk2/*.cmxs
%{_libdir}/ocaml/stublibs/*.so
%{_bindir}/gdk_pixbuf_mlsource
%{_bindir}/lablgladecc2
%{_bindir}/lablgtk2


%files devel
%defattr(-,root,root,-)
%doc README COPYING CHANGES
%dir %{_libdir}/ocaml/lablgtk2
%{_libdir}/ocaml/lablgtk2/META
%{_libdir}/ocaml/lablgtk2/*.a
%{_libdir}/ocaml/lablgtk2/*.cmxa
%{_libdir}/ocaml/lablgtk2/*.cmx
%{_libdir}/ocaml/lablgtk2/*.mli
%{_libdir}/ocaml/lablgtk2/*.ml
%{_libdir}/ocaml/lablgtk2/*.h
%{_libdir}/ocaml/lablgtk2/gtkInit.cmo
%{_libdir}/ocaml/lablgtk2/gtkInit.o
%{_libdir}/ocaml/lablgtk2/gtkThInit.cmo
%{_libdir}/ocaml/lablgtk2/gtkThread.cmo
%{_libdir}/ocaml/lablgtk2/gtkThread.o
%{_libdir}/ocaml/lablgtk2/propcc
%{_libdir}/ocaml/lablgtk2/varcc


%files doc
%defattr(-,root,root,-)
%doc examples doc/html


%changelog
* Thu Jul 15 2010 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-3
- Rebuild for EL-6 branch.

* Mon Sep 28 2009 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-2
- Ignore GtkSourceView2_types dependency (pure type-only *.cmi file).

* Mon Sep 28 2009 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-1
- New upstream version 2.14.0.
- Patch to fix ml_panel.c is now upstream, so removed.
- New *.cmxs files (dynamically linked OCaml native code) added to
  the base package.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.12.0-3
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 2.12.0-1
- New upstream version 2.12.0.
- Patch to include gnome-ui-init.h.
- gdk-pixbuf-mlsource was renamed gdk_pixbuf_mlsource (this will
  probably break things).

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-7
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-6
- Rebuild for OCaml 3.11.0

* Mon Sep 22 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-5
- Ignore bogus requires GtkSourceView_types.

* Thu Sep 18 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-4
- Add missing BR for gtksourceview-devel (rhbz#462651).

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10.1-3
- fix license tag

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-2
- Rebuild for OCaml 3.10.2

* Mon Apr 21 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-0
- New upstream release 2.10.1.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.0-3
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.0-2
- Rebuild for OCaml 3.10.1.

* Wed Nov  7 2007 Richard W.M. Jones <rjones@redhat.com> - 2.10.0-1
- New upstream release 2.10.0.
- Fix path to Camlp4Parsers in 'make doc' rule.

* Fri Sep  7 2007 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-10.20060908cvs
- rebuild

* Thu Aug 30 2007 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-9.20060908cvs
- rebuild

* Sat Jul  7 2007 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-8.20060908cvs
- update to cvs version
- renamed package from lablgtk to ocaml-lablgtk

* Sat Dec  2 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-7
- Rebuild for ocaml 3.09.3

* Tue Aug 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-6
- added BR: ncurses-devel

* Tue Aug 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-5
- Rebuild for FE6

* Wed May 10 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-4
- rebuilt for ocaml 3.09.2
- removed unnecessary ldconfig

* Sun Feb 26 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-3
- Rebuild for Fedora Extras 5

* Sun Jan  1 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-1
- new version 2.6.0

* Sat Sep 10 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.4.0-6
- include META file

* Sun May 22 2005 Toshio Kuratomi <toshio-iki-lounge.com> - 2.4.0-5
- Removed gnome-1.x BuildRequires
- Removed BuildRequires not explicitly mentioned in the configure script
  (These are dragged in through dependencies.)
- Fix a gcc4 error about lvalue casting.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:2.4.0-2
- Remove %{_smp_mflags} as it breaks the build

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:2.4.0-1
- New Version 2.4.0

* Sat Nov 13 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:2.2.0-5
- BR gnome-panel-devel instead of gnome-panel (since FC2!)

* Wed Apr 28 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:2.2.0-0.fdr.4
- Compile with debug

* Tue Dec  2 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:2.2.0-0.fdr.3
- Make GL support optional using --with gl switch

* Fri Nov 28 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:2.2.0-0.fdr.2
- Added dependency on libcroco
- Honor RPM_OPT_FLAGS

* Fri Oct 31 2003 Gerard Milmeister <milmei@ifi.unizh.ch> - 0:2.2.0-0.fdr.1
- First Fedora release

* Mon Oct 13 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Update to 2.2.0.

* Sun Aug 17 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Provide ocaml-lablgtk (reported by bishop@platypus.bc.ca).

* Wed Apr  9 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Rebuilt for Red Hat 9.

* Tue Nov 26 2002 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Initial build
