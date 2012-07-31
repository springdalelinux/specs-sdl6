%define kmod_name nvidia-96xx

Name:          nvidia-96xx-kmod
Version:       96.43.20
Release:       2%{?dist}
# Taken over by kmodtool
Summary:       NVIDIA 96xx display driver kernel module
Group:         System Environment/Kernel
License:       Redistributable, no modification permitted
URL:           http://www.nvidia.com/
# Source is created from these files:
# http://us.download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}-pkg0.run
# http://us.download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}-pkg0.run

# <switch me> when sources are on kwizart's repo
Source0:       http://rpms.kwizart.net/fedora/SOURCES/nvidia-kmod-data-%{version}.tar.bz2
#Source0:       http://www.diffingo.com/downloads/livna/kmod-data/nvidia-kmod-data-%{version}.tar.bz2
# </switch me>
Source11:      nvidia-kmodtool-excludekernel-filterfile
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i686 x86_64

BuildRequires:  %kernel_module_package_buildreqs
%kernel_module_package -n %{kmod_name}

%description
The nvidia %{version} display driver kernel module for kernel %{kversion}.

%prep
%setup -q -c -T -a 0

# patch loop
#for arch in x86 x64
#do
#    pushd nvidiapkg-${arch}
# empty
#    popd
#done

for flavor in %flavors_to_build ; do
%ifarch %{ix86}
    cp -a nvidiapkg-x86 _kmod_build_${flavor}
%else
    cp -a nvidiapkg-x64 _kmod_build_${flavor}
%endif
done

%build
for flavor in %flavors_to_build ; do
    pushd _kmod_build_${flavor}/usr/src/nv/
    ln -s -f Makefile.kbuild Makefile
    case $flavor in
	*xen*)
		CC="cc -D__XEN_TOOLS__ \
		-I%{kernel_version $flavor}/include/asm/mach-xen" \
		IGNORE_XEN_PRESENCE=1 \
		make %{?_smp_mflags}  SYSSRC="%{kernel_source $flavor}" module
		;;
	*)
		IGNORE_XEN_PRESENCE=1 \
		make %{?_smp_mflags}  SYSSRC="%{kernel_source $flavor}" module
		;;
    esac
    popd
done

%install
rm -rf $RPM_BUILD_ROOT
for flavor in %flavors_to_build ; do
    install -D -m 0755 _kmod_build_${flavor}/usr/src/nv/nvidia.ko $RPM_BUILD_ROOT/lib/modules/%kverrel${flavor%default}/extra/%{kmod_name}/nvidia.ko
done

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Wed Nov 03 2010 Nicolas Chauvet <kwizart@gmail.com> - 96.43.19-1
- Update to 96.43.19

* Thu Oct 21 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.18-1.5
- rebuild for new kernel

* Sun Sep 19 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.18-1.4
- rebuild for new kernel

* Mon Sep 13 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.18-1.3
- rebuild to build i686 packages

* Wed Sep 01 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.18-1.2
- rebuild for new kernel

* Fri Aug 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.18-1.1
- rebuild for new kernel

* Sat Aug 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 96.43.18-1
- Update to 96.43.18

* Tue Jul 27 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.16-1.10
- rebuild for new kernel

* Wed Jul 07 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.16-1.9
- rebuild for new kernel

* Fri Jun 18 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.16-1.8
- rebuild for new kernel

* Sat May 01 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.16-1.7
- rebuild for new kernel

* Thu Apr 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.16-1.6
- rebuild for new kernel

* Thu Apr 22 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.16-1.5
- rebuild for new kernel

* Mon Apr 19 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.16-1.4
- rebuild for new kernel

* Sat Apr 17 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.16-1.3
- rebuild for new kernel

* Sat Apr 10 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.16-1.2
- rebuild for new kernel

* Mon Mar 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.16-1.1
- rebuild for new kernel

* Sat Mar 27 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 96.43.16-1
- Update to 96.43.16

