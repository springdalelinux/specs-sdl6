Name:	 kile
Summary: (La)TeX source editor and TeX shell
Version: 2.1
Release: 1%{?dist}

License: GPLv2+
Group: 	 Applications/Publishing
URL:	 http://kile.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/kile/kile-%{version}%{?pre}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: kdelibs4-devel

%if 0%{?fedora} > 8 || 0%{?rhel} > 5
Requires: tex(latex)
%else
Requires: tetex-latex
%endif

## Optional/recommended, but not absolutely required.
#Requires: dvipdfmx
# okular
#Requires: kdegraphics

%{?_kde4_version:Requires: kdelibs4%{?_isa} >= %{_kde4_version}}

%description
Kile is a user friendly (La)TeX editor.  The main features are:
  * Compile, convert and view your document with one click.
  * Auto-completion of (La)TeX commands
  * Templates and wizards makes starting a new document very little work.
  * Easy insertion of many standard tags and symbols and the option to define
    (an arbitrary number of) user defined tags.
  * Inverse and forward search: click in the DVI viewer and jump to the
    corresponding LaTeX line in the editor, or jump from the editor to the
    corresponding page in the viewer.
  * Finding chapter or sections is very easy, Kile constructs a list of all
    the chapter etc. in your document. You can use the list to jump to the
    corresponding section.
  * Collect documents that belong together into a project.
  * Easy insertion of citations and references when using projects.
  * Advanced editing commands.


%prep
%setup -q -n %{name}-%{version}%{?pre}


%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --with-kde

