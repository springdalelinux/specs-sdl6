Summary: A PAM module that allows users to authenticate on htpasswd-type files separate from /etc/passwd.
Name: pam_pwdfile
Version: 0.99
Release: 1%{?dist}
License: LGPL
Group: System Environment/Base
Source0: %{name}-%{version}.tar.gz
URL: http://cpbotha.net/pam_pwdfile.html
BuildRequires: pam-devel
Requires: pam

%description
This pam module can be used for the authentication service only, in cases
where one wants to use a different set of passwords than those in the main
system password database. 

%prep
%setup
mv contrib/Makefile.standalone Makefile

%build
make CFLAGS="%{optflags} -c -fPIC" LD=gcc LDFLAGS="-shared"

%install
make PAM_LIB_DIR="$RPM_BUILD_ROOT/%{_lib}/security" install

%files
%defattr(-,root,root)
%doc README changelog
%attr(0755, root, root) /%{_lib}/security/pam_pwdfile.so
