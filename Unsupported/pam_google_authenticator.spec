Name: pam_google_authenticator
Summary: Google Authenticator PAM Module
Version: 0.1
Release: 4%{?dist}
License: Apache License
Source: %{name}-%{version}.tar.bz2
Source1: README.pam
Patch1: pam_google_authenticator-puias.patch
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://code.google.com/p/google-authenticator/
BuildRequires: pam-devel
BuildRequires: qrencode-devel
Requires: qrencode

%description
Example PAM module demonstrating two-factor authentication.

%prep
%setup -n %{name}
%patch1 -p1 -b .puias
cp %{SOURCE1} .

%build
LDFLAGS="-ldl" make all

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_lib}/security $RPM_BUILD_ROOT/%{_bindir}
install -m 0750 pam_google_authenticator.so $RPM_BUILD_ROOT/%{_lib}/security/
install -m 0755 google-authenticator $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 demo $RPM_BUILD_ROOT%{_bindir}/google-authenticator-demo

%clean
rm -rf %{buildroot}

%check
make test

%files
%defattr(-,root,root,-)
%doc FILEFORMAT README* totp.html
%dir %attr(0750,root,root) /%{_lib}/security/pam_google_authenticator.so
%dir %attr(0755,root,root) %{_bindir}/google-authenticator*

%changelog
* Tue Mar 22 2011 Josko Plazonic <plazonic@math.princeton.edu>
- update README.pam file with an easy selinux workaround
- Initial build 