## unpackaged files
rm -rfv %{buildroot}%{_kde4_docdir}/kile


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/kde4/kile.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
update-mime-database %{_datadir}/mime &> /dev/null || :
if [ $1 -eq 0 ] ; then
  update-desktop-database -q &> /dev/null
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
update-desktop-database -q &> /dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%doc kile-remote-control.txt
%{_kde4_bindir}/kile
%{_kde4_appsdir}/kile/
%{_kde4_appsdir}/kconf_update/*
%{_kde4_datadir}/applications/kde4/kile.desktop
%{_kde4_datadir}/config.kcfg/kile.kcfg
%{_datadir}/dbus-1/interfaces/net.sourceforge.kile.main.xml
%{_kde4_iconsdir}/hicolor/*/*/*
%{_datadir}/mime/packages/kile.xml


%clean
rm -rf %{buildroot}


%changelog
* Mon Jun 13 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.1-1
- update to 2.1 final, finally includes translations (drop extra tarball)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-0.11.b5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.1-0.10.b5
- update to 2.1b5 and matching translations (revision 1211084 from 2011-01-03)
- drop docbook version hack and completion-kde46 patch, fixed upstream

* Tue Dec 07 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.1-0.9.b4
- backport upstream patch to make completion work with kdelibs 4.6
- update docbook version to make doc-translations build with kdelibs 4.6

* Sat Apr 17 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.1-0.8.b4
- update translations

* Mon Apr 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.1-0.7.b4
- kile-2.1b4

* Tue Feb 02 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.1-0.6.b3
- force termination when the main window is closed (#557436, kde#220343)

* Sun Dec 20 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.1-0.5.b3
- add translations from l10n-kde4 SVN (revision 1055480 from Nov 28)

* Mon Nov 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.1-0.4.b3
- kile-2.1b3

* Sun Aug 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.1-0.3.b2
- kile-2.1b2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-0.2.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.1-0.1.b1
- kile-2.1b1, kde4 version, woo!

* Mon Mar 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.0.3-3
- optimize scriptlets

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.0.3-1
- update to 2.0.3 (#476108)

* Sun Sep 28 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.0.2-1
- update to 2.0.2 (#464320)

* Sun Jun 22 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.0.1-2
- also change QuickPreview to use xdg-open (#445934 reloaded)

* Sun May 11 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.1-1
- kile-2.0.1 (#445975)
- kile should require: kdebase3 (#445933)
- kpdf preview is broken (#445934)
- drop deprecated kile-i18n references

* Fri Feb 15 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0-4
- respin (new tarball)
- f9+: Requires: tex(latex)

* Sat Feb 09 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.0-3
- rebuild for GCC 4.3

* Thu Jan 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.0-2
- BR kdelibs3-devel (F7+, EL6+)

* Mon Nov 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0-1
- kile-2.0

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.3-6
- patch kile.desktop to satisfy desktop-file-validate

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.3-5
- respin (BuildID)
- BR: desktop-file-utils (again)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.9.3-3
- License: GPLv2+

* Tue Nov 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.3-2
- drop desktop-file-utils usage

* Sat Nov 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.3-1
- kile-1.9.3, CVE-2006-6085 (#217238)

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.2-4
- revert to saner/simpler symlink handling

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.2-3
- fc6 respin

* Sun Aug 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.2-1
- kile-1.9.2

* Sat Jun 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9.1-1
- kile-1.9.1

* Mon May 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9-2
- safer abs->rel symlink conversion 

* Fri Mar 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9-1
- 1.9(final)

* Mon Mar 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.9-0.1.rc
- 1.9rc1

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Thu Nov 10 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.3-7
- fix symlinks
- simplify configure

* Fri Oct 22 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.3-5
- %%description: < 80 columns
- %%post/%%postun: update-desktop-database
- touchup %%post/%%postun icon handling to match icon spec
- absolute->relative symlinks
- remove Req: qt/kdelibs crud

* Tue Oct 11 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.3-4
- use gtk-update-icon-cache (#170291)

* Thu Aug 18 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.8.1-3
- fix broken Obsoletes (#166300)

* Thu Jun 02 2005 Rex Dieter 1.8.1-1
- 1.8.1
- x86_64 fix (bug #161343)

* Tue May 31 2005 Rex Dieter 1.8-2
- Obsoletes: kile-i18n

* Mon May 23 2005 Rex Dieter 1.8-1
- 1.8 

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.7.1
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Jan 12 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:1.7.1-3
- fix (katepart) conflicts with kde >= 3.2
- update %%description

* Mon Oct 18 2004 Rex Dieter <rexdieter at sf.net> 0:1.7.1-0.fdr.2
- -katepart: fix conflicts with kde >= 3.3 (optional)

* Mon Oct 18 2004 Rex Dieter <rexdieter at sf.net> 0:1.7.1-0.fdr.1
- 1.7.1

* Tue Sep 28 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.3-0.fdr.2
- respin (against kde-3.3)

* Fri May 14 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.3-0.fdr.1
- 1.6.3

* Sun Mar 28 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.2-0.fdr.2
- BuildRequires: gettext

* Mon Mar 22 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.2-0.fdr.1
- 1.6.2

* Wed Mar 17 2004 Rex Dieter <rexdietet at sf.net> 0:1.6.1-0.fdr.7
- fix detection/usage of desktop-file-install

* Thu Mar 16 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.6
- properly fix desktop file.
- BuildRequires: fam-devel for lame/broken (err, fc2) kde builds.

* Thu Mar 11 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.5
- dynamically determine versions for qt and kdelibs dependancies.

* Wed Mar 10 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.4
- loosen Requires a bit

* Tue Mar 09 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.3
- --disable-rpath

* Tue Mar 09 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.2
- respin for kde-3.2.1

* Wed Feb 11 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.1
- Allow for building on/for both kde-3.1/kde-3.2

* Sun Feb 01 2004 Rex Dieter <rexdieter at sf.net> 0:1.6.1-0.fdr.0
- 1.6.1

* Mon Dec 01 2003 Rex Dieter <rexdieter at sf.net> 0:1.6-0.fdr.5
- add BuildRequires to satisfy fedora's build system.

* Wed Nov 26 2003 Rex Dieter <rexdieter at sf.net> 0:1.6-0.fdr.4
- removed Utility;TextEditor desktop Categories.

* Wed Nov 26 2003 Rex Dieter <rexdieter at sf.net> 0:1.6-0.fdr.3
- Requires: tetex-latex
- configure --disable-rpath
- remove Obsoletes: ktexmaker2

* Mon Nov 24 2003 Rex Dieter <rexdieter at sf.net> 0:1.6-0.fdr.2
- fixup file lists
- update macros for Fedora Core support

* Sat Nov 01 2003 Rex Dieter <rexdieter at sf.net> 0:1.6-0.fdr.1
- 1.6

* Wed Sep 17 2003 Rex Dieter <rexdieter at sf.net> 0:1.5.2-0.fdr.4
- fix missing latexhelp.html

* Thu Sep 11 2003 Rex Dieter <rexdieter at sf.net> 0:1.5.2-0.fdr.3
- patch1 

* Wed Aug 20 2003 Rex Dieter <rexdieter at sf.net> 0:1.5.2-0.fdr.2
- 1.5.2

* Fri May 30 2003 Rex Dieter <rexdieter at sf.net> 0:1.5-0.fdr.2
- re-add %%find_lang and %%doc files not present in 1.5.2a

* Thu May 29 2003 Rex Dieter <rexdieter at sf.net> 0:1.5-0.fdr.1
- resync with unstable branch.

* Fri May 16 2003 Rex Dieter <rexdieter at sf.net> 0:1.5-0.fdr.0
- bite bullet now, revert back to 1.5.
- fedora versioning.

* Fri Apr 25 2003 Rex Dieter <rexdieter at sf.net> 1.50-0.0
- 1.5 release, artificially use 1.50 so rpm thinks it is > 1.32.

* Fri Apr 25 2003 Rex Dieter <rexdieter at sf.net> 1.40-1.3
- remove %%doc NEWS

* Mon Mar 03 2003 Rex Dieter <rexdieter at sf.net> 1.40-1.2 
- version: 1.4 -> 1.40 so silly rpm knows that 1.40 is newer than 1.32
- use epochs in Obsoletes/Provides/Requires.

* Fri Feb 21 2003 Rex Dieter <rexdieter at sf.net> 1.4-1.1
- yank kmenu

* Tue Feb 18 2003 Rex Dieter <rexdieter at sf.net> 1.4-1.0
- 1.40
- use desktop-create-kmenu

* Fri Feb 07 2003 Rex Dieter <rexdieter at sf.net> 1.32-0.0
- 1.32
- kde-redhat versioning

* Tue Jan 14 2003 Rex Dieter <rdieter@unl.edu> 1.31-0
- 1.31
- update Url, Vendor
- specfile cleanup

* Fri Oct 25 2002 Rex Dieter <rdieter@unl.edu> 1.3-1
- 1.3 (final).

* Wed Oct 23 2002 Rex Dieter <rdieter@unl.edu> 1.3-0.beta.1
- 1.3beta.

* Mon Sep 09 2002 Rex Dieter <rdieter@unl.edu> 1.2-0
- 1.2

* Wed Aug 21 2002 Rex Dieter <rdieter@unl.edu> 1.1-1.1
- workaround automake bug.

* Wed Aug 14 2002 Rex Dieter <rdieter@unl.edu> 1.1-1.0
- rebuild on/for kde 3.0.3

* Fri Aug 09 2002 Rex Dieter <rdieter@unl.edu> 1.1-0.0
- first shot at 1.1

* Mon Jul 08 2002 Rex Dieter <rdieter@unl.edu. 1.0-2
- rebuild for kde 3.0.2

* Sun Jun 16 2002 Rex Dieter <rdieter@unl.edu> 1.0-1
- 1.0
