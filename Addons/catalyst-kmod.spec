%define kmod_name catalyst

# Tweak to have debuginfo - part 1/2
%if 0%{?fedora} > 7 || 0%{?rhel} > 4
#define __debug_install_post %{_builddir}/%{?buildsubdir}/find-debuginfo.sh %{_builddir}/%{?buildsubdir} %{nil}
%undefine _missing_build_ids_terminate_build
%endif

Name:        catalyst-kmod
Version:     12.6
Release:     1%{?dist}.2
# Taken over by kmodtool
Summary:     AMD display driver kernel module
Group:       System Environment/Kernel
License:     Redistributable, no modification permitted
URL:         http://ati.amd.com/support/drivers/linux/linux-radeon.html
Source0:     http://downloads.diffingo.com/rpmfusion/kmod-data/catalyst-kmod-data-%{version}.tar.bz2
Source11:    catalyst-kmodtool-excludekernel-filterfile
Patch0:      compat_alloc-Makefile.patch
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# needed for plague to make sure it builds for i686
ExclusiveArch:  i686 x86_64

BuildRequires:  %kernel_module_package_buildreqs
%kernel_module_package -n %{kmod_name}

%description
The catalyst %{version} display driver kernel module.


%prep
%setup -q -c -T -a 0

mkdir fglrxpkg
%ifarch %{ix86}
cp -r fglrx/common/* fglrx/arch/x86/* fglrxpkg/
%endif

%ifarch x86_64
cp -r fglrx/common/* fglrx/arch/x86_64/* fglrxpkg/
%endif

# proper permissions
find fglrxpkg/lib/modules/fglrx/build_mod/ -type f -print0 | xargs -0 chmod 0644

# debuginfo fix
#sed -i -e 's|strip -g|/bin/true|' fglrxpkg/lib/modules/fglrx/build_mod/make.sh

pushd fglrxpkg
%patch0 -p0 -b.compat_alloc
popd

for flavor in %flavors_to_build ; do
    cp -a fglrxpkg/  _kmod_build_${flavor}
done


%build
for flavor in %flavors_to_build ; do
    pushd _kmod_build_${flavor}/lib/modules/fglrx/build_mod/2.6.x
    make CC="gcc" PAGE_ATTR_FIX=0 \
      KVER="%{kernel_version $flavor}" \
      KDIR="%{kernel_source $flavor}"
    popd
done


%install
rm -rf $RPM_BUILD_ROOT
for flavor in %flavors_to_build ; do
    install -D -m 0755 _kmod_build_${flavor}/lib/modules/fglrx/build_mod/2.6.x/fglrx.ko $RPM_BUILD_ROOT/lib/modules/%kverrel${flavor%default}/extra/%{kmod_name}/fglrx.ko
done

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Feb 18 2011 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild for puias use, weak modules

* Sat Feb 12 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.12-1.1
- rebuild for updated kernel

* Sun Dec 26 2010 Stewart Adam <s.adam at diffingo.com> - 10.12-1
- Update to Catalyst 10.12 (internal version 8.80.1)
- Merge changes from F-13 branch

* Fri Dec 17 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.11-1.2
- rebuild for updated kernel

* Tue Dec 07 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.11-1.1
- rebuild for F-14 kernel

* Sat Nov 20 2010 Stewart Adam <s.adam at diffingo.com> - 10.11-1
- Update to Catalyst 10.11 (internal version 8.79.1)

* Mon Oct 25 2010 Stewart Adam <s.adam at diffingo.com> - 10.10-1
- Update to Catalyst 10.10 (internal version 8.78.3)

* Thu Oct 21 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.9-1.2
- rebuild for new kernel

* Sun Sep 19 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.9-1.1
- rebuild for new kernel

* Sat Sep 18 2010 Stewart Adam <s.adam at diffingo.com>	- 10.9-1
- Update to Catalyst 10.9 (internal version 8.77.1)

* Sat Sep 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.8-1.2
- rebuild for new kernel

* Fri Sep 10 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.8-1.1
- rebuild for new kernel

* Mon Aug 30 2010 Stewart Adam <s.adam at diffingo.com> - 10.8-1
- Update to 10.8 (internal version 8.76.2)

* Sat Aug 28 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.7-1.4
- rebuild for new kernel

* Fri Aug 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.7-1.3
- rebuild for new kernel

* Wed Aug 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.7-1.2
- rebuild for new kernel

* Sun Aug 08 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.7-1.1
- rebuild for new kernel

* Wed Jul 28 2010 Stewart Adam <s.adam at diffingo.com> - 10.7-1
- Update to Catalyst 10.7 (internal version 8.75.3)
- Synchronize changes with those in F-12 branch

* Tue Jul 27 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.5-1.4
- rebuild for new kernel

* Wed Jul 07 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.5-1.3
- rebuild for new kernel

* Fri Jun 18 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.5-1.2
- rebuild for new kernel

* Tue Jun 1 2010 Stewart Adam <s.adam at diffingo.com> - 10.5-1.1
- Rebuild with correct sources

* Thu May 27 2010 Stewart Adam <s.adam at diffingo.com> - 10.5-1
- Update to Catalyst 10.5 (internal version 8.73.2)

* Sat May 1 2010 Stewart Adam <s.adam at diffingo.com> - 10.4-1
- Update to Catalyst 10.4 (internal version 8.72.3)

* Thu Feb 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.1-1.3
- rebuild for new kernel

* Mon Feb 08 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.1-1.2
- rebuild for new kernel

* Thu Feb 04 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10.1-1.1
- rebuild for new kernel

* Wed Jan 27 2010 Stewart Adam <s.adam at diffingo.com> - 10.1-1
- Update to Catalyst 10.1 (internal version 8.69)

* Fri Jan 22 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.12-1.1
- rebuild for new kernel

* Mon Dec 28 2009 Stewart Adam <s.adam at diffingo.com> - 9.12-1
- Update to Catalyst 9.12 (internal version 8.68.1)

* Sat Dec 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.10-1.4
- rebuild for new kernel

* Sun Dec 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.10-1.3
- rebuild for new kernel

* Sun Nov 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.10-1.2
- rebuild for new kernels

* Thu Nov 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.10-1.1
- rebuild for new kernels

* Sat Oct 24 2009 Stewart Adam <s.adam at diffingo.com>	- 9.10-1
- Update to Catalyst 9.10 (internal version 8.66.1)

* Tue Oct 20 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.9-1.2
- rebuild for new kernels

* Wed Sep 30 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.9-1.1
- rebuild for new kernels

* Fri Sep 11 2009 Stewart Adam <s.adam at diffingo.com> - 9.9-1
- Update to Catalyst 9.9 (internal version 8.65.4)

* Tue Sep 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.8-1.4
- rebuild for new kernels

* Thu Aug 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.8-1.3
- rebuild for new kernels

* Sun Aug 23 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.8-1.2
- rebuild for new kernels

* Sat Aug 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.8-1.1
- rebuild for new kernels

* Wed Aug 19 2009 Stewart Adam <s.adam at diffingo.com> - 9.8-1
- Update to Catalyst 9.8 (internal version 8.64.3)

* Sat Aug 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.5-1.8
- rebuild for new kernels

* Tue Aug 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.5-1.7
- rebuild for new kernels

* Tue Jul 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.5-1.6
- rebuild for new kernels

* Mon Jun 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.5-1.5
- rebuild for new kernels

* Fri Jun 19 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.5-1.4
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.5-1.3
- rebuild for new kernels

* Sun May 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.5-1.2
- rebuild for new kernels

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.5-1.1
- rebuild for new kernels

* Thu May 21 2009 kwizart < kwizart at gmail.com > - 9.5-1
- Update to 9.5 (internal version 8.612)

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.4-2.2
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.4-2.1
- rebuild for new kernels

* Wed May 6 2009 Stewart Adam <s.adam at diffingo.com> - 9.4-2
- Remove Makefile patch and set KDIR variable instead (thanks to kwizart)

* Sat Apr 18 2009 Stewart Adam <s.adam at diffingo.com> - 9.4-1
- Update to 9.4
- Fork as catalyst-kmod

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.4-0.2.beta.1
- rebuild for new kernels

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 9.4-0.2.beta
- rebuild for new F11 features

* Sat Mar 28 2009 Stewart Adam <s.adam at diffingo.com> - 9.4-0.1.beta
- Update to Catalyst 9.4 (beta)

* Sat Mar 28 2009 Stewart Adam <s.adam at diffingo.com> - 9.3-1
- Update to Catalyst 9.3

* Sat Feb 21 2009 Stewart Adam <s.adam at diffingo.com> - 9.2-2
- Fix flush_tlb_page modprobe errors on x86_64

* Fri Feb 20 2009 Stewart Adam <s.adam at diffingo.com> - 9.2-1
- Update to Catalyst 9.2
- Use Catalyst version for Version tag instead of internal driver version

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.573-1.9.1.2
- rebuild for latest Fedora kernel;

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.573-1.9.1.1
- rebuild for latest Fedora kernel;

* Sat Jan 31 2009 Stewart Adam <s.adam at diffingo.com> - 8.573-1.9.1
- Update to Catalyst 9.1

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.561-2.8.12.6
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.561-2.8.12.5
- rebuild for latest Fedora kernel;

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.561-2.8.12.4
- rebuild for latest Fedora kernel;

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.561-2.8.12.3
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.561-2.8.12.2
- rebuild for latest Fedora kernel;

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.561-2.8.12.1
- rebuild for latest Fedora kernel;

* Tue Dec 16 2008 Stewart Adam <s.adam at diffingo.com> - 8.561-2.8.12
- Don't use /lib/modules/$KVER/build, patch in /usr/src/kernels/$KVER instead 

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.561-1.8.12.1
- rebuild for latest Fedora kernel;

* Wed Dec 10 2008 Stewart Adam <s.adam at diffingo.com> - 8.561-1.8.12
- Update to 8.12
- Remove unneeded makefile patch

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.552-1.8.11.3
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.552-1.8.11.2
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.552-1.8.11.1
- rebuild for latest Fedora kernel;

* Mon Nov 17 2008 Stewart Adam <s.adam at diffingo.com> - 8.552-1.8.11
- Update to 8.11

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.543-0.3.8.11beta.6
- rebuild for latest Fedora kernel;

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.543-0.3.8.11beta.5
- rebuild for latest Fedora kernel;

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.543-0.3.8.11beta.4
- rebuild for latest rawhide kernel;

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.543-0.3.8.11beta.3
- rebuild for latest rawhide kernel

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8.543-0.3.8.11beta.2
- rebuild for latest rawhide kernel

* Fri Oct 17 2008 Stewart Adam <s.adam at diffingo.com> - 8.543-0.3.8.11beta.2
- Add the missing "popd"

* Fri Oct 17 2008 kwizart < kwizart at gmail.com > - 8.543-0.3.8.11beta.1
- Drop the make.sh layer

* Thu Oct 16 2008 Stewart Adam <s.adam at diffingo.com> - 8.543-0.2.8.11beta.1
- Update patches

* Thu Oct 16 2008 Stewart Adam <s.adam at diffingo.com> - 8.543-0.1.8.11beta.1
- Update to 8.53.4 (Catalyst 8.11beta)

* Thu Oct 16 2008 Stewart Adam <s.adam at diffingo.com> - 8.542-1.8.10.1
- Update to 8.10

* Sat Sep 21 2008 Stewart Adam <s.adam at diffingo.com> - 8.532-1.8.09
- Update to 8.09

* Thu Aug 21 2008 Stewart Adam <s.adam at diffingo.com> - 8.522-1.8.08
- Update to 8.08

* Thu Jul 24 2008 Stewart Adam <s.adam at diffingo.com> - 8.512-1.8.07
- Update to 8.07

* Wed Jun 18 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.501-1.8.06
- Update to 8.06

* Thu May 22 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.493-1.8.05
- Update to 8.05
- Remove obsolete 2.6.25 capt patch
- Update debuginfo fix

* Fri Apr 18 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.476-1.8.04
- Update to 8.04
- Add capt patch to fix compiling against 2.6.25 kernels
- Fix license tag

* Wed Mar 5 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.471-1.8.03
- Update to 8.03

* Wed Feb 13 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.455.2-1.8.02
- Update to 8.02

* Sat Jan 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.452.1-3.8.01
- rebuild for new kmodtools, akmod adjustments

* Sun Jan 20 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.452.1-2.8.01
- build akmods package

* Sat Jan 19 2008 Stewart Adam <s.adam[AT]diffingo[DOT]com> - 8.452.1-1.8.01
- Update to Catalyst 8.01
- Fix License tag according to rpmlint

* Sat Dec 22 2007 Stewart Adam <s.adam[AT]diffingo[DOT]com> - 8.443.1-1.7.12
- Update to Catalyst 7.12
- Drop obsolete suspend patch

* Sat Dec 8 2007 Stewart Adam <s.adam[AT]diffingo[DOT]com> - 8.43-3.7.11
- Rebuild for latest kernels

* Wed Nov 21 2007 Stewart Adam <s.adam[AT]diffingo[DOT]com> - 8.43-2.7.11
- Fix stupid mistake in patch version

* Wed Nov 21 2007 Stewart Adam <s.adam[AT]diffingo[DOT]com> - 8.43-1.7.11
- Update to Catalyst 7.11

* Sat Nov 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.42.3-8
- rebuilt for 2.6.23.1-49.fc8

* Mon Nov 05 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.42.3-7
- rebuilt for F8 kernels

* Wed Oct 31 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.42.3-6
- rebuilt for latest kernels

* Tue Oct 30 2007 Stewart Adam <s.adam[AT]diffingo[DOT]com> - 8.42.3-5
- Add suspend patch (fixes bz#1691)

* Tue Oct 30 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.42.3-4
- rebuilt for latest kernels

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.42.3-3
- rebuilt for latest kernels
- adjust to rpmfusion and new kmodtool

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.42.3-2
- rebuilt for latest kernels

* Tue Oct 23 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.42.3-1
- Update to 8.42.3
- Update 2.6.23 patch

* Tue Oct 23 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.40.4-13
- rebuilt for latest kernels

* Mon Oct 22 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.40.4-12
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.40.4-11
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.40.4-10
- rebuilt for latest kernels

* Fri Oct 12 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.40.4-9
- rebuilt for latest kernels

* Thu Oct 11 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.40.4-8
- rebuilt for latest kernels

* Wed Oct 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 8.40.4-7
- rebuilt for latest kernels

* Tue Oct 09 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 8.40.4-6
- rebuilt for latest kernels

* Sun Oct 7 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.40.4-5
- update for new kmod-helper stuff
- build for newest kernels

* Sun Oct 7 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.40.4-4
- 2.6.23 patch

* Sun Sep 09 2007 Thorsten Leemhuis < fedora AT leemhuis DOT info > - 8.40.4-3
- Convert to new kmods stuff from livna
- Rebuild for F8T2 and rawhide

* Sun Aug 19 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.40.4-2
- Don't use testing kernel

* Thu Aug 16 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.40.4-1
- Update to 8.40.4

* Sun Jul 23 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.39.4-2
- Update ATI's fixed 8.39.4

* Thu Jul 19 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.39.4-1
- Update to 8.39.4

* Sun Jul 1 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.38.7-2
- Bump

* Sat Jun 30 2007 Niko Mirthes <nmirthes AT gmail DOT com> - 8.38.7-1
- Update to 8.38.7

* Tue Jun 26 2007 Niko Mirthes <nmirthes AT gmail DOT com> - 8.38.6-1
- corrected version update in changelog
- removed sed edit for past releases on 2.6.2x.x kernel

* Mon Jun 25 2007 Niko Mirthes <nmirthes AT gmail DOT com> - 8.38.6-1
- Update to 8.38.6
- removed agpgart patch. agpgart_be.c no longer exists

* Sun Jun 03 2007 Niko Mirthes <nmirthes AT gmail DOT com> - 8.37.6-2
- Updated URL field to current address.

* Thu May 31 2007 Stewart Adam < s.adam AT diffingo DOT com> - 8.37.6-1
- Update to 8.37.6

* Fri Apr 27 2007 Stewart Adam < s.adam AT diffingo DOT com> - 8.36.5-3
- Rebuild for F7T4

* Wed Apr 19 2007 Stewart Adam < s.adam AT diffingo DOT com> - 8.36.5-2
- Just because it builds without the patches doesn't mean the patches are useless...

* Wed Apr 18 2007 Stewart Adam < s.adam AT diffingo DOT com> - 8.36.5-1
- Update to new 8.36.5 release
- Remove old patches

* Tue Apr 17 2007 Stewart Adam < s.adam AT diffingo DOT com> - 8.35.5-2
- Testing deemed this safe and working, so bump for official build
- Do a little spec cleanup

* Fri Mar 30 2007 Stewart Adam < s.adam AT diffingo DOT com> - 8.35.5-1
- Update to 8.35.5
- Copy 'official' 2.6.20 patch from fglrxpkg
- Remove old patches

* Mon Mar 26 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-6
- Ville Skyttä's patch for debuginfo packages (#1459)

* Sun Mar 4 2007 Stewart Adam < s.adam AT diffingo DOT com> - 8.34.8-5
- kdump for non-i686...
- Fix changelog date

* Sat Mar 3 2007 Stewart Adam < s.adam AT diffingo DOT com> - 8.34.8-4
- No kdump
- New kernel

* Fri Mar 2 2007 Stewart Adam < s.adam AT diffingo DOT com> - 8.34.8-3
- New kernel
- Make Source0 a URL

* Sat Feb 24 2007 Stewart Adam < s.adam AT diffingo DOT com> - 8.34.8-2
- Standardize all summaries and descriptions with other nvidia and fglrx
  packages
- Kernel bump

* Sun Feb 21 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-1
- Update to 8.34.8
- Move paths and names to plain fglrx, not ati-fglrx, the driver's name's
  long changed!
- Product support in %%description...
- Conditional patch for 2.6.20

* Sat Feb 17 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.33.6-2
- Change descriptions to more informative, easy-to-understand ones

* Fri Jan 12 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.33.6-1
- Update to 8.33.6

* Fri Nov 17 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.31.5-1
- Update to 8.31.5, patch from Edgan in #livna

* Sat Oct 14 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.29.6-1
- Update to 8.29.6 (needed for 2.6.18 suppport/FC6)

* Fri Aug 18 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.28.8-1
- Update to 8.28.8
- refactored %%prep now that ATi's installer has merged arches

* Thu Aug 10 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-3
- update for kernel 2.6.17-1.2174_FC5

* Sat Aug 05 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-2
- no i586 on fc5

* Sun Jul 30 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-1
- Update to 8.27.10
- removal of random tabs

* Tue Jun 27 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.26.18-1
- Update to 8.26.18

* Sun Jun 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 8.25.18-2
- Invoke kmodtool with bash instead of sh.

* Wed May 24 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.25.18-1
- Update to 8.25.18
- drop patch25

* Thu May 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 8.24.8-3
- Require version >= of fglrx-kmod-common.
- Provide fglrx-kmod instead of kmod-fglrx to fix upgrade woes (#970).

* Thu Apr 27 2006 Ville Skyttä <ville.skytta at iki.fi> - 8.24.8-2
- Provide "kernel-modules" instead of "kernel-module" to match yum's config.

* Sat Apr 15 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 8.24.8-1
- Update to 8.24.8
- Remove old patches, x86_64 patch still needed

* Thu Mar 23 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 8.23.7.1-4
- apply patches that might fix x86_64 at least for some people

* Thu Mar 23 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 8.23.7.1-3
- disable xen0, too

* Wed Mar 22 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 8.23.7.1-2
- allow to pass kversion and kvariants via command line
- disable x86_64 (build problem)

* Sat Mar 18 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.23.7.1-1
- drop 0.lvn
- drop ati-fglrx-get_page.patch patch
- update to 8.23.7
- hardcode kversion and kvariants

* Wed Feb 08 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.20.8.1-0.lvn.2
- add ati-fglrx-accessok.patch

* Mon Jan 30 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.20.8.1-0.lvn.1
- split into packages for userland and kmod
- rename to fglrx-kmod

* Mon Dec 19 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.20.8.1-0.lvn.3
- Add patch for kernel 2.6.15

* Tue Dec 13 2005 Dams <anvil[AT]livna.org> - 8.20.8.1-0.lvn.2
- Really dropped Epoch

* Sat Dec 10 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.20.8.1-0.lvn.1
- Update to 8.20.8-1
- Drop Epoch

* Sun Nov 13 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.19.10.1-0.lvn.2
- Patch for 2.6.14 still needed on x86_64 (thx Ryo Dairiki for noticing)

* Sat Nov 12 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.19.10.1-0.lvn.1
- Update to 8.19.10-1
- Remove patches for 2.6.14
- Add fresh translation to desktop-file

* Wed Nov 09 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.18.6.1-0.lvn.2
- Patch kernel-module source to compile with 2.6.14

* Thu Oct 13 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.18.6.1-0.lvn.1
- Update to 8.18.6-1
- Conflict with nvidia-glx{,-legacy) (#627)
- Fix moduleline.split in ati-fglrx-config-display (#582)
- Unload drm in ati-fglrx-config-display, too
- Only ship self compiled fireglcontrolpanel

* Fri Aug 19 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.16.20.1-0.lvn.1
- Update to 8.16.20-1
- Update patch1, fireglcontrol.desktop
- Don't strip kernel-module for now

* Tue Jun 07 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.5
- Update fglrx-2.6.12-inter_module_get.patch (thx to Mike Duigou)

* Tue Jun 07 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.4
- Add patches from http://ati.cchtml.com/show_bug.cgi?id=136 and some tricks
  to built with 2.6.12 -- fixes building for FC4

* Tue Jun 07 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.3
- Missed one thing during reword of kernel-module-build-stuff
- Both x86_64 and x86 in the same package now

* Sun Jun 05 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.2
- Fix thinko

* Sun Jun 05 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.1
- Rework kernel-module-build-stuff for FC3 kmd and FC4 and new livna scheme
- Simplify the install; Lowers risk to miss files and is easier to maintain
- Remove dep on fedora-rpmdevtools
- Use modules and userland rpmbuild parameter to not build kernel- or driver-package

* Wed May 04 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.12.10.1-0.lvn.2
- Add fix for kernel 2.6.11

* Fri Apr 08 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.12.10.1-0.lvn.1
- Update to 8.12.10-1
- mod 0755 dri.so to let rpm detect require libstdc++.so.5

* Thu Mar 06 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.10.19.1-0.lvn.2
- Add patch for via agpgart (#355)

* Thu Feb 17 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.10.19.1-0.lvn.1
- Update to 8.10.19-1
- Remove patch for 2.6.10 kernel
- require libstdc++.so.5

* Wed Jan 19 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.8.25.1-0.lvn.4
- fix x86-64 in spec-file and in ati-fglrx-config-display
- Fix by Ville Skyttä: ldconfig on upgrades

* Wed Jan 19 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.8.25.1-0.lvn.3
- Package library links

* Wed Jan 19 2005 Dams <anvil[AT]livna.org> - 0:8.8.25.1-0.lvn.2
- Urlized ati rpm source

* Sat Jan 15 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.8.25.1-0.lvn.1
- Update to 8.8.25
- Remove workaround from last version
- Remove special drm includes
- Prepare package for 64-bit version; But untested ATM
- Update patches

* Tue Jan 11 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.6-0.lvn.3
- add patch10 -- allows building on 2.6.10; Found:
  http://www.rage3d.com/board/showthread.php?t=33798874&highlight=2.6.10
- update drm-includes
- temporary for kernel-module:  Requires: ati-fglrx >= %%{epoch}:%%{version}-0.lvn.2
  so we don't have to rebuild the driver package

* Sun Nov 21 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.6-0.lvn.2
- Use kernelp and driverp rpmbuild parameter to not build kernel- or
  driver-package
- Trim doc in header

* Fri Nov 04 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.6-0.lvn.1
- Update to 3.14.6

* Fri Nov 04 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.7
- Build per default without kmoddev
- Rename --without tools to --without dirverp
- Update dri-headers to 2.6.9 version
- update building documentation in header

* Fri Oct 22 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.6
- Some small cleanups to various parts of the package as suggested by Dams

* Fri Oct 22 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.5
- Enhance makefile patch so building with different uname should work correctly
- Build verbose

* Thu Oct 21 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.4
- Update fedora-unrpm usage to work with newer version
- Update one para in README and ati-fglrx-config-display output

* Fri Oct 15 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.3
- Change the enabling/disabling methode again -- driver is changed now
  directly. DRI is enabled when fglrx is enabled, but try to unload/warn if
  radeon kernel-module is loaded. DRI will be disabled and reenabled on the
  when next restart when disableing fglrx driver.
- Update README.fglrx.Fedora

* Mon Oct 11 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.2
- Let new version of ati-flrx-config-display change default depth to 24
- Updated Spec-File bits: fedora-kmodhelper usage and building description

* Thu Sep 30 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.1
- Update to 3.14.1
- In expectation of missing kernel-sourcecode package in FC3 remove the BR
  on it and include the neccessary header-files in the package. Will
  integrate more packages if there are API changes. But for now I
  think this is the easiest methode.
- Let ati-flrx-config-display handle /etc/ld.so.conf.d/ati-fglrx.conf
- Update ati-flrx-config-display; it adds a VideoOverlay Option now
  so xv works out of the box
- Don't (de)activate driver if DRI-Kernel-Modules are loaded; Let the
  init script to that during restart
- Update README.fglrx.Fedora

* Wed Sep 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.12.0-0.lvn.2
- Allow rpm to strip the kernel module.
- Fix shared library permissions.
- Split Requires(post,postun) to two to work around a bug in rpm.
- Fix -devel dependencies and kernel module package provisions.
- Improve summary and description, remove misleading comments.

* Sat Sep 11 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.12.0-0.lvn.1
- Update to 3.12.0
- Fix some fedora-kmodhelper/kernel-module related bits in spec
- Clean up install part a bit more

* Sun Sep 05 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.6
- Add stupid ati-fglrx.profile.d workaround for systems that had the
  original fglrx drivers installed before
- Conflict with fglrx -- the package should be removed so it can clean up
  the mess it did itself.
- Clean up desktop file

* Tue Aug 24 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.5
- Add ifdefs so building tools and kernel-module can be separated
- BuildRequire kernel-sourcecode kverrel, not kernel

* Wed Aug 17 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.4
- Fixed double release in Requires of devel-package
- Building against custom kernels now should work using rhkernel-macro
- Updated fedora-kmodhelper to 0.9.10
- Add 'include ld.so.conf.d/*.conf' before /usr/lib/X11 in /etc/ld.so.conf if
  it does not exists

* Wed Aug 10 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.3
- small fixes for dump issues

* Thu Aug 09 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.2
- BuildRequire fedora-rpmdevtools
- Use KERNEL_PATH correctly, needs updated patch1

* Sat Aug 07 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.1
- Update to 3.11.1
- Minor fixes

* Fri Aug  6 2004 Dams <anvil[AT]livna.org> 0:3.9.0-0.lvn.4
- .a files are 0644 moded. tgz files too.
- Added missing BuildReq: desktop-file-utils, qt-devel, fedora-rpmdevtools

* Mon Jul 19 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.9.0-0.lvn.3
- Update Patches to a working solution
- Modify start-script-- fglrx can also work without kernel-module (no DRI then)

* Sun Jul 18 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.9.0-0.lvn.2
- intergrate Readme, init-script and ati-fglrx-config-display (stolen from
  nvidia package)

* Sat Jul 17 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.9.0-0.lvn.1
- Initial RPM release.
