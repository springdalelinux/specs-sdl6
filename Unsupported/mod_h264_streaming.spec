Name:           mod_h264_streaming
Version:        2.2.7
Release:        0.2%{?dist}
Summary:        H264 Streaming Module plugin for Apache/Lighttpd/Nginx webserver.

Group:          System Environment/Daemons
License:        Free for non commercial user
URL:            http://h264.code-shop.com/trac/wiki
Source0:        http://h264.code-shop.com/download/apache_mod_h264_streaming-2.2.7.tar.gz

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  httpd-devel

Requires:       httpd

%description
H264 Streaming Module plugin for Apache/Lighttpd/Nginx webserver.

%prep
%setup -q

%build
%configure --with-apxs=%{_sbindir}/apxs
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d
cat > %{buildroot}%{_sysconfdir}/httpd/conf.d/h264_streaming.conf <<ENDCONF
LoadModule h264_streaming_module modules/mod_h264_streaming.so
AddHandler h264-streaming.extensions .mp4
ENDCONF


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%changelog
* Tue May 23 2012 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