* Fri Mar 05 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.14
- rebuild for new kernel

* Mon Mar 01 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.13
- rebuild for new kernel

* Sun Feb 28 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.12
- rebuild for new kernel

* Sat Feb 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.11
- rebuild for new kernel

* Sat Feb 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.10
- rebuild for new kernel

* Thu Feb 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.9
- rebuild for new kernel

* Wed Feb 10 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.8
- rebuild for new kernel

* Sat Jan 30 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.7
- rebuild for new kernel

* Wed Jan 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.6
- rebuild for new kernel

* Sat Dec 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.5
- rebuild for new kernel

* Thu Dec 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.4
- rebuild for new kernel

* Sun Dec 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.3
- rebuild for new kernel

* Wed Nov 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.2
- rebuild for new kernel

* Sun Nov 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.14-1.1
- rebuild for new kernel, disable i586 builds

* Sat Nov 14 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 96.43.14-1
- Update to 96.43.14

* Thu Nov 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.13-1.4
- rebuild for new kernels

* Tue Oct 20 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.13-1.3
- rebuild for new kernels

* Wed Sep 30 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.13-1.2
- rebuild for new kernels

* Tue Sep  1 2009 kwizart < kwizart at gmail.com > - 96.43.13-1.1
- rebuild for new kernels

* Mon Aug 31 2009 kwizart < kwizart at gmail.com > - 96.43.13-1
- Update to 96.43.13 (beta)

* Thu Aug 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.17
- rebuild for new kernels

* Sun Aug 23 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.16
- rebuild for new kernels

* Sat Aug 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.15
- rebuild for new kernels

* Sat Aug 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.14
- rebuild for new kernels

* Fri Aug 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.13
- rebuild for new kernels

* Fri Jul 31 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.12
- rebuild for new kernels

* Tue Jul 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.11
- rebuild for new kernels

* Sun Jun 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.10
- rebuild for new kernels

* Sun Jun 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.9
- rebuild for new kernels

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.8
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.7
- rebuild for new kernels

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.6
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.5
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.4
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.3
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.2
- rebuild for new kernels

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2.1
- rebuild for new kernels

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.11-2
- rebuild for new F11 features

* Wed Feb 25 2009 kwizart < kwizart at gmail.com > - 96.43.11-1
- Update to 96.43.11 (stable)

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.10-2.2
- rebuild for latest Fedora kernel;

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.10-2.1
- rebuild for latest Fedora kernel;

* Thu Jan 29 2009 kwizart < kwizart at gmail.com > - 96.43.10-2
- Update the spec file in sync with nvidia-kmod

* Thu Jan 29 2009 kwizart < kwizart at gmail.com > - 96.43.10-1
- Update to 96.43.10 (beta)

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.09-1.12
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.09-1.11
- rebuild for latest Fedora kernel;

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.09-1.10
- rebuild for latest Fedora kernel;

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.09-1.9
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.09-1.8
- rebuild for latest Fedora kernel;

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.09-1.7
- rebuild for latest Fedora kernel;

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.09-1.6
- rebuild for latest Fedora kernel;

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.09-1.5
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.09-1.4
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.09-1.3
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.09-1.2
- rebuild for latest Fedora kernel;

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.09-1.1
- rebuild for latest Fedora kernel;

* Thu Oct 30 2008 kwizart < kwizart at gmail.com > - 96.43.09-1
- Update to 96.43.09 (beta)

* Thu Oct 23 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 96.43.07-6.2
- rebuild for latest kernel

* Sun Oct 05 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 96.43.07-6.1
- rebuild for rpm fusion

* Wed Oct 01 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 96.43.07-5
- rebuild for new kernels

* Sun Sep 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 96.43.07-4
- rebuild for new kernels

* Sat Aug 16 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 96.43.07-3
- rebuild for new kernels

* Thu Jul 24 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.07-2
- rebuild for new Fedora kernels

