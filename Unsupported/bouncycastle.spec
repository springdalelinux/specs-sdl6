%global with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}
%global ver  1.45
%global archivever  jdk16-%(echo %{ver}|sed 's|\\\.||')
%global classname   org.bouncycastle.jce.provider.BouncyCastleProvider

Summary:          Bouncy Castle Crypto Package for Java
Name:             bouncycastle
Version:          %{ver}
Release:          1%{?dist}
Group:            System Environment/Libraries
License:          MIT
URL:              http://www.%{name}.org/
# Original source http://www.bouncycastle.org/download/bcprov-%{archivever}.tar.gz
# is modified to
# bcprov-%{archivever}-FEDORA.tar.gz with patented algorithms removed.
# Specifically: IDEA algorithms got removed.
Source0:          bcprov-%{archivever}-FEDORA.tar.gz
Source1:          http://repo2.maven.org/maven2/org/bouncycastle/bcprov-jdk16/%{version}/bcprov-jdk16-%{version}.pom
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
BuildRequires:    java-devel >= 1.7
Requires:         java >= 1.7
BuildRequires:    junit4

Provides:         bcprov = %{version}-%{release}

%description
The Bouncy Castle Crypto package is a Java implementation of cryptographic
algorithms. The package is organised so that it contains a light-weight API
suitable for use in any environment (including the newly released J2ME) with
the additional infrastructure to conform the algorithms to the JCE framework.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
API documentation for the %{name} package.

%prep
%setup -q -n bcprov-%{archivever}

# Remove provided binaries
find . -type f -name "*.class" -exec rm -f {} \;
find . -type f -name "*.jar" -exec rm -f {} \;

mkdir src
unzip -qq src.zip -d src/

%build
pushd src
  export CLASSPATH=$(build-classpath junit4)
  %javac -g -target 1.5 -encoding UTF-8 $(find . -type f -name "*.java")
  jarfile="../bcprov-%{version}.jar"
  # Exclude all */test/* files except org.bouncycastle.util.test, cf. upstream
  files="$(find . -type f \( -name '*.class' -o -name '*.properties' \) -not -path '*/test/*')"
  files="$files $(find . -type f -path '*/org/bouncycastle/util/test/*.class')"
  test ! -d classes && mf="" \
    || mf="`find classes/ -type f -name "*.mf" 2>/dev/null`"
  test -n "$mf" && jar cvfm $jarfile $mf $files \
    || %jar cvf $jarfile $files
popd

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/java/security/security.d
touch $RPM_BUILD_ROOT%{_sysconfdir}/java/security/security.d/2000-%{classname}

# install bouncy castle provider
install -dm 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 bcprov-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/bcprov-%{version}.jar
pushd $RPM_BUILD_ROOT%{_javadir}
  ln -sf bcprov-%{version}.jar bcprov.jar
popd
  install -dm 755 $RPM_BUILD_ROOT%{_javadir}/gcj-endorsed
  pushd $RPM_BUILD_ROOT%{_javadir}/gcj-endorsed
    ln -sf ../bcprov-%{version}.jar bcprov-%{version}.jar
  popd
%if %{with_gcj}
  %{_bindir}/aot-compile-rpm
%endif

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# maven pom
install -dm 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-bcprov.pom
%add_to_maven_depmap org.bouncycastle bcprov-jdk16 %{version} JPP bcprov

