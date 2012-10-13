Name:           ragel   
Version:        6.6
Release:        2%{?dist}
Summary:        Finite state machine compiler

Group:          Development/Tools
License:        GPLv2+
URL:            http://www.complang.org/%{name}/
Source0:        http://www.complang.org/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# for documentation building
BuildRequires:  transfig, tetex-latex, gcc-objc
Requires:       gawk

%description
Ragel compiles finite state machines from regular languages into executable C,
C++, Objective-C, or D code. Ragel state machines can not only recognize byte
sequences as regular expression machines do, but can also execute code at
arbitrary points in the recognition of a regular language. Code embedding is
done using inline operators that do not disrupt the regular language syntax.

%prep
%setup -q

%build
# set the names of the other programming commandline programs
%configure --docdir=%{_docdir}/%{name}-%{version} RUBY=ruby JAVAC=javac GMCS=gmcs 

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING ragel.vim
%doc doc/ragel-guide.pdf
%{_bindir}/ragel
%{_mandir}/*/*

%changelog
* Thu Feb 18 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 6.6-2
- rebuilt

* Thu Feb 18 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 6.6-1
- Update to 6.6
- remove patch

* Sun Aug 02 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 6.5-2
- fix build process 

* Sun Aug 02 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 6.5.1
- Update to 6.5

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> 6.4-3
-  remove main.cpp patch for testing

* Sat Apr 11 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> 6.4-2
-  add patch for main.cpp

* Sat Apr 11 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> 6.4-1
-  Update to 6.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Aug 30 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 6.3-1
- update to 6.3

* Mon May 12 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 6.2-1
- update to 6.2

* Mon Apr 14 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 6.1-1
- update to 6.1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6.0-2
- Autorebuild for GCC 4.3

* Sat Jan 19 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 6.0-1
- update to 6.0

* Sun Jan 06 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 5.25-1
- update to 5.25

* Tue Sep 18 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 5.24-1
- update to 5.24
- update License tag

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 5.23-2
- Rebuild for selinux ppc32 issue.

* Tue Jul 24 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 5.23-1
- update to 5.23
- removed ragel-rlcodegen-replace.patch - it was applied upstream

* Mon Jun 18 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 5.22-1
- update to 5.22
- remove ragel-Makefile-in.patch - it was applied upstream
- update ragel-rlcodegen-replace.patch to apply cleanly

* Sat Mar 24 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 5.19-4
- further replacement of rlcodegen
- rework patches

* Fri Mar 23 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 5.19-3
- replace RPM_BUILD_ROOT in spec file with buildroot macro
- cleanup rpmlint errors for the src.rpm
- add ragel(1) man page patch

* Tue Mar 20 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 5.19-1
- Creation of spec file
