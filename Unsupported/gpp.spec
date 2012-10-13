Summary:	GNOME Photo Printer
Name:           gpp
Version:	0.7.0
Release:	1
Source:         http://www.fogman.de/%{name}/%{name}-%{version}.tar.gz
License:	GPL
Group:		Applications/Publishing
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libgnomeui-devel libgnomeprintui22-devel libgnomeprint22-devel libglade2-devel perl-XML-Parser gettext
Packager:	Damian Ivereigh
Requires:	libgnomeui libgnomeprint22 libgnomeprintui22 libglade2 perl-XML-Parser

%define longname	gnome-photo-printer
%define _iconsdir	%{_datadir}/icons/hicolor/

%description
Gnome Photo Printer is intended for printing photos in an easy way.
Just drag your Photos from Nautilus to the Gnome Photo Printer window
and drop it.  Make some selections like Photo or Paper size, hit Preview
or  Print , and see your pictures printed.

%prep
%setup -q

%build
%configure
CFLAGS="$RPM_OPT_FLAGS" make

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}
ln -s %{longname} ${RPM_BUILD_ROOT}/%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT 

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/%{longname}
%{_datadir}/applications/%{longname}.desktop
%{_iconsdir}/scalable/apps/%{longname}.svg
%{_iconsdir}/16x16/apps/%{longname}.png
/%{_iconsdir}/22x22/apps/%{longname}.png
/%{_iconsdir}/32x32/apps/%{longname}.png
/%{_iconsdir}/48x48/apps/%{longname}.png
%{_datadir}/locale/de/LC_MESSAGES/%{longname}.mo


%changelog
* Wed Apr 04 2012 Thomas Uphill <uphill@ias.edu> 0.7.0-1
- updating for puias6

* Fri Oct 24 2003 Damian Ivereigh <damian@cisco.com>
- autoconf'ed & automake'd the whole system

* Sat Oct 18 2003 Damian Ivereigh <damian@cisco.com>
- Initial version