%check
pushd src
  export CLASSPATH=$PWD:$(build-classpath junit4)
  for test in $(find . -name AllTests.class) ; do
    test=${test#./} ; test=${test%.class} ; test=${test//\//.}
    # TODO: failures; get them fixed and remove || :
    %java org.junit.runner.JUnitCore $test || :
  done
popd


%post
{
  # Rebuild the list of security providers in classpath.security
  suffix=security/classpath.security
  secfiles="/usr/lib/$suffix /usr/lib64/$suffix"

  for secfile in $secfiles
  do
    # check if this classpath.security file exists
    [ -f "$secfile" ] || continue

    sed -i '/^security\.provider\./d' "$secfile"

    count=0
    for provider in $(ls /etc/java/security/security.d)
    do
      count=$((count + 1))
      echo "security.provider.${count}=${provider#*-}" >> "$secfile"
    done
  done
} || :

%if %{with_gcj}
  if [ -x %{_bindir}/rebuild-gcj-db ]; then
    %{_bindir}/rebuild-gcj-db
  fi
%endif
%update_maven_depmap

%postun
if [ $1 -eq 0 ] ; then

  {
    # Rebuild the list of security providers in classpath.security
    suffix=security/classpath.security
    secfiles="/usr/lib/$suffix /usr/lib64/$suffix"

    for secfile in $secfiles
    do
      # check if this classpath.security file exists
      [ -f "$secfile" ] || continue

      sed -i '/^security\.provider\./d' "$secfile"

      count=0
      for provider in $(ls /etc/java/security/security.d)
      do
        count=$((count + 1))
        echo "security.provider.${count}=${provider#*-}" >> "$secfile"
      done
    done
  } || :

  %if %{with_gcj}
    if [ -x %{_bindir}/rebuild-gcj-db ]; then
      %{_bindir}/rebuild-gcj-db
    fi
  %endif

fi
%update_maven_depmap

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc *.html
%{_javadir}/bcprov.jar
%{_javadir}/bcprov-%{version}.jar
  %{_javadir}/gcj-endorsed/bcprov-%{version}.jar
%if %{with_gcj}
  %{_libdir}/gcj/%{name}/
%endif
%{_sysconfdir}/java/security/security.d/2000-%{classname}
%{_mavenpomdir}/JPP-bcprov.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}/

%changelog
* Thu Feb 11 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.45-1
- Import Bouncy Castle 1.45.

* Sat Nov 14 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.44-1
- Import Bouncy Castle 1.44.

* Sun Sep  6 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.43-6
- Include improvements from #521475:
- Include missing properties files in jar.
- Build with javac -encoding UTF-8.
- Use %%javac and %%jar macros.
- Run test suite during build (ignoring failures for now).
- Follow upstream in excluding various test suite classes from jar; drop
  dependency on junit4.

* Wed Aug 26 2009 Andrew Overholt <overholt@redhat.com> 1.43-5
- Add maven POM

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-3
- Raise java requirement to >= 1.7 once again.

* Fri Jul 10 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-2
- Re-enable AOT bits thanks to Andrew Haley.

* Mon Apr 20 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-1
- Import Bouncy Castle 1.43.

* Sat Apr 18 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-3
- Don't build AOT bits. The package needs java1.6

* Thu Apr 09 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-2
- Add missing Requires: junit4

* Tue Mar 17 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-1
- Import Bouncy Castle 1.42.
- Update description.
- Add javadoc subpackage.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 11 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.41-2
- Fixed license tag (BSD -> MIT).
- Minor improvements in the SPEC file for better compatibility with the 
  Fedora Java Packaging Guidelines.
- Added "Provides: bcprov == %%{version}-%%{release}".

* Thu Oct  2 2008 Lillian Angel <langel@redhat.com> - 1.41-1
- Import Bouncy Castle 1.41.
- Resolves: rhbz#465203

* Thu May 15 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.39-1
- Import Bouncy Castle 1.39.
- Set target to 1.5.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.38-2
- Autorebuild for GCC 4.3

* Thu Nov 29 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.38-1
- Import Bouncy Castle 1.38.
- Require junit4 for build.
- Require java-1.7.0-icedtea-devel for build.
- Wrap lines at 80 columns.
- Inline rebuild-security-providers in post and postun sections.
- Related: rhbz#260161

* Sat Mar 31 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.34-3
- Require java-1.5.0-gcj.

* Tue Dec 12 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.34-2
- Install bcprov jar and unversioned symlink in %%{_javadir}.
- Install bcprov symlink in %%{_javadir}/gcj-endorsed.
- Change release numbering format to X.fc7.
- Include new bcprov files in files list.
- Import Bouncy Castle 1.34.
- Related: rhbz#218794

* Tue Jul 25 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.33-3
- Bump release number.

* Mon Jul 10 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.33-2
- Fix problems pointed out by reviewer.

* Fri Jul  7 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.33-1
- First release.
