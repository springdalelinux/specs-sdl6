Name:			fish
Version:	1.23.1
Release:	1%{?dist}
Summary:	Fish shell

Group:		System Environment/Shells
License:	GPL
URL:		  http://ridiculousfish.com/shell
Source0:	fishfish.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	ncurses-devel autoconf gettext
Requires:	ncurses

%description

a shell

%prep
%setup -q -n fishfish


%build
%{__autoconf} configure.ac >configure
chmod 755 configure
%configure
make


%install
rm -rf %{buildroot}
%makeinstall


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc
%{_sysconfdir}/fish/config.fish
%{_bindir}/fish*
%{_bindir}/mimedb
%{_bindir}/set_color
%{_datadir}/fish
%{_datadir}/locale/*/*/fish.mo
%{_mandir}/man1/xsel.1x.gz




%changelog
* Thu Jun 7 2012 Thomas Uphill <uphill@ias.edu>
- initial build
