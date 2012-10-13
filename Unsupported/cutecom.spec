Summary: A graphical serial terminal, like minicom or Hyperterminal on Windows
Name: cutecom
Version: 0.22.0
Release: 1%{?dist}
License: GPLv2+
Group: Applications/Communications
URL: http://cutecom.sourceforge.net/

# The source for this package is released at sourceforge:
Source: http://cutecom.sourceforge.net/%{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake
BuildRequires: qt4-devel
BuildRequires: desktop-file-utils

%description
CuteCom is a graphical serial terminal, like minicom or Hyperterminal on 
Windows. It is aimed mainly at hardware developers or other people who need 
a terminal to talk to their devices. 

%prep
%setup -q
# Change icon to "utilities-terminal":
sed 's/=openterm/=utilities-terminal/' cutecom.desktop > cutecom.desktop.new
mv -f cutecom.desktop.new cutecom.desktop

%build
%cmake .
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
# We don't invoke upstream's make install since the man file is installed in 
#  a wrong directory (/usr/man/...)
# make install DESTDIR=$RPM_BUILD_ROOT

install -D -m 755 $(pwd)/cutecom ${RPM_BUILD_ROOT}%{_bindir}/cutecom
install -D -m 644 $(pwd)/cutecom.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/cutecom.1


# Upstream script does not install the .desktop file if KDE is not installed, 
# so we install it manually:
desktop-file-install \
   --remove-key=Path --remove-key=Encoding \
   --remove-key=BinaryPattern --remove-key=TerminalOptions \
   --add-category=System \
   --dir ${RPM_BUILD_ROOT}%{_datadir}/applications/ \
   $(pwd)/cutecom.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING README Changelog TODO
%{_bindir}/cutecom
%{_mandir}/man1/cutecom.1*
%{_datadir}/applications/cutecom.desktop 


%changelog
* Mon Jan 16 2012 Rich Mattes <richmattes@gmail.com> - 0.22.0-1
- Update to release 0.22.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 - Jose Luis Blanco <joseluisblancoc@gmail.com> 0.20.0-3
- Fixed .desktop file and .spec file comments.

* Tue Feb 17 2009 - Jose Luis Blanco <joseluisblancoc@gmail.com> 0.20.0-2
- Added documentation files.
- Fixed License field.
- .desktop file installed with desktop-file-install

* Sun Feb 15 2009 - Jose Luis Blanco <joseluisblancoc@gmail.com> 0.20.0-1
- Initial packaging for Fedora.

