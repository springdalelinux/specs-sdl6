Name:           y4mscaler
Version:        9.0
Release:        9%{?dist}
Summary:        Video scaler which operates on YUV4MPEG2 streams

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://www.mir.com/DMG/Software/
Source0:        http://www.mir.com/DMG/Software/%{name}-%{version}-src.tgz
Patch0:         y4mscaler-9.0-new-mjpegtools.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mjpegtools-devel >= 1.6.3

%description
y4mscaler is a video scaler which operates on YUV4MPEG2 streams, as
used by the tools in the MJPEGtools project.  It essentially takes
some region of an input stream, and scales it into some region of the
output stream.


%prep
%setup -q
%patch0 -p1


%build
make %{?_smp_mflags} CXX="%{__cxx}" COPT="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 755 y4mscaler $RPM_BUILD_ROOT%{_bindir}/y4mscaler
install -Dpm 644 y4mscaler.1 $RPM_BUILD_ROOT%{_mandir}/man1/y4mscaler.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README TODO
%{_bindir}/y4mscaler
%{_mandir}/man1/y4mscaler.1*


%changelog
* Wed Dec 14 2011 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild for new mjpegtools (2.0.0)

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.0-8
- rebuild for new F11 features

* Sat Aug 16 2008 Hans de Goede <jwrdegoede@fedoraproject.org> 9.0-7
- Fix build with new mjpegtools

* Sat Aug 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 9.0-6
- rebuild

* Wed Aug 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 9.0-5
- License: GPLv2+

* Fri Jun  8 2007 Ville Skyttä <ville.skytta at iki.fi> - 9.0-4
- Rebuild.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 9.0-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Ville Skyttä <ville.skytta at iki.fi> - 9.0-2
- Rebuild.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Mon Dec 12 2005 Ville Skyttä <ville.skytta at iki.fi> - 9.0-0.lvn.1
- 9.0.

* Sun Oct  9 2005 Dams <anvil[AT]livna.org> - 8.1-0.lvn.5
- Really rebuild against mjpegtools

* Mon Sep 26 2005 Thorsten Leemhuis <fedoral[AT]leemhuis.info> - 8.1-0.lvn.4
- Rebuilt against new mjpegtools

* Tue Aug 30 2005 Dams <anvil[AT]livna.org> - 8.1-0.lvn.3
- Rebuilt against new mjpegtools

* Thu May 26 2005 Ville Skyttä <ville.skytta at iki.fi> - 8.1-0.lvn.2
- Lower mjpegtools-devel build dependency to 1.6.3.

* Sat May 21 2005 Ville Skyttä <ville.skytta at iki.fi> - 8.1-0.lvn.1
- 8.1.

* Fri Dec 31 2004 Ville Skyttä <ville.skytta at iki.fi> - 0.6.2-0.lvn.1
- First build.
