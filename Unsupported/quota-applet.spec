Summary: Quota Notification Applet
Name: quota-applet
Version: 0.1
Release: 1%{dist}
License: GNU
Group: Applications/System
Source: %{name}-%{version}.tar.bz2
BuildRoot: /tmp/%{name}-%{version}-%{release}-root
Requires: python-quota
Requires: pygtk2

%description
Displays a quota status icon on the notification area.  Warns user is over quota

%prep
%setup 

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart
cp quota-applet.py $RPM_BUILD_ROOT/%{_libexecdir}
cp quota_applet_images.py $RPM_BUILD_ROOT/%{_libexecdir}
cp quota-applet.desktop $RPM_BUILD_ROOT/%{_sysconfdir}/xdg/autostart

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README TODO
%{_sysconfdir}/xdg/autostart/quota-applet.desktop
%{_libexecdir}/quota-applet.py*
%{_libexecdir}/quota_applet_images.py*

%changelog
* Mon Apr 11 2011 Thomas Uphill <uphill@ias.edu> - 0.1-1
- initial release