* Sat Jul 19 2008 Stewart Adam <s.adam at diffingo.com> - 96.43.07-1
- Update to 96.43.07
- Remove 2.6.25 patch

* Tue Jul 15 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-15
- rebuild for new Fedora kernels

* Thu Jul 03 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-14
- rebuild for new Fedora kernels

* Fri Jun 20 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-13
- rebuild for new Fedora kernels

* Fri Jun 06 2008 kwizart < kwizart at gmail.com > - 96.43.05-12
- Add Patch for 2.6.25 kernels

* Fri Jun 06 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-11
- rebuild for new Fedora kernels

* Thu May 15 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-10
- rebuild for new Fedora kernels

* Fri Apr 25 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-9
- rebuild for 2.6.24.5-85.fc8 2.6.21.7-3.fc8xen

* Wed Apr 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-8
- rebuild for 2.6.24.4-64.fc8 2.6.21.7-3.fc8xen (second try)

* Mon Mar 31 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-7
- rebuild for 2.6.24.4-64.fc8 2.6.21.7-3.fc8xen

* Wed Mar 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-6
- rebuild for 2.6.24.3-50.fc8

* Sun Mar 16 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-5
- rebuild for 2.6.24.3-34.fc8

* Fri Mar 07 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-4
- rebuild for 2.6.24.3-12.fc8 2.6.21.7-2.fc8xen

* Mon Feb 11 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-3
- rebuild for 2.6.23.15-137.fc8

* Wed Feb 06 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.05-2
- rebuild for 2.6.23.14-115.fc8

* Mon Feb  4 2008 kwizar < kwizart at gmail.com > - 96.43.05-1
- Update to 96.43.05

* Thu Jan 24 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-20
- rebuilt for 2.6.23.9-107.fc8

* Thu Dec 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-19
- rebuilt for 2.6.21-2952.fc8xen 2.6.23.9-85.fc8

* Mon Dec 03 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-18
- rebuilt for 2.6.23.8-63.fc8 2.6.21-2952.fc8xen

* Sat Nov 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-17
- rebuilt for 2.6.23.1-49.fc8

* Mon Nov 05 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-16
- rebuilt for F8 kernels

* Wed Oct 31 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-15
- rebuilt for latest kernels

* Tue Oct 30 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-14
- rebuilt for latest kernels

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-13
- rebuilt for latest kernels
- adjust to rpmfusion and new kmodtool

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-12
- rebuilt for latest kernels

* Tue Oct 23 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-11
- rebuilt for latest kernels

* Mon Oct 22 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-10
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-9
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-8
- rebuilt for latest kernels

* Fri Oct 12 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-7
- rebuilt for latest kernels

* Thu Oct 11 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-6
- rebuilt for latest kernels

* Wed Oct 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 96.43.01-5
- rebuilt for latest kernels

* Tue Oct 09 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 96.43.01-4
- rebuilt for latest kernels

* Sun Oct 07 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> 
- build for rawhide kernels as of today

* Thu Oct 04 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 96.43.01-2
- update for new kmod-helper stuff
- build for newest kernels

* Wed Oct  3 2007 kwizart < kwizart at gmail.com > - 96.43.01-1
- Update to 96.43.01

* Wed May 30 2007 kwizar < kwizart at gmail.com > - 1.0.9639-1
- Update to 1.0.9639

* Fri Apr 27 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9631-12
- Rebuild for F7T4 (fixed kversion)

* Fri Apr 27 2007 kwizart < kwizart at gmail.com > - 1.0.9631-11
- Build for Fedora test4 kernel

* Sun Mar 4 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9631-10
- kdump for non-i686

* Sat Mar 3 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9631-9
- Patch shouldn't be a URL!
- No kdump
- New kernel

* Fri Mar 2 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9631-8
- New kernel
- Make Source0 a URL

* Sat Feb 24 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9631-7
- Standardize all summaries and descriptions with other nvidia and fglrx
  packages
- Move paths from nvidia-glx to nvidia-96xx

