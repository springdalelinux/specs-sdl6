Name:           findbugs
Version:        2.0.0
Release:        1.1%{?dist}
Summary:        Find bugs in java classfiles

License:        GPL
URL:            http://findbugs.sourceforge.net/
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:  coreutils
Requires:       java

%description
Find bugs in Java code

%prep
%setup -q


%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT/usr/share/java/%{name}-%{version}
%{__mkdir_p} $RPM_BUILD_ROOT/usr/bin
%{__cp} -r * $RPM_BUILD_ROOT/usr/share/java/%{name}-%{version}
%{__ln_s} /usr/share/java/%{name}-%{version}/bin/findbugs $RPM_BUILD_ROOT/usr/bin/findbugs


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/usr/share/java/%{name}-%{version}
/usr/bin/findbugs


%changelog
* Fri Mar 30 2012 Benjamin Rose <benrose@cs.princeton.edu>
- Initial release
