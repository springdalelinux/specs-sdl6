# Copyright (c) 2000-2007, JPackage Project
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

%define _with_gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

Name:           xml-commons-apis12
Epoch:          0
Version:        1.2.04
Release:        3.5%{?dist}
Summary:        JAXP 1.2, DOM 2, SAX 2.0.1, SAX2-ext 1.0 apis
Group:          System Environment/Libraries
URL:            http://xml.apache.org/commons/
License:        ASL 2.0 and W3C and Public Domain
Source0:        xml-commons-external-1.2.04.tar.gz
# svn export http://svn.apache.org/repos/asf/xml/commons/tags/xml-commons-external-1_2_04/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       jaxp = 1.2
Provides:       dom = 2
Provides:       sax = 2.0.1
Provides:       xslt = 1.0

Requires:       jpackage-utils >= 0:1.6
%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%endif

BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.6
%if ! %{gcj_support}
BuildArch:      noarch
%endif

%description 
DOM 2 org.w3c.dom and SAX XML 2.0 org.xml.sax processor apis used 
by several pieces of Apache software. XSLT 1.0.
This version includes the JAXP 1.2 APIs -- Java API for XML 
Processing 1.2, i.e. javax.xml{.parsers,.transform}

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Provides:       %{name}-apis-javadoc = %{epoch}:%{version}-%{release}

%description javadoc
%{summary}.

%package manual
Group:          Documentation
Summary:        Documents for %{name}

%description manual
%{summary}.

%prep
%setup -q -c

%build
ant -f xml-commons-external-1_2_04/java/external/build.xml jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 xml-commons-external-1_2_04/java/external/build/xml-apis.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

pushd $RPM_BUILD_ROOT%{_javadir}
for jar in *-%{version}*; do
ln -sf ${jar} $(echo $jar | sed -e 's|-%{version}\.jar|.jar|');
done

ln -sf %{name}.jar xml-commons-jaxp-1.2-apis.jar
ln -sf %{name}.jar jaxp12.jar
ln -sf %{name}.jar dom2.jar
popd


# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr xml-commons-external-1_2_04/java/external/build/docs/javadoc/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf xml-commons-external-1_2_04/java/external/build/docs/javadoc

# manuals
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr xml-commons-external-1_2_04/java/external/build/docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

# -----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# -----------------------------------------------------------------------------

%files 
%defattr(0644,root,root,0755)
%{_javadir}/%{name}*.jar
%{_javadir}/jaxp12.jar
%{_javadir}/dom2.jar
%{_javadir}/xml-commons-jaxp-1.2-apis.jar
%doc xml-commons-external-1_2_04/java/external/LICENSE
%doc xml-commons-external-1_2_04/java/external/LICENSE.dom-documentation.txt
%doc xml-commons-external-1_2_04/java/external/LICENSE.dom-software.txt
%doc xml-commons-external-1_2_04/java/external/LICENSE.sax.txt
%doc xml-commons-external-1_2_04/java/external/README.dom.txt
%doc xml-commons-external-1_2_04/java/external/README-sax
%doc xml-commons-external-1_2_04/java/external/README.sax.txt
%doc xml-commons-external-1_2_04/java/external/NOTICE

%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%{_docdir}/%{name}-%{version}

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

# -----------------------------------------------------------------------------

%changelog
* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.04-3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.04-2.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.2.04-1.5
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.2.04-1jpp.4
- Autorebuild for GCC 4.3

* Sun Jun 03 2007 Florian La Roche <laroche@redhat.com> - 0:1.2.04-0jpp.4
- the javadoc subrpm used an undefined macro

* Tue Apr 12 2007 Matt Wringe <mwringe@redhat.com> - 0:1.2.04-0jpp.3
- Remove the provides on xml-commons-apis = 1.2 since this will not
  work properly with our other xml-commons-apis package.

* Tue Mar 13 2007 Matt Wringe <mwringe@redhat.com> - 0:1.2.04-0jpp.2
- Enable gcj option

* Thu Feb 16 2007 Matt Wringe <mwringe@redhat.com> - 0:1.2.04-0jpp.1
- Initial build. Based heavily on the xml-commons 1.3.03-7jpp spec file.
