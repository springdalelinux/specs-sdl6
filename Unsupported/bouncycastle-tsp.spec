%global with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}
%global ver 1.45
%global archivever  jdk16-%(echo %{ver}|sed 's|\\\.||')

Summary:          TSP libraries for Bouncy Castle
Name:             bouncycastle-tsp
Version:          %{ver}
Release:          1%{?dist}
Group:            System Environment/Libraries
License:          MIT
URL:              http://www.bouncycastle.org/
Source0:          http://www.bouncycastle.org/download/bctsp-%{archivever}.tar.gz
Source1:          http://repo2.maven.org/maven2/org/bouncycastle/bctsp-jdk16/%{version}/bctsp-jdk16-%{version}.pom
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    jpackage-utils >= 1.5
Requires:         jpackage-utils >= 1.5
Requires(post):   jpackage-utils >= 1.7
Requires(postun): jpackage-utils >= 1.7
%if %{with_gcj}
Requires:         java-1.5.0-gcj
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:    java-gcj-compat-devel
%else
BuildArch:        noarch
%endif
BuildRequires:    bouncycastle-mail = %{version}
Requires:         bouncycastle-mail = %{version}
BuildRequires:    java-devel >= 1.7
Requires:         java >= 1.7
BuildRequires:    junit4

Provides:         bctsp = %{version}-%{release}

%description
Bouncy Castle consists of a lightweight cryptography API and is a provider 
for the Java Cryptography Extension and the Java Cryptography Architecture.
This library package offers additional classes, in particuar 
generators/processors for Time Stamp Protocol (TSP), for Bouncy Castle.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
API documentation for the %{name} package.

%prep
%setup -q -n bctsp-%{archivever}
mkdir src
unzip -qq src.zip -d src/
# Remove provided binaries
find . -type f -name "*.class" -exec rm -f {} \;
find . -type f -name "*.jar" -exec rm -f {} \;

%build
pushd src
  export CLASSPATH=$(build-classpath bcprov bcmail junit4)
  %javac -g -target 1.5 -encoding UTF-8 $(find . -type f -name "*.java")
  jarfile="../bctsp-%{version}.jar"
  # Exclude all */test/* , cf. upstream
  files="$(find . -type f \( -name '*.class' -o -name '*.properties' \) -not -path '*/test/*')"
  test ! -d classes && mf="" \
    || mf="`find classes/ -type f -name "*.mf" 2>/dev/null`"
  test -n "$mf" && %jar cvfm $jarfile $mf $files \
    || %jar cvf $jarfile $files
popd

%install
rm -rf $RPM_BUILD_ROOT

# install bouncy castle tsp
install -dm 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 bctsp-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/bctsp-%{version}.jar
pushd $RPM_BUILD_ROOT%{_javadir}
  ln -sf bctsp-%{version}.jar bctsp.jar
popd
install -dm 755 $RPM_BUILD_ROOT%{_javadir}/gcj-endorsed
pushd $RPM_BUILD_ROOT%{_javadir}/gcj-endorsed
  ln -sf ../bctsp-%{version}.jar bctsp-%{version}.jar
popd
%if %{with_gcj}
  %{_bindir}/aot-compile-rpm
%endif

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# maven pom
install -dm 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-bctsp.pom
%add_to_maven_depmap org.bouncycastle bctsp-jdk16 %{version} JPP bctsp

%check
pushd src
  export CLASSPATH=$PWD:$(build-classpath junit4 bcprov bcmail)
  for test in $(find . -name AllTests.class) ; do
    test=${test#./} ; test=${test%.class} ; test=${test//\//.}
    %java org.junit.runner.JUnitCore $test
  done
popd

%post
%update_maven_depmap
%if %{with_gcj}
  if [ -x %{_bindir}/rebuild-gcj-db ]; then
    %{_bindir}/rebuild-gcj-db
  fi
%endif

%postun
%update_maven_depmap
%if %{with_gcj}
  if [ -x %{_bindir}/rebuild-gcj-db ]; then
    %{_bindir}/rebuild-gcj-db
  fi
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc *.html
%{_javadir}/bctsp.jar
%{_javadir}/bctsp-%{version}.jar
%{_javadir}/gcj-endorsed/bctsp-%{version}.jar
%{_mavenpomdir}/JPP-bctsp.pom
%{_mavendepmapfragdir}/%{name}
%if %{with_gcj}
  %{_libdir}/gcj/%{name}/
%endif

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}/

%changelog
* Thu Feb 11 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.45-1
- Import Bouncy Castle 1.45.

* Sat Nov 14 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.44-1
- Import Bouncy Castle 1.44.

* Thu Sep 17 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-6
- Similar fixes proposed in RHBZ#521475, namely:
- Include missing properties files in jar.
- Build with javac -encoding UTF-8.
- Use %%javac and %%jar macros.
- Run test suite during build.
- Follow upstream in excluding various test suite classes from jar.
- Remove R: junit4

* Wed Aug 26 2009 Andrew Overholt <overholt@redhat.com> 1.43-5
- Add maven POM

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 13 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-3
- Re-enable AOT bits thanks to Andrew Haley.

* Sun Jun 21 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-2
- Minor cleanup in the spec file

* Tue Jun 16 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-1
- Initial build (Spec file stolen from bouncycastle-mail and modified for bctsp)