* Wed Feb 7 2007 kwizart < kwizar at gmail.com > - 1.0.9631-6
- Disable xen variant
 
* Wed Feb 7 2007 kwizart < kwizar at gmail.com > - 1.0.9631-5
- Rebuild for Fedora Core 7 test1

* Sat Jan 13 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9631-4
- Initial release
- Make %%Source0 a URL

* Sun Jan  7 2007 kwizart < kwizart at gmail.com > - 1.0.9631-3
- Update xen patch patch-nv-1.0-9625-xenrt.txt (not the newest anyway)!
- Fix perm in SOURCES.

* Thu Dec 28 2006 kwizart < kwizart at gmail.com > - 1.0.9631-2
- New legacy version named kmod-nvidia-96xx

* Thu Dec 07 2006 kwizart < kwizart at gmail.com > - 1.0.9631-1
- Update to 1.0.9631-1

* Tue Nov 07 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.9629-1
- update to release 1.0.9629
- include xen patch (thx to Bob Richmond)

* Wed Nov 01 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.9626-2
- include patch from 
  http://www.nvnews.net/vbulletin/showpost.php?p=996233&postcount=20

* Sun Oct 22 2006 Stewart Adam <s.adam AT diffingo DOT com> - 1.0.9626-1
- update to release 1.0.9626

* Sat Oct 07 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8774-2
- sed-away the config.h include

* Thu Aug 24 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8774-1
- update to release 1.0.8774

* Thu Aug 10 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8762-5
- update for kernel 2.6.17-1.2174_FC5

* Mon Aug 07 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8762-4
- forgot to update release field

* Fri Aug 04 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8762-3
- minor changes to spacing, removal of random tabs, re-arrangements

* Sun Jun 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.8762-2
- Invoke kmodtool with bash instead of sh.

* Wed May 24 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8762-1
- update to 1.0.8762

