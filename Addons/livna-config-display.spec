%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:        livna-config-display
Version:     0.0.24
Release:     1%{?dist}
Summary:     Tools to manage graphic drivers from the Livna repository

URL:         http://rpm.livna.org
License:     GPLv2+
Group:       System Environment/Base
Source0:     http://downloads.diffingo.com/livna/livna-config-display/%{name}-%{version}.tar.gz

Requires:    pygtk2, pygtk2-libglade
Requires:    usermode
Requires:    pyxf86config >= 0.3.16

BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:         noarch
BuildRequires:     desktop-file-utils
BuildRequires:     gettext

%description
%{name} is a graphical and command-line tool to manage the various
display drivers offered at the Livna repository. It configures the
GDM and KDM display managers, as well as the X server configuration.

%prep

%setup -q
#pushd src/livnaConfigDisplay
#patch0 -b .patch0
#popd

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

desktop-file-install --vendor livna\
 --dir ${RPM_BUILD_ROOT}%{_datadir}/applications\
       ${RPM_BUILD_ROOT}%{_datadir}/applications/livna-config-display.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_datadir}/livna-config-display
%dir %{python_sitelib}/livnaConfigDisplay
%{_bindir}/livna-config-display
%{_sbindir}/livna-config-display
%{_datadir}/%{name}/*
%{_datadir}/applications/*.desktop
%{python_sitelib}/livnaConfigDisplay/*

%config(noreplace) %{_sysconfdir}/security/console.apps/livna-config-display
%config(noreplace) %{_sysconfdir}/pam.d/livna-config-display
%ghost %{_sysconfdir}/sysconfig/livna-config-display
%doc TODO CHANGELOG COPYING

%changelog
* Mon Aug 30 2010 Stewart Adam <s.adam at diffingo.com> - 0.0.24-1
- Update to 0.0.24
- Remove dependency on system-config-display

* Sat Aug 21 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.23-3
- rebuilt

* Wed Aug 11 2010 Stewart Adam <s.adam at diffingo.com> - 0.0.23-2
- Rebuild for Python 2.7

* Sun Apr 19 2009 Stewart Adam <s.adam at diffingo.com> - 0.0.23-1
- Update to 0.0.23

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.22-3
- rebuild for new F11 features

* Thu Dec 11 2008 Stewart Adam <s.adam at diffingo.com> - 0.0.22-2
- Rebuild for python 2.6

* Thu Nov 6 2008 Stewart Adam <s.adam at diffingo.com> - 0.0.22-1
- Update to 0.0.22

* Wed Oct 22 2008 Stewart Adam <s.adam at diffingo.com> - 0.0.21-1
- Update to 0.0.21

* Sun Oct 05 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.0.20-2
- rebuild for rpm fusion

* Sat Dec 8 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.20-1
- Update to 0.0.20
- Drop obsolete duplicate module patch

* Tue Nov 20 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.19-2
- Don't duplicate modules in xorg.conf (bz#1609)

* Thu Nov 1 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.19-1
- Specfile improvements
- Update to 0.0.19

* Tue Oct 23 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.18-1
- Update to 0.0.18

* Sun Oct 14 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.17-2
- redhat-artwork no longer exists! Remove the Requires since it turns out
  we actually don't need it anymore.

* Fri Aug 24 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.17-1
- Update to 0.0.17 (fixes tracebacks on new config)
- Update License tag to GPLv2+... My bad.

* Tue Aug 14 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.16a-1
- Update to 0.0.16a (fixes one-liner that prevented lcd from running)

* Mon Aug 13 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.16-1
- Update to 0.0.16
- Update License tag to GPLv2

* Tue Jul 17 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.15-1
- Update to 0.0.15
- Add Requires system-config-display

* Sun Jul 8 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.14b-1
- Update to 0.0.14b

* Sun Jul 1 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.14a-1
- Update to 0.0.14a

* Sat Jun 30 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.14-1
- Update to 0.0.14

* Thu Jun 21 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.13-1
- Update to 0.0.13

* Mon Jun 4 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.12-1
- Update to 0.0.12
- livna is the .desktop vendor, not fedora

* Tue May 8 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.11-1
- Update to 0.0.11

* Sun May 6 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.10-1
- Update to 0.0.10

* Sun Apr 29 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.9-1
- Update to 0.0.9 (adds new translations)
- Drop Compsite patch

* Sat Mar 10 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.8-2
- Fix compsite in /etc/sysconfig/livna-config-display file

* Sat Mar 10 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.8-1
- Update to 0.0.8

* Sat Mar 10 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.7-2
- Apply button shouldn't be insensitive ALL the time...

* Fri Mar 9 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.7-1
- Change Category in .desktop menu entry so it appears in Administration
- Fix two critical bugs

* Sat Feb 24 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.6-8
- Bump

* Sat Feb 24 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.6-7
- Use %%ghost, add oldDriver when setting up base config

* Thu Feb 22 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.6-6
- Fix error on non-existing STATUS_FILE... Again!

* Thu Feb 22 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.6-5
- Fix error on non-existing STATUS_FILE

* Thu Feb 22 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.6-4
- Fix error on attempting to backup nonexistant files

* Fri Feb 9 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.6-3
- LivnaUtils class if now just plain defs
- A few minor changes
- Specfile cleanups
- Regen .pot file

* Sun Feb 4 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.6-2
- Removed .py(o|c) and .bak files and also wrapped $@ in quotes

* Fri Jan 26 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.6-1
- Re-add support for manual-configuration
- Remove initscript template; Unfeasable
- Support nVidia /ATi source installations, but RPM comes first.
- Add functions to Utils.py
- Merge the many Xgl Gdm|Kdm functions into a simple format: get[Gdm|Kdm]Xgl and set[Gdm|Kdm]Xgl
- Improve client ease-of-use
- Fix a few typo bugs
- Added many docstrings!
- Check if things exist before attempts to modify them
- Disable Xgl when it's not there
- Don't backup files twice.

* Fri Jan 25 2007 Alphonse Van Assche <alcapcom@gmail.com> 0.0.5-1
- Some bug fix in advanced option TUI.
- Add ConfigFile class.
- Check if the driver is enabled in the initscript.
- Add --noauto, --quiet and --noconfig TUI options.
- Add build target to the main Makefile.
- Run ldconfig only on specific directories (for performance)
- Add src/livnaConfigDisplay + *.glade on the po/Makefile.
- Add fr.po file.
- Change the color of the app icon to fit with the livna web site style.
- Compile livnaConfigDisplay package at install time (livnaConfigDispay/Makefile).
- Fix some missing import.
- Add icon on the enable/disable button (commented out for the moment)
- Add --applynow arg on TUI, if user add these argument, We ask him to apply the new settings immediately.
- Remove unneeded file before make the archive (Makefile).
- Backup and restore stuff are better managed in both UI's
- Library can now be used by other apps in a simpler way.
- Xgl stuff is disabled by default, this feature can be enabled in the config file.
- Multiple driver a once stuff is disabled by default, this feature can be enabled in const.py.
- Cleanup i18n strings.
- Introspect and load *ConfigDisplay see ConfigDisplayClient.py at line 119.
- Update spec file.


* Tue Jan 9 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.4-1
- Fix multi-lingual issues
- Correct 'Error applying the configuration' error, yet it infact the configuration was applied...

* Tue Jan 9 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.4-1
- New release

* Thu Jan 4 2007 Stewart Adam <s.adam AT diffingo DOT com> 0.0.3-2
- Clean up according to FE standards and FE spec template
- Change %%description
- Repackage, removing unneeded files
- Fix import LivnaConfigDisplay and import livnaConfigDisplay mismatches 

* Sat Dec 30 2006 Alphonse Van Assche <alcapcom@gmail.com>
- fix verbose mode.
- add some new args to the TUI
  --aiglx-flag     enable or disable Aiglx flag
  --compposite     enable or disable Composite extension
  --xgl-gdm        enable or disable Xgl settings in GDM
  --xgl-gdm-def    add Xgl settings def in GDM for the given vendor
  -d, --disable-glx    disable all X GLX stuff 
- using of getAutoConfig() in the TUI too.
- remove system configuration stuff in enable() and disable() vendor classes.
- fix: check if a Module section exist in xorg.conf before try to remove a loded module (livnaConfigDisplay).
- add restart-xserver.sh script + user can now restart the X server from the GUI with that build-in script.
- add KDM support for Xgl in both UI's.
- fix: setGDMXglServerDef only update the lines that begin with "command=/usr/bin/Xgl" in custom.conf file.

* Wed Dec 27 2006 Alphonse Van Assche <alcapcom@gmail.com>
- add muti driver at once in the GUI (so if the future gives us this possibility, we 
  are ready)
- fix charset bug.
- add auto and manual configuration in the GUI.
- add a DEBUG var in livnaConfigClient, so we can now show all drivers in the 
  GUI combobox when we debug the app.
- the GUI load automatically the best GDM and XORG configuration for the 
  selected driver, through getAutoConfig() def "packager side classes".
  
* Sat Dec 23 2006 Alphonse Van Assche <alcapcom@gmail.com>
- add --tui and --gui
- add driver option for ati ("KernelModuleParm", "locked-userpages=0")
- according with what is saying there: http://fr.opensuse.org/Depannage_Xgl,
   Xgl doesn't work on X300, X600 and X700 without these driver option.
   TODO ask people that have these type of hardware to confirme that.
- add multi driver at once support
- enable args for installed pkgs in TUI.
- show installed pkgs in --help.

* Wed Dec 20 2006 Alphonse Van Assche <alcapcom@gmail.com>
- backup xorg.conf file.
- restore backup in a better way (catch errors and print them on the UIs).
- add the cool _setGDMXglServerDef function, thank's Stewart.
- fix the icon path .py and add the fullpath to the icon in the .desktop.in file.
- add legacy boolean on the disable(self, isLegacy) function, so we can do specific trick 
  when legacy drivers are disabled.

* Thu Dec 19 2006 Alphonse Van Assche <alcapcom@gmail.com> 0.0.1-1
- init package.
