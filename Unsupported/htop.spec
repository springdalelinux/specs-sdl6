Name:           htop
Version:        0.8.3
Release:        2%{?dist}
Summary:        Interactive process viewer
Summary(pl):    Interaktywna przeglądarka procesów

Group:          Applications/System
License:        GPL+
URL:            http://htop.sourceforge.net/
Source0:        http://download.sourceforge.net/htop/%{name}-%{version}.tar.gz
#Patch0:         %{name}-0.8.1-nonprint.patch
#Patch1:         %{name}-0.8.1-processlist.patch
#Patch2:         %{name}-0.8.2-arrays.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  ncurses-devel, python

%description
htop is an interactive text-mode process viewer for Linux, similar to
top(1).

%description -l pl
htop to interaktywna tekstowa przeglądarka procesów dla Linuksa podobna
do top(1).


%prep
%setup -q
#%patch0 -p0
#%patch1 -p0
#%patch2 -p0
sed -i s#"INSTALL_DATA = @INSTALL_DATA@"#"INSTALL_DATA = @INSTALL_DATA@ -p"# Makefile.in
#sed -i -e '2,3d' -e '9d' htop.desktop

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications \
        --vendor fedora \
        --delete-original \
        $RPM_BUILD_ROOT%{_datadir}/applications/htop.desktop

#remove empty direcories
rm -rf $RPM_BUILD_ROOT%{libdir}
rm -rf $RPM_BUILD_ROOT%{includedir}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO
%{_bindir}/htop
%{_datadir}/applications/fedora-htop.desktop
%{_datadir}/pixmaps/htop.png
%{_mandir}/man1/htop.1*


%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Rafał Psota <rafalzaq@gmail.com> - 0.8.3-1
- update to 0.8.3

* Fri Jun 12 2009 Rafał Psota <rafalzaq@gmail.com> - 0.8.2-2
- "htop aborts after hitting F6 key" fixed (#504795)

* Tue Jun 02 2009 Rafał Psota <rafalzaq@gmail.com> - 0.8.2-1
- update to 0.8.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 05 2009 Rafał Psota <rafalzaq@gmail.com> - 0.8.1-3
- "Tree view doesn't work with threads hidden" fixed (#481072)

* Tue Nov 18 2008 Rafał Psota <rafalzaq@gmail.com> - 0.8.1-2
- non-printable character filter patch (#504144)

* Tue Oct 14 2008 Rafał Psota <rafalzaq@gmail.com> - 0.8.1-1
- update to 0.8.1

* Thu Jul 31 2008 Rafał Psota <rafalzaq@gmail.com> - 0.8-1
- update to 0.8

* Sun Apr 27 2008 Rafał Psota <rafalzaq@gmail.com> - 0.7-2
- desktop file fix

* Mon Feb 11 2008 Rafał Psota <rafalzaq@gmail.com> - 0.7-1
- update to 0.7

* Sat Dec  9 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.5-1
- Update to 0.6.5

* Wed Oct  4 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.4-1
- Update to 0.6.4

* Sat Sep 16 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.3-2
- Rebuild for FE6

* Sun Jul 30 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.3-1
- Update to 0.6.3
- Correct e-mail address in ChangeLog
- Replace tabs with spaces

* Sat May 20 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.2-1
- Update to 0.6.2

* Wed May 10 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.1-2
- Add missing BR: desktop-file-utils

* Wed May 10 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.1-1
- Update to 0.6.1

* Tue Feb 14 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6-3
- Rebuild for Fedora Extras 5

* Wed Dec 28 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6-2
- Rebuild with updated tarball

* Wed Dec 28 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6-1
- Version 0.6

* Fri Nov 11 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.5.4-2
- Don't use superflous CFLAGS variable (Dmitry Butskoy)
- Don't include AUTHORS and NEWS files

* Thu Nov 10 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.5.4-1
- Initial RPM release.
