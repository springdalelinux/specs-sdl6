Name:           google-authenticator
Version:        1.0
Release:        0.1%{?dist}
Summary:        One-time passcode support using open standards

License:        ASL 2.0
URL:            http://code.google.com/p/google-authenticator/
Source0:        libpam-google-authenticator-%{version}-source.tar.bz2
Patch1:         0001-Add-no-drop-privs-option-to-manage-secret-files-as-r.patch
Patch2:		0002-Allow-expansion-of-PAM-environment-variables-in-secr-2.patch
BuildRequires:  pam-devel

%description
The Google Authenticator package contains a pluggable authentication
module (PAM) which allows login using one-time passcodes conforming to
the open standards developed by the Initiative for Open Authentication
(OATH) (which is unrelated to OAuth).

Passcode generators are available (separately) for several mobile
platforms.

These implementations support the HMAC-Based One-time Password (HOTP)
algorithm specified in RFC 4226 and the Time-based One-time Password
(TOTP) algorithm currently in draft.

%prep
%setup -q -n libpam-google-authenticator-%{version}
#patch1 -p1
%patch2 -p1

%build
make CFLAGS="${CFLAGS:-%optflags}" LDFLAGS=-ldl %{?_smp_mflags}

%check
./pam_google_authenticator_unittest

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_lib}/security
install -m0755 pam_google_authenticator.so $RPM_BUILD_ROOT/%{_lib}/security/pam_google_authenticator.so
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -m0755 google-authenticator $RPM_BUILD_ROOT/%{_bindir}/google-authenticator

%files
/%{_lib}/security/*
%{_bindir}/google-authenticator
%doc FILEFORMAT README totp.html



%changelog
* Mon Oct 03 2011 David Woodhouse <David.Woodhouse@intel.com> - 0-0.3.20110830.hgd525a9bab875
- Remove qrencode-devel from BR; it doesn't exist on RHEL6

* Mon Sep 12 2011 David Woodhouse <David.Woodhouse@intel.com> - 0-0.2.20110830.hgd525a9bab875
- Add support for expanding PAM environment variables in secret key file name:
  http://code.google.com/p/google-authenticator/issues/detail?id=108

* Mon Sep 12 2011 David Woodhouse <David.Woodhouse@intel.com> - 0-0.1.20110830.hgd525a9bab875
- Initial import

