Name:           lbcd
Version:        3.3.0
Release:        3%{?dist}
Summary:        lbcd - Load balancing client daemon
License:        Other
URL:            http://www.eyrie.org/~eagle/software/lbcd/lbcd.html
Source0:        lbcd-3.3.0.tar.gz
Source1:	lbcd-init-script

#BuildRequires:  
#Requires:       

%description
lbcd runs as a daemon and reports various system utilization information and 
optionally service status information via a UDP network protocol. It is 
designed to run on the client systems of a remote load balancing system, 
such as the DNS-based lbnamed load balancer. 


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_initddir}
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_initddir}/lbcd


%files
%defattr(-,root,root)
%doc README NEWS
%{_sbindir}/lbcd
%{_bindir}/lbcdclient
%{_mandir}/man8/lbcd.8*
%{_mandir}/man1/lbcdclient.1*
%{_initddir}/lbcd




%changelog
* Thu Sep 22 2011 Robert Knight <knight@princeton.edu> 3.3.0-3
- Make init script executable

* Wed Sep 21 2011 Robert Knight <knight@princeton.edu> 3.3.0-2
- Add init script

* Tue Sep 20 2011 Robert Knight <knight@princeton.edu> 3.3.0-1
- Initial version.