* Sun May 14 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.8756-3
- Require version >= of nvidia-kmod-common.
- Provide nvidia-kmod instead of kmod-nvidia to fix upgrade woes (#970).

* Thu Apr 27 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.8756-2
- Provide "kernel-modules" instead of "kernel-module" to match yum's config.

* Sat Apr 08 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8756-1
- Update to 8756
- drop patch

* Thu Mar 23 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8178-6
- disable xen0 for now

* Wed Mar 22 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8178-5
- build for 2.6.16-1.2069_FC5

* Wed Mar 22 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8178-4
- allow to pass kversion and kvariants via command line

* Sat Mar 18 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8178-3
- drop 0.lvn
- use kmodtool from svn
- hardcode kernel and variants

* Mon Jan 30 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8178-0.lvn.2
- Some minor fixes
- new kmodtool

* Sun Jan 22 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8178-0.lvn.1
- split into packages for userland and kmod
- rename to nvidia-kmod

* Thu Dec 22 2005 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 0:1.0.8178-0.lvn.2
- change nvidia-glx.sh and nvidia-glx.csh to point to README.txt rather than README
- reference xorg.conf rather than XF86Config in the init script
- improve readability of instructions and comments, fix some typos
- drop epoch, as it seems to be affecting dependencies according to rpmlint
- tweak the nvidia-settings desktop file so it always shows up on the
  menu in the right location
- add the manual pages for nvidia-settings and nvidia-xconfig
- remove header entries from the nvidia-glx files list. they belong in -devel
- fix changelog entries to refer to 7676 not 7176 (though there was a 7176 x86_64
  release prior to 7174)
- add libXvMCNVIDIA.so
- update to 8178

* Wed Dec 07 2005 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 0:1.0.8174-0.lvn.1
- add the manual pages for nvidia-settings and nvidia-xconfig
- install the new nvidia-xconfig utility and associated libs

* Mon Dec 05 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.8174-0.lvn.1
- Update to 8174
- desktop entry now Categories=Settings (#665)
- Ship bug-reporting tool in doc (#588)
- Things from Bug 635, Niko Mirthes (straw) <nmirthes AT gmail DOT com>:
-- avoid changing time stamps on libs where possible
-- only add /etc/modprobe.conf entries if they aren't already there
-- add /etc/modprobe.conf entries one at a time
-- only remove /etc/modprobe.conf entries at uninstall, not during upgrade
-- avoid removing any modprobe.conf entries other than our own
-- match Xorg's install defaults where it makes sense (0444)
-- a few other minor tweaks to the files lists

* Sun Sep 04 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.7676-0.lvn.3
- Conflics with nvidia-glx-legacy
- Integrate some minor correction suggested by Niko Mirthes
  <nmirthes AT gmail DOT com> in #475

* Fri Aug 26 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.7676-0.lvn.2
- Rename src5: nvidia.init to nvidia-glx-init
- Fix correct servicename in nvidia-glx-init
- Run nvidia-glx-init before gdm-early-login; del and readd the script
  during post

* Sun Aug 21 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.7676-0.lvn.1
- Update to 7676
- Lots of cleanup from me and Niko Mirthes <nmirthes AT gmail DOT com>
- add NVreg_ModifyDeviceFiles=0 to modprobe.conf (Niko)
- Drop support for FC2
- Nearly proper Udev-Support with workarounds around FC-Bug 151527

* Fri Jun 17 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7174-0.lvn.5
- Slight change of modprobe.conf rexexp

* Thu Jun 16 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7174-0.lvn.4
- Fixed a critical bug in modprobe.conf editing where all lines starting with alias and
  ending with then a word starting with any of the letters n,v,i,d,i,a,N,V,r,e is removed.

* Mon Jun 13 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.7174-0.lvn.3
- Adjust kenrnel-module-stuff for FC4
- Ship both x86 and x64 in the SRPM

* Sun Jun 12 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7174-0.lvn.2
- Only create 16 devices
- Put libXvMCNVIDIA.a in -devel
- Don't remove nvidia options in /etc/modprobe.conf
- Make ld.so.conf file config(noreplace)
- Use same directory permissions as the kernel

* Sat Apr 2 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7174-0.lvn.1
- New upstream release, 7174

* Wed Mar 30 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7167-0.lvn.5
- Added x86_64 support patch from Thorsten Leemhuis

* Wed Mar 23 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7167-0.lvn.4
- Fix kernel module permissions again (644)
- Only create 16 /dev/nvidia* devices, 256 is unnecessary

* Fri Mar 18 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7167-0.lvn.3
- Fixed kernel-module permissions

* Thu Mar 17 2005 Dams <anvil[AT]livna.org> 0:1.0.7167-0.lvn.2
- Removed provides on kernel-module and kernel-modules

* Sat Mar 05 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7167-0.lvn.1
- New upstream release 1.0.7167
- Added patch from http://www.nvnews.net/vbulletin/showthread.php?t=47405
- Removed old patch against 2.6.9

* Sat Feb 05 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6629-0.lvn.7
- Added a number of post-6629 patches from http://www.minion.de/files/1.0-6629
- Fixed permissions of nvidia/nvidia.ko

* Fri Jan 21 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6629-0.lvn.6
- Fix incorrect MAKDEV behaviour and dependency

* Tue Nov 30 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6629-0.lvn.4
- Fixed creation of /dev/nvidia* on FC2

* Sat Nov 27 2004 Dams <anvil[AT]livna.org> - 0:1.0.6629-0.lvn.3
- Dont try to print kvariant in description when it's not defined.

* Sun Nov 21 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:1.0.6629-0.lvn.2
- resulting kernel-module package now depends again on /root/vmlinuz-<kernelver>
- Use rpmbuildtags driverp and kernelp

* Sat Nov 06 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6629-0.lvn.1
- New upstream version, 1.0-6629
- Build without kernel-module-devel by default

* Fri Oct 29 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.6
- Make n-c-display handle misc problems in a better way
- Fixed wrong icon file name in .desktop file
- Re-added the mysteriously vanished sleep line in the init script
  when kernel module wasn't present

* Fri Oct 22 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:1.0.6111-0.lvn.5
- Use fedora-kmodhelper in the way ntfs or ati-fglrx use it
- Allow rpm to strip the kernel module. Does not safe that much space ATM but
  might be a good idea
- Allow to build driver and kernel-module packages independent of each other
- Some minor spec-file changes

* Thu Oct 21 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.4
- udev fixes
- Incorporated fix for missing include line in ld.so.conf from ati-fglrx spec (T Leemhuis)

* Sun Sep 19 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.3
- Remove FC1/kernel 2.4 compability
- Rename srpm to nvidia-glx
- Build with kernel-module-devel

* Sun Aug 15 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.2
- Restore ldsoconfd macro
- Disable autoamtic removal of scripted installation for now; needs testing

* Sat Aug 14 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.1
- Upstream release 6111
- Fixed init script (again)

* Tue Aug  3 2004 Dams <anvil[AT]livna.org> 0:1.0.6106-0.lvn.4
- ld.so.conf.d directory detected by spec file
- Using nvidialibdir in nvidia-glx-devel files section
- Got rid of yarrow and tettnang macros
- libGL.so.1 symlink in tls directory always present

* Mon Jul 19 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.3
- Fixed script bug that would empty prelink.conf
- Added symlink to non-tls libGL.so.1 on FC1

* Tue Jul 13 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.2.3
- Updated init script to reflect name change -xfree86 -> -display

* Mon Jul 12 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.2.2
- Fixed backup file naming

* Sun Jul 11 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.2.1
- Restore working macros
- Always package the gui tool

* Sun Jul 11 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.2
- Renamed nvidia-config-xfree86 to nvidia-config-display
- Fixed symlinks
- Use ld.so.conf.d on FC2
- Remove script installation in pre
- Use system-config-display icon for nvidia-settings
- 2 second delay in init script when kernel module not found
- Make nvidia-config-display fail more gracefully
- Add blacklist entry to prelink.conf on FC1

* Mon Jul 05 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.1
- New upstream release
- First attempt to support FC2
- Dropped dependency on XFree86

* Mon Feb 09 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.5336-0.lvn.3
- Use pkg0

* Sun Feb 08 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.5336-0.lvn.2
- New Makefile variable SYSSRC to point to kernel sources.
- kmodhelper fixes.

* Fri Jan 30 2004 Keith G. Robertson-Turner <nvidia-devel[AT]genesis-x.nildram.co.uk> 0:1.0.5336-0.lvn.1
- New upstream release
- Removed (now obsolete) kernel-2.6 patch
- Install target changed upstream, from "nvidia.o" to "module"
- Linked nv/Makefile.kbuild to (now missing) nv/Makefile

* Sun Jan 25 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.18
- Updated nvidia-config-display
- Now requiring pyxf86config

* Mon Jan 19 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.17
- Added nvidiasettings macro to enable/disable gui packaging

* Mon Jan 19 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.16
- Updated minion.de patches
- Added some explicit requires
- Test nvidia-config-xfree86 presence in kernel-module package
  scriptlets

* Mon Jan 12 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.15
- Updated Readme.fedora
- nvidia-glx-devel package

* Sat Jan  3 2004 Dams <anvil[AT]livna.org> 0:1.0.5328-0.lvn.14
- Hopefully fixed kernel variant thingy

* Fri Jan  2 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.13
- Support for other kernel variants (bigmem, etc..)
- Changed URL in Source0

* Tue Dec 30 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.13
- Dropped nvidia pkgX information in release tag.

* Tue Dec 30 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.12.pkg0
- Renamed kernel module package in a kernel-module-nvidia-`uname -r` way
- Using fedora.us kmodhelper for kernel macro
- Using nvidia pkg0 archive

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.11.pkg1
- kernel-module-nvidia package provides kernel-module
- We wont own devices anymore. And we wont re-create them if they are
  already present

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.10.pkg1
- Yet another initscript update. Really.
- Scriptlets updated too

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.9.pkg1
- Fixed alias in modprobe.conf for 2.6

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.8.pkg1
- Another initscript update

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.7.pkg1
- kernel module requires kernel same kversion
- initscript updated again
- Dont conflict, nor obsolete XFree86-Mesa-libGL. Using ld.so.conf to
  make libGL from nvidia first found. Hope Mike Harris will appreciate.

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.6.pkg1
- kernel-module-nvidia requires kernel same version-release

* Sat Dec 20 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.6.pkg1
- Updated initscript

* Fri Dec 19 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.5.pkg1
- lvn repository tag

* Fri Dec 19 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.fdr.5.pkg1
- Added initscript to toggle nvidia driver according to running kernel
  and installed kernel-module-nvidia packages
- Updated scriptlets

* Thu Dec 18 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.fdr.4.pkg1
- Arch detection
- Url in patch0

* Tue Dec 16 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.fdr.3.pkg1
- Desktop entry for nvidia-settings
- s/kernel-module-{name}/kernel-module-nvidia
- nvidia-glx doesnt requires kernel-module-nvidia-driver anymore
- Using modprobe.conf for 2.6 kernel
- Hopefully fixed symlinks

* Mon Dec 15 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.fdr.2.pkg1
- Building kernel module for defined kernel
- kernel module for 2.6 is nvidia.ko
- Patch not to install kernel module on make install
- Updated patch for 2.6
- depmod in scriptlet for defined kernel
- nvidia-glx conflicting XFree86-Mesa-libGL because we 0wn all its
  symlink now
- Dont override libGL.so symlink because it belongs to XFree86-devel
- Added nvidia 'pkgfoo' info to packages release
- Spec file cleanup

* Fri Dec 12 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4620-0.fdr.2
- Fixed repairing of a link in post-uninstall
- Obsolete Mesa instead of Conflict with it, enables automatic removal.

* Mon Dec 08 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4620-0.fdr.1
- Added support for 2.6 kernels
- Cleaned up build section, removed the need for patching Makefiles.
- Added missing BuildReq gcc32
- Don't package libs twice, only in /usr/lib/tls/nvidia
- Made config cript executable and put it into /usr/sbin
- Moved kernel module to kernel/drivers/video/nvidia/
- Fixed libGL.so and libGLcore.so.1 links to allow linking against OpenGL libraries

* Mon Dec 08 2003 Keith G. Robertson-Turner <nvidia-devel at genesis-x.nildram.co.uk> - 0:1.0.4620-0.fdr.0
- New beta 4620 driver
- New GUI control panel
- Some minor fixes

* Thu Nov 20 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.10.1
- Finally fixed SMP builds.

* Wed Nov 19 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.9
- Don't make nvidia-glx depend on kernel-smp

* Tue Nov 18 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.8
- Some build fixes

* Tue Nov 11 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.7
- Added CC=gcc32
- Fixed upgrading issue
- Added driver switching capabilities to config script.

* Fri Nov 07 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.4
- Added conflict with XFree86-Mesa-libGL.
- Disabled showing of the README.Fedora after installation.

* Sun Oct 12 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.3
- Added NVidia configuration script written in Python.
- Some cleanup of files section
- For more info, see https://bugzilla.fedora.us/show_bug.cgi?id=402

* Tue Jul 08 2003 Andreas Bierfert (awjb) <andreas.bierfert[AT]awbsworld.de> - 0:1.0.4363-0.fdr.2
- renamed /sbin/makedevices.sh /sbin/nvidia-makedevices.sh ( noticed by
  Panu Matilainen )
- Fixed name problem
* Sun Jun 22 2003 Andreas Bierfert (awjb) <andreas.bierfert[AT]awbsworld.de> - 0:1.0.4363-0.fdr.1
- Initial RPM release, still some ugly stuff in there but should work...
