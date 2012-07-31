# Prevent stripping
%define __spec_install_post /usr/lib/rpm/brp-compress
# Turn off debuginfo package
%define debug_package %{nil}

Summary: Helper for flash plugin to install automatically on 64 bit
Name: flash-plugin64
Version: 10.1
Release: 2%{dist}
License: GPL
ExclusiveArch: x86_64
Group: Applications/Internet
Requires: flash-plugin(x86-32) nspluginwrapper(x86-32) nspluginwrapper(x86-64)

%description
Helper for Adobe Flash Plugin %{version} 32 bit to trigger nspluginwrapper
automatically on installs and updates of flash-plugin.

%prep

%build

%install

%triggerin -- firefox, mozilla, opera, seamonkey, flash-plugin, google-chrome-beta, google-chrome-stable, google-chrome-unstable
/usr/bin/mozilla-plugin-config >/dev/null 2>&1 || :
if [ -e /usr/lib64/mozilla/plugins-wrapped/nswrapper_32_64.libflashplayer.so -a -d /opt/google/chrome -a -O /opt/google/chrome -a ! -e /opt/google/chrome/plugins/nswrapper_32_64.libflashplayer.so ]; then
	test -d /opt/google/chrome/plugins || rm -rf /opt/google/chrome/plugins && install -d 755 /opt/google/chrome/plugins
	test -d /opt/google/chrome/plugins && ln -s /usr/lib64/mozilla/plugins-wrapped/nswrapper_32_64.libflashplayer.so /opt/google/chrome/plugins
fi

%files

%changelog
* Fri Jul 09 2010 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
