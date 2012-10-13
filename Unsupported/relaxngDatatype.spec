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

Name:           relaxngDatatype
Version:        1.0
Release:        5.3%{?dist}
Summary:        RELAX NG Datatype API

Group:          Development/Libraries/Java
License:        BSD
URL:            https://sourceforge.net/projects/relaxng
Source0:        %{name}-%{version}.zip
Patch0:         %{name}-compressjar.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
Requires:       jpackage-utils
Provides:       msv <= %{version}
Obsoletes:      msv <= %{version}

%description
RELAX NG is a public space for test cases and other ancillary software
related to the construction of the RELAX NG language and its
implementations.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation
Requires:       jpackage-utils

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch0 -p0

%build
ant -Dbuild.sysclasspath=only
sed -i 's/\r//g' copying.txt

%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 644 %{name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
pushd $RPM_BUILD_ROOT%{_javadocdir}/%{name}
for f in `find -name \*.html -o -name \*.css`; do
    sed -i 's/\r//g' $f > /dev/null
done
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc copying.txt
%{_javadir}/*.jar

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}*

%changelog
* Mon Mar  8 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.0-5.3
- Added missing Requires: jpackage-utils (%%{_javadir} and %%{_javadocdir})

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-3.2
- drop repotag

* Mon Feb 12 2007 Andrew Overholt <overholt@redhat.com> 1.0-3jpp.1
- Fixed issues for Fedora-ization
- Add patch to compress the main jar

* Tue Apr 11 2006 Ralph Apel <r.apel@r-apel.de>- 0:1.0-3jpp
- First JPP-1.7 release

* Wed Aug 25 2004 Fernando Nasser <fnasser@redhat.com>- 0:1.0-2jpp
- Require Ant > 1.6
- Rebuild with Ant 1.6.2

* Tue Jul 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-1jpp
- First JPackage build from sources

