%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Net_IPv4

Name:           php-pear-Net-IPv4
Version:        1.3.4
Release:        1%{?dist}
Summary:        IPv4 network calculations and validation

Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/%{pear_name}
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
Source2:        xml2changelog
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       /bin/ping

%description
Class used for calculating IPv4 (AF_INET family) address information
such as network as network address, broadcast address, and IP address

%prep
%setup -q -c
# package.xml is V2
%{_bindir}/php -n %{SOURCE2} package.xml >CHANGELOG
mv package.xml %{pear_name}-%{version}/%{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT docdir
cd %{pear_name}-%{version}
%{__pear} -d download_dir=$PWD install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc CHANGELOG
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Net
%{pear_phpdir}/test/%{pear_name}

%changelog
* Mon Jan 03 2010 Josko Plazonic <plazonic@math.princeton.edu>
- initial build from Net_Ping src.rpm
