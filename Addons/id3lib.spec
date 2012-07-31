Summary:        Library for manipulating ID3v1 and ID3v2 tags
Name:           id3lib
Version:        3.8.3
Release:        24%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://id3lib.sourceforge.net/
Source0:        http://downloads.sourceforge.net/id3lib/%{name}-%{version}.tar.gz
Source1:        id3lib-no_date_footer.hml
Patch0:         id3lib-dox.patch
Patch1:         id3lib-3.8.3-libtool-autofoo.patch.bz2
Patch2:         id3lib-3.8.3-io_helpers-163101.patch
Patch3:         id3lib-3.8.3-mkstemp.patch
Patch4:         id3lib-3.8.3-includes.patch
Patch5:         http://launchpadlibrarian.net/33114077/id3lib-vbr_buffer_overflow.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  zlib-devel doxygen

%description
This package provides a software library for manipulating ID3v1 and
ID3v2 tags. It provides a convenient interface for software developers
to include standards-compliant ID3v1/2 tagging capabilities in their
applications. Features include identification of valid tags, automatic
size conversions, (re)synchronisation of tag frames, seamless tag
(de)compression, and optional padding facilities. Additionally, it can
tell mp3 header info, like bitrate etc.


%package devel
Summary:        Development tools for the id3lib library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       zlib-devel

%description devel
This package provides files needed to develop with the id3lib library.


%prep
%setup -q
%patch0 -p0
%patch1 -p1 -b .libtool-autofoo
%patch2 -p1 -b .io_helpers-163101
%patch3 -p1 -b .mkstemp
%patch4 -p1 -b .gcc43
%patch5 -p1
chmod -x src/*.h src/*.cpp include/id3/*.h
sed -i -e 's/\r//' doc/id3v2.3.0.*
sed -i -e 's|@DOX_DIR_HTML@|%{_docdir}/%{name}-devel-%{version}/api|' \
  doc/index.html.in
iconv -f ISO-8859-1 -t UTF8 ChangeLog > tmp; mv tmp ChangeLog
iconv -f ISO-8859-1 -t UTF8 THANKS > tmp; mv tmp THANKS
sed -i -e "s,HTML_FOOTER.*$,HTML_FOOTER = id3lib-no_date_footer.hml,g" doc/Doxyfile.in
cp %{SOURCE1} doc


%build
%configure --disable-dependency-tracking --disable-static
make %{?_smp_mflags} libid3_la_LIBADD=-lz


%install
rm -rf $RPM_BUILD_ROOT __doc
make install DESTDIR=$RPM_BUILD_ROOT
make docs
for i in txt html; do
  iconv -f ISO-8859-1 -t UTF8 doc/id3v2.3.0.$i > tmp; mv tmp doc/id3v2.3.0.$i
done
mkdir -p __doc/doc ; cp -p doc/*.{gif,jpg,png,html,txt,ico,css}  __doc/doc
rm -f $RPM_BUILD_ROOT%{_libdir}/libid3.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog HISTORY NEWS README THANKS TODO __doc/doc/
%{_libdir}/libid3-3.8.so.*
%{_bindir}/id3convert
%{_bindir}/id3cp
%{_bindir}/id3info
%{_bindir}/id3tag

%files devel
%defattr(-,root,root,-)
%doc doc/id3lib.css doc/api/
%{_includedir}/id3.h
%{_includedir}/id3/
%{_libdir}/libid3.so


%changelog
* Thu Nov 12 2009 Adrian Reber <adrian@lisas.de> - 3.8.3-24
- Fix "Stack smashing with vbr mp3 files" (bz #533706)
  also see https://bugs.launchpad.net/ubuntu/+source/id3lib3.8.3/+bug/444466

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Adrian Reber <adrian@lisas.de> - 3.8.3-22
- Fix "id3lib-devel multilib conflict" (bz #507700)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.8.3-20
- Autorebuild for GCC 4.3

* Fri Dec  4 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.8.3-19
- Fix building of id3lib and programs using it with gcc34
- Drop prebuild doxygen docs, now that doxygen is fixed to not cause multilib
  conflicts
- Convert some docs to UTF-8 

* Sun Oct 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.8.3-18
- Fix multilib api documentation conflict (bz 341551)

* Mon Aug 20 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.8.3-17
- Use mkstemp instead of insecure tempfile creation (bz 253553)

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.8.3-16
- Update License tag for new Licensing Guidelines compliance

* Wed Nov 22 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 3.8.3-15
- Link libid3-3.8.so.3 with -lz (bug #216783)

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 3.8.3-14
- Taking over as maintainer since Anvil has other priorities
- FE6 Rebuild

* Sat Feb 18 2006 Ville Skyttä <ville.skytta at iki.fi> - 3.8.3-13
- Don't ship static libs.
- Build with dependency tracking disabled.
- Don't use %%exclude.
- Drop unneeded cruft from docs, move API docs to -devel.
- Clean up some cosmetic rpmlint warnings.

* Sat Jul 16 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 3.8.3-12
- Fix UTF-16 writing bug (bug #163101, upstream #1016290).

* Thu Jun 30 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 3.8.3-11
- Make libtool link against libstdc++ (bug #162127).

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 3.8.3-10
- rebuilt

* Wed Oct 29 2003 Ville Skytta <ville.skytta at iki.fi> - 0:3.8.3-0.fdr.9
- Rebuild.

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:3.8.3-0.fdr.8
- Removed comment after scriptlets

* Mon May  5 2003 Dams <anvil[AT]livna.org> 0:3.8.3-0.fdr.7
- libid3-3.8.so.3.0.0 -> libid3-3.8.so.*
- {buildroot} -> RPM_BUILD_ROOT

* Sun Apr 27 2003 Dams <anvil[AT]livna.org> 0:3.8.3-0.fdr.6
- Added post/postun scriptlets

* Thu Apr 24 2003 Dams <anvil[AT]livna.org> 0:3.8.3-0.fdr.5
- Added zlib-devel require tag for -devel package

* Fri Apr  4 2003 Dams <anvil[AT]livna.org> 0:3.8.3-0.fdr.4
- Added URL in Source:

* Thu Apr  3 2003 Dams <anvil[AT]livna.org> 0:3.8.3-0.fdr.3
- added ".so" file to the devel package

* Thu Apr  3 2003 Dams <anvil[AT]livna.org> 0:3.8.3-0.fdr.2
- Added missing epoch requirement

* Wed Apr  2 2003 Dams <anvil[AT]livna.org>
- Initial build.
