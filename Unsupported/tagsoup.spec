# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define gcj_support 1

%define section free

Name:           tagsoup
Version:        1.0.1
Release:        4.3%{?dist}
Epoch:          0
Summary:        A SAX-compliant HTML parser written in Java 
License:        GPLv2+ or AFL
Source0:        http://home.ccil.org/~cowan/XML/tagsoup/tagsoup-1.0.1-src.zip
URL:            http://home.ccil.org/~cowan/XML/tagsoup/
Group:          Text Processing/Markup/XML
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# see https://bugzilla.redhat.com/show_bug.cgi?id=502328
ExcludeArch:  ppc64
%if ! %{gcj_support}
BuildArch:      noarch
%endif
# Used to ensure that jpackage-utils is available till uninstallation of package
Requires:          jpackage-utils >= 0:1.6
Requires(postun):       jpackage-utils >= 0:1.6
BuildRequires:  ant, ant-trax, xalan-j2, /bin/bash

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%endif

%description 
TagSoup is a SAX-compliant parser written in Java that, instead of
parsing well-formed or valid XML, parses HTML as it is found in the wild: nasty
and brutish, though quite often far from short. TagSoup is designed for people
who have to process this stuff using some semblance of a rational application
design. By providing a SAX interface, it allows standard XML tools to be
applied to even the worst HTML.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation
# Used to ensure that jpackage-utils is available till uninstallation of package
Requires:               jpackage-utils >= 0:1.6
Requires(postun):       jpackage-utils >= 0:1.6

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

%build
ant \
  -Dversion=%{version} \
  -Dj2se.apiurl=%{_javadocdir}/java \
  dist docs-api

%install
rm -fr $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/lib/%{name}-%{version}.jar \
               $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/*.jar
%doc CHANGES README LICENSE

%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/tagsoup-1.0.1.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0.1-4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 24 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0:1.0.1-3.3
- Fix FTBFS: disabled ppc64 build

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0.1-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0.1-2.2
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.0.1-2jpp.1
- Autorebuild for GCC 4.3

* Mon Feb 12 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.0.1-1jpp.1.fc7
- rpmlint fixes
- Use fedora approved naming convention
- Fix buildroot to conform to Fedora packaging guidelines
- Add LICENSE to the rpm and label as doc
- Remove Vendor and Distribution tags
- Minor formatting fixes
- Use proper javaoc handling
- Add requires and requires(x) on jpackage-utils
- Add GCJ support
- BR on ant-trax and xalan-j2

* Sun Jan 20 2007 Sebastiano Vigna <vigna@dsi.unimi.it> 0:1.0.1-1jpp
- Upgraded to 1.0.1

* Mon Feb 27 2006 Fernando Nasser <fnasser@redhat.com> 0:1.0rc-2jpp
- First JPP 1.7 version

* Fri Jan 28 2005 Sebastiano Vigna <vigna@acm.org> 0:1.0rc-1jpp
- First JPackage version
