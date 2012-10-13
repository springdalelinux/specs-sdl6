Summary: Tool for generating C-based recognizers from regular expressions
Name: re2c
Version: 0.13.5
Release: 1%{?dist}
License: Public Domain
Group: Development/Tools
URL: http://re2c.org/
Source: http://downloads.sf.net/re2c/re2c-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
re2c is a tool for writing very fast and very flexible scanners. Unlike any
other such tool, re2c focuses on generating high efficient code for regular
expression matching. As a result this allows a much broader range of use than
any traditional lexer offers. And Last but not least re2c generates warning
free code that is equal to hand-written code in terms of size, speed and
quality.


%prep
%setup -q
# Fix all those executable files, set executable only the ones that need to be
find . -type f -exec chmod -x {} \;
%{__chmod} +x configure depcomp install-sh missing


%build
%configure
# Build re2c, then our own scanner.cc, then rebuild the final re2c with it
%{__make} %{?_smp_mflags} re2c
%{__rm} -f scanner.cc
./re2c -b -o scanner.cc scanner.re
%{__rm} -f re2c scanner.o
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__install} -D -p -m 0755 re2c %{buildroot}%{_bindir}/re2c
%{__install} -D -p -m 0644 re2c.1 %{buildroot}%{_mandir}/man1/re2c.1


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc CHANGELOG README examples/ doc/* lessons/
%{_bindir}/re2c
%{_mandir}/man1/re2c.1*


%changelog
* Mon Jul 12 2010 Matthias Saou <http://freshrpms.net/> 0.13.5-1
- Update to 0.13.5.
- Update URL to the one used in the included spec file.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.12.3-2
- Autorebuild for GCC 4.3

* Thu Sep 13 2007 Matthias Saou <http://freshrpms.net/> 0.12.3-1
- Update to 0.12.3.

* Thu Aug 23 2007 Matthias Saou <http://freshrpms.net/> 0.12.2-1
- Update to 0.12.2.
- Update URL location.

* Wed Jun 20 2007 Matthias Saou <http://freshrpms.net/> 0.12.1-2
- Fix license tag to "Public Domain".
- Update description with most recent text from the website.

* Wed Jun 20 2007 Matthias Saou <http://freshrpms.net/> 0.12.1-1
- Spec file changes.

* Wed May 23 2007 Dag Wieers <dag@wieers.com> - 0.12.1-1
- Updated to release 0.12.1.

* Thu May 03 2007 Dag Wieers <dag@wieers.com> - 0.12.0-1
- Initial version.

