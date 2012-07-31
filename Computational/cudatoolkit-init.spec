Name:		cudatoolkit-init
Version:	1.0
%define destdir /usr/local/cudatoolkit/%{version}
%define cudamajor %(echo %{version} | cut -d. -f1,2 | )
Release:	1%{?dist}
Summary:	NVIDIA's CUDA Toolkit initscript
Group:		Development/Libraries
License:	Other
Source1:	nvidiacuda
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

%description
NVIDIA's CUDA Toolkit init scripts

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_initddir}
install -D -p -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_initddir}/nvidiacuda

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add nvidiacuda || :

%files
%defattr(-,root,root,-)
%{_initddir}/nvidiacuda

%changelog
* Mon Mar 12 2012 Josko Plazonic <plazonic@math.princeton.edu>
- initial build, partially from NVIDIA pdf
