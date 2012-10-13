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

%define oversion 1.1.3_8

Summary:        XML Pull Parser
Name:           xpp3
Version:        1.1.3.8
Release:        3.3%{?dist}
Epoch:          0
License:        ASL 1.1
URL:            http://www.extreme.indiana.edu/xgws/xsoap/xpp/mxp1/index.html
Group:          Text Processing/Markup/XML
Source0:        http://www.extreme.indiana.edu/dist/java-repository/xpp3/distributions/xpp3-%{oversion}_src.tgz
Patch0:         %{name}-link-docs-locally.patch
Requires:       jpackage-utils >= 0:1.6
Requires:       java >= 0:1.4.2
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  junit
BuildRequires:  xml-commons-apis
BuildRequires:  /usr/bin/perl
Requires:       jpackage-utils
Requires:       junit
Requires:       xml-commons-apis
Requires:       java
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Xml Pull Parser 3rd Edition (XPP3) MXP1 is a new XmlPull
parsing engine that is based on ideas from XPP and in
particular XPP2 but completely revised and rewritten to
take best advantage of latest JIT JVMs such as Hotspot in JDK 1.4.

%package minimal
Summary:        Minimal XML Pull Parser
Group:          Text Processing/Markup/XML
Requires:       jpackage-utils
Requires:       junit
Requires:       xml-commons-apis
Requires:       java

%description minimal
Minimal XML pull parser implementation.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{oversion}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%patch0

%build
export CLASSPATH=$(build-classpath xml-commons-apis junit)
ant xpp3 junit apidoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{name}-%{oversion}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p build/%{name}_min-%{oversion}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-minimal-%{version}.jar
cp -p build/%{name}_xpath-%{oversion}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-xpath-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; \
  do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

rm -rf doc/{build.txt,api}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc README.html LICENSE.txt doc/*
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}-xpath.jar
%{_javadir}/%{name}-xpath-%{version}.jar

%files minimal
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%{_javadir}/%{name}-minimal.jar
%{_javadir}/%{name}-minimal-%{version}.jar

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/*

%changelog
* Wed Mar 10 2010 Peter Lemenkov <lemenkov@gmail.com> - 0:1.1.3.8-3.3
- *-javadoc must also require jpackage-utils (for %%{_javadocdir})

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.1.3.8-1.2
- fix license tag
- drop jpp tag

* Mon Feb 12 2007 Fernando Nasser <fnasser@redhat.com> - 0:1.1.3.8-1jpp.1
- Import
- Fix per Fedora spec

* Mon Feb 12 2007 Fernando Nasser <fnasser@redhat.com> - 0:1.1.3.8-1jpp
- Upgrade to 1.1.3.8
- Remove vendor and distribution tags

* Mon Feb 27 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.1.3.4-1.o.2jpp
- First JPP 1.7 build

* Tue Dec 20 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3.4-1.o.1jpp
- Upgrade to 1.1.3.4-O
- Now includes xpath support

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3.4-1.d.2jpp
- Build with ant-1.6.2

* Tue Jun 01 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3.4-1.d.1jpp
- Update to 1.1.3.4

* Mon May  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-1.a.3jpp
- Fix non-versioned javadoc symlinking.

* Mon Apr 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-1.a.2jpp
- Include non-versioned javadoc symlink.

* Tue Apr  1 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-1.a.1jpp
- First JPackage release.
