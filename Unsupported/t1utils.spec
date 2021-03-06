Name:		t1utils
Version:	1.36
Release:	2%{?dist}

Summary:	Collection of Type 1 and 2 font manipulation utilities

Group:		Applications/Publishing
# The Click license is an MIT variant.
License:	MIT
URL:		http://www.lcdf.org/~eddietwo/type/
Source0:	http://www.lcdf.org/~eddietwo/type/t1utils-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
t1utils is a collection of programs for manipulating PostScript type 1
and type 2 fonts containing programs to convert between PFA (ASCII)
format, PFB (binary) format, a human-readable and editable ASCII
format, and Macintosh resource forks.


%prep
%setup -q
iconv -f iso-8859-1 -t utf-8 -o NEWS{.utf8,}
mv NEWS{.utf8,}

%build
%configure
make  %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc NEWS README
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Robert Scheck <robert@fedoraproject.org> 1.36-1
- Update to 1.36

* Thu Jul 30 2009 José Matos <jamatos@fc.up.pt> - 1.34-1
- New upstream release and fix issue with stricter gcc.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.33-1
- fix license tag
- update to 1.33

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.32-10
- Autorebuild for GCC 4.3

* Tue Aug 28 2007 José Matos <jamatos[AT]fc.up.pt> - 1.32-9
- License fix, rebuild for devel (F8).

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.32-8
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 José Matos <jamatos[AT]fc.up.pt> - 1.32-7
- Rebuild for FC-6.

* Tue Feb 14 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.32-6
- Rebuild for Fedora Extras 5

* Tue Jan 17 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.32-5
- rebuild

* Mon Jan 16 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.32-4
- add %%{?dist} tag
- correct License

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.32-3
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue May 11 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.32-0.fdr.1
- Updated to 1.32.

* Wed Oct 22 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.29-0.fdr.1
- Updated to 1.29.

* Sat Aug 30 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.28-0.fdr.1
- Initial Fedora RPM release.

