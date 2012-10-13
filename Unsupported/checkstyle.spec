Name:           checkstyle
Version:        5.5
Release:        4.1%{?dist}
Summary:        Check programmers styling

License:        GPL
URL:            http://checkstyle.sourceforge.net/
Source0:        %{name}-%{version}-bin.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:  coreutils
Requires:       java

%description
Check if the programmer used good style practices

%prep
%setup -q


%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT/usr/bin
%{__mkdir_p} $RPM_BUILD_ROOT/usr/share/java/%{name}-%{version}
%{__cp} -r * $RPM_BUILD_ROOT/usr/share/java/%{name}-%{version}

cat << EOF > $RPM_BUILD_ROOT/usr/bin/checkstyle
#!/bin/bash

JAVA="java -client -Xms5m -Xmx5m"
JAR="/usr/share/java/%{name}-%{version}/%{name}-%{version}-all.jar"

if [ "\${CHECKSTYLEXML}" == "" ]; then
        echo "WARNING: No CHECKSTYLEXML environment variable set, using default rules.";
        CHECKSTYLEXML="/usr/share/java/%{name}-%{version}/contrib/examples/checks/all-checkstyle-checks.xml"
fi

\${JAVA} -jar \${JAR} -c \${CHECKSTYLEXML} \${@}
EOF

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/usr/share/java/%{name}-%{version}
%attr(0755,root,root) /usr/bin/checkstyle
%doc



%changelog
* Sat Apr 28 2012 Josko Plazonic <plazonic@math.princeton.edu>
- convert to noarch and require java

* Fri Mar 30 2012 Benjamin Rose <benrose@cs.princeton.edu>
- Initial release
