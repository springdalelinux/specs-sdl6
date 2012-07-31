%{!?octave_api: %define octave_api %(octave-config -p API_VERSION || echo 0)}

Name:           octave-forge
Version:        20090607
Release:        17%{?dist}
Summary:        Contributed functions for octave

Group:          Applications/Engineering
License:        GPLv2+ and Public Domain
URL:            http://octave.sourceforge.net
## Source0:        http://downloads.sourceforge.net/sourceforge/octave/%{name}-bundle-%{version}.tar.gz
## The original sources contain a non-free tree of functions that are
## GPL incompatible. A patched version with the non-free sources removed
## is created as follows:
## tar xzf octave-forge-bundle-%{version}.tar.gz
## rm -Rf octave-forge-bundle-%{version}/nonfree/
## tar czf octave-forge-bundle-%{version}.patched.tar.gz octave-forge-bundle-%{version}
## rm -Rf octave-forge-bundle-%{version}
Source0:        %{name}-bundle-%{version}.patched.tar.gz
Patch0:		octave-forge-20090607-ann-swig-build.patch
Patch1:		octave-forge-20090607-parallel-build.patch
Patch2:		octave-forge-20090607-java-build.patch
Patch3:		octave-forge-20090607-fixed-build.patch
Patch4:		octave-forge-20090607-vrml-build.patch
Patch5:		octave-forge-20090607-ann-debian-noautoload.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  octave-devel >= 6:3.0.0-1
BuildRequires:  tetex gcc-gfortran ginac-devel
BuildRequires:  ImageMagick-c++-devel libnc-dap-devel pcre-devel gsl-devel
BuildRequires:  libjpeg-devel libpng-devel ncurses-devel ftplib-devel
BuildRequires:  openssl-devel java-devel-gcj

Requires:	octave(api) = %{octave_api} ImageMagick

# Main
Provides: octave-ann = 1.0.2
Provides: octave-audio = 1.1.4
Provides: octave-benchmark = 1.1.1
Provides: octave-bioinfo = 0.1.2
Provides: octave-combinatorics = 1.0.9
Provides: octave-communications = 1.0.10
Provides: octave-control = 1.0.11
# octave-database is removed
Provides: octave-data-smoothing = 1.2.0
Provides: octave-econometrics = 1.0.8
Provides: octave-financial = 0.3.2
Provides: octave-fixed = 0.7.10
# temporarily disable: SWIG wrappers are broken: known upstream
# Provides: octave-ftp = 1.0.2
Provides: octave-ga = 0.9.7
Provides: octave-general = 1.1.3
Provides: octave-gsl = 1.0.8
Provides: octave-ident = 1.0.7
Provides: octave-image = 1.0.10
Provides: octave-informationtheory = 0.1.8
Provides: octave-io = 1.0.9
Provides: octave-irsa = 1.0.7
Provides: octave-linear-algebra = 1.0.8
Provides: octave-miscellaneous = 1.0.9
Provides: octave-missing-functions = 1.0.2
Provides: octave-nnet = 0.1.10
Provides: octave-octcdf = 1.0.13
Provides: octave-octgpr = 1.1.5
Provides: octave-odebvp = 1.0.6
Provides: octave-odepkg = 0.6.7
Provides: octave-optim = 1.0.6
Provides: octave-optiminterp = 0.3.2
Provides: octave-outliers = 0.13.9
Provides: octave-parallel = 2.0.1
Provides: octave-physicalconstants = 0.1.7
Provides: octave-plot = 1.0.7
Provides: octave-quaternion = 1.0.0
Provides: octave-signal = 1.0.10
Provides: octave-simp = 1.1.0
Provides: octave-sockets = 1.0.5
Provides: octave-specfun = 1.0.8
Provides: octave-special-matrix = 1.0.7
Provides: octave-splines = 1.0.7
Provides: octave-statistics = 1.0.9
Provides: octave-strings = 1.0.7
Provides: octave-struct = 1.0.7
Provides: octave-symbolic = 1.0.9
Provides: octave-time = 1.0.9
# octave-video is removed
Provides: octave-vrml = 1.0.10
Provides: octave-zenity = 0.5.7

# Extra
Provides: octave-ad = 1.0.6
Provides: octave-bim = 0.1.1
Provides: octave-civil-engineering = 1.0.7
# octave-engine is removed
Provides: octave-fpl = 0.1.6
Provides: octave-generate_html = 0.0.9
# temporarily disable: doesn't yet build
# Provides: octave-graceplot = 1.0.8
Provides: octave-integration = 1.0.7
Provides: octave-java = 1.2.6
# octave-jhandles is removed
Provides: octave-mapping = 1.0.7
Provides: octave-msh = 0.1.1
Provides: octave-multicore = 0.2.15
Provides: octave-nan = 1.0.9
Provides: octave-nlwing2 = 1.1.1
Provides: octave-nurbs = 1.0.1
Provides: octave-ocs = 0.0.4
Provides: octave-oct2mat = 1.0.7
Provides: octave-pdb = 1.0.7
Provides: octave-secs1d = 0.0.8
Provides: octave-secs2d = 0.0.8
Provides: octave-symband = 1.0.10
Provides: octave-tcl-octave = 0.1.8
Provides: octave-tsa = 4.0.1
# octave-windows is removed
Provides: octave-xraylib = 1.0.8

# Language
# temporarily disable, doesn't build
# Provides: octave-spanish = 1.0.1
Provides: octave-pt_br = 1.0.8


%description
Octave-forge is a community project for collaborative development of
Octave extensions. The extensions in this package include additional
data types, and functions for a variety of different applications
including signal and image processing, communications, control,
optimization, statistics, and symbolic math.


%prep
%setup -q -n octave-forge-bundle-%{version}
# The scripts below will build everything automatically, so first
# remove some packages that we don't want to build:
# 1. video stuff requires non-free libraries
rm main/video-*.tar.gz
# 2. engine is not a real octave package
rm extra/engine-*.tar.gz
# 3. jhandles depends on jogl, which is forbidden from Fedora
rm extra/jhandles-*.tar.gz
# 4. other OS stuff
rm extra/windows-*.tar.gz
# 5. exclude database stuff--it should be in its own package
rm main/database-*.tar.gz
# 6. exclude ftp -- SWIG wrappers are broken
rm main/ftp-*.tar.gz
# 7. exclude graceplot --  doesn't build against Octave 3.2
rm extra/graceplot-*.tar.gz
# 8. exclude spanish -- doesn't build against Octave 3.2
rm language/spanish-*.tar.gz

#Unpack everything
for pkg in main extra language
do
   cd $pkg
   for tgz in *.tar.gz
   do
      tar xzf $tgz

      #Collect provides
      echo $tgz | sed 's/\(.*\)-\([0-9]*\.[0-9]*\.[0-9]*\)\.tar\.gz/Provides: octave-\1 = \2/' >> ../octave-forge-provides
   done
   cd ..
done

#apply patches
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p1

#Install with -nodeps
sed -i -e "s/pkg('install',/pkg('install','-nodeps',/" */*/Makefile


%build
#Prevents escape sequence from being inserted into octave version string
export TERM=""
for pkg in main extra language
do
   cd $pkg
   for dir in *.*[0-9]
   do
      cd $dir
      if [ -f configure ]
      then
         %configure
      elif [ -f src/configure ]
      then
         cd src
         %configure
         cd ..
      fi
      if [ -f Makefile ]
      then
         make TMPDIR=%{_tmppath}
      elif [ -f src/Makefile ]
      then
         cd src
         make TMPDIR=%{_tmppath}
         cd ..
      fi
      cd ..
   done
   cd ..
done
   

%install
rm -rf $RPM_BUILD_ROOT
export TERM=""

for pkg in main extra language
do
   cd $pkg
   for dir in *.*[0-9]
   do
       cd $dir
       make install TMPDIR=%{_tmppath} DESTDIR=$RPM_BUILD_ROOT DISTPKG=redhat
       cd ..
   done
   cd ..
done


%clean
rm -rf $RPM_BUILD_ROOT


%post
octave -q -H --no-site-file --eval "pkg('rebuild');"

%postun
octave -q -H --no-site-file --eval "pkg('rebuild');"


%files
%defattr(-,root,root,-)
%{_datadir}/octave/packages/
%{_libexecdir}/octave/packages/


%changelog
* Mon Jul  5 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-17
- Update java patch to disable autoloading of java package
  currently this package leads to crashing on exit (#562276)

* Sat Jun 19 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-16
- Adapt two patches from Debian to disable autoloading of 'ann' package:
  http://patch-tracker.debian.org/patch/series/view/octave-ann/1.0.2+dfsg-2/warn-clear-all-at-init.diff
  http://patch-tracker.debian.org/patch/series/view/octave-ann/1.0.2+dfsg-2/autoload-no.diff
  'ann' currently causes crashes even if not being used.
  Should workaround #562276 until upstream fixes the 'ann' package
  properly.

* Mon Sep  7 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-15
- Re-enable 'fixed' subpackage, builds now, this closes #510841
- ftp, graceplot and spanish packages need fixing upstream, leave
  disabled for the moment

* Mon Sep  7 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-14
- Re-enable java subpackage, now building
- Rebuild against new atlas, fixes the ieee warnings.

* Sun Sep  6 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-13
- Rebuild against new lapack/octave combination to fix ieee problem

* Mon Aug 31 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-12
- Add patch from upstream SVN (r6073) for 'vrml'
- Disable 'fixed' package again, patch fixed the build but fails at
  install-time on i686 probably for similar reasons java- fails to
  install

* Mon Aug 31 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-11
- Fixed shell globbing in build and install sections that missed
  packages with subminor versions (thanks Dmitri Sergatskov)
- Add patch from upstream SVN (r5936) to build fixed-0.7.10 package 
- Renumber patches

* Mon Aug 31 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-10
- Re-enable parallel package, fixed in upstream SVN (diff r5742:6118)
- Disable include patch, now part of parallel patch

* Mon Aug 31 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-9
- Temporarily disable java build again

* Thu Aug 20 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-8
- Add patch from upstream SVN (r6098) to fix 'java' build.
- Disable spanish package: doesn't build with Octave 3.2

* Thu Aug 20 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-7
- More build failures: remove java, report upstream as (yet) another
  broken package.

* Wed Aug 19 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-6
- More build failures: temporarily disable graceplot, report upstream
  as (yet) another broken package.

* Wed Aug 19 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-5
- Disable 'parallel' and associated patches temporarily just to get
  the whole thing to build and fix broken deps (upstream working on
  it)

* Wed Aug 19 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-4
- Add patch from SVN upstream (r6116) to fix build of parallel package
  (bump version of package to 2.0.1)

* Tue Aug 18 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-3
- Temporarily remove ftp because of build problems with SWIG upstream.

* Sat Aug  1 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-2
- Add patch from SVN (r6006) which has SWIG fixes for ann module.

* Fri Jul 31 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20090607-1
- Apply patch from Jussi Lehtola <jussilehtola@fedoraproject.org> to
  update to 20090607

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080831-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20080831-9
- Rebuild for dependencies

* Sat Mar 28 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20080831-8
- Rebuild for new ginac.

* Tue Mar 10 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20080831-7
- Fix BuildRequires to specifically request GCJ version of Java.

* Tue Mar 10 2009 Rakesh Pandit <rakesh@fedorapeople.org> - 20080831-6
- Bumped to consume the soname update in ImageMagic.

* Tue Feb 24 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20080831-5
- Rebuild against new hdf5 and for GCC 4.4.

* Mon Jan  5 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 20080831-4
- Patch to temporarily get image subpackage to build (#477577)

* Sun Jan 04 2009 Rakesh Pandit <rakesh@fedoraproject.org> 20080831-3
- Fixed unowned directories (BZ 474675)

* Thu Sep 11 2008 Orion Poplawski <orion@cora.nwra.com>  20080831-2
- Rebuild for new libdap

* Mon Sep 8 2008 Orion Poplawski <orion@cora.nwra.com>  20080831-1
- Update to 20080831
- Drop upstreamed patches
- Enable octave-parallel for 64-bit platforms

* Fri May  2 2008 Quentin Spencer <qspencer@users.sf.net> 20080429-6
- Add patch for new ImageMagick.

* Thu May  1 2008 Quentin Spencer <qspencer@users.sf.net> 20080429-5
- Modify the patch to fix compile flags in a subpackage.

* Thu May  1 2008 Quentin Spencer <qspencer@users.sf.net> 20080429-4
- Extend the gcc 4.3 patch to more files.

* Thu May  1 2008 Quentin Spencer <qspencer@users.sf.net> 20080429-3
- Fix the gcc 4.3 patch.

* Thu May  1 2008 Quentin Spencer <qspencer@users.sf.net> 20080429-2
- Patch so it will compile with gcc 4.3.

* Wed Apr 30 2008 Quentin Spencer <qspencer@users.sf.net> 20080429-1
- New release.
- Add ftplib-devel as dependency.
- Remove obsolete dependencies and obsolete build steps.

* Thu Feb 28 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 20071212-8
- Rebuild for cln soname bump

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 20071212-7
- Autorebuild for GCC 4.3

* Wed Jan  2 2008 Quentin Spencer <qspencer@users.sf.net> 20071212-6
- Rebuild for libdap API change.

* Wed Dec 26 2007 Quentin Spencer <qspencer@users.sf.net> 20071212-5
- Rebuild for octave 3.0.0. Remove edit.m because it's now in octave.

* Thu Dec 20 2007 Quentin Spencer <qspencer@users.sf.net> 20071212-4
- I give up. Disable parallel build.

* Thu Dec 20 2007 Quentin Spencer <qspencer@users.sf.net> 20071212-3
- Try the patch again.

* Thu Dec 20 2007 Quentin Spencer <qspencer@users.sf.net> 20071212-2
- Add patch to fix parallel build of odepkg and optiminterp (again).

* Wed Dec 12 2007 Quentin Spencer <qspencer@users.sf.net> 20071212-1
- New release. Remove old patches that are now in sources.
- Update package description (some functions mentioned are now in octave).

* Wed Dec  5 2007 Quentin Spencer <qspencer@users.sf.net> 20071014-5
- Rebuild for new octave

* Sat Dec  1 2007 Alex Lancaster <alexlan@fedoraproject.org> 20071014-4
- Rebuild for new octave

* Wed Nov  7 2007 Quentin Spencer <qspencer@users.sf.net> 20071014-3
- Add new patch to listen.cc for compatibility with octave-2.9.16

* Tue Oct 16 2007 Orion Poplawski <orion@cora.nwra.com>  20071014-2
- Add patch to fix parallel build of odepkg and optiminterp

* Tue Oct 16 2007 Orion Poplawski <orion@cora.nwra.com>  20071014-1
- Rewrite to handle new "bundle" method to releasing packages and
  new octave package manager
- Prepare for eventual splitting of the package with provides

* Mon Sep 24 2007 Jesse Keating <jkeating@redhat.com> - 2006.07.09-10
- Rebuild for new octave

* Tue Feb 20 2007 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-9
- Remove libtermcap-devel as build dependency (Bug 226768).
- Change octave version dependency to octave(api) dependency,
  which is now provided by the octave package.

* Mon Nov 06 2006 Jindrich Novy <jnovy@redhat.com> 2006.07.09-8
- rebuild against the new curl

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 2006.07.09-7
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sat Sep 23 2006 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-6
- Rebuild for updated libdap.

* Fri Sep 15 2006 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-5
- Rebuild for FC6.

* Fri Aug 25 2006 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-4
- New build for octave 2.9.8.
- Patch bug in imread.m
- Patch LOADPATH bug.
- Fix configure command so that m files containing paths are
  correctly generated.

* Tue Jul 11 2006 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-3
- New build for octave 2.9.7.
- Disable mex related functions (they are in octave now).

* Tue Jul 11 2006 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-2
- Patch legend.m.

* Mon Jul 10 2006 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-1
- New release. Old patches and associated specfile cruft removed.

* Wed May  3 2006 Quentin Spencer <qspencer@users.sf.net> 2006.03.17-4
- Bug fix for #190481

* Thu Apr 27 2006 Quentin Spencer <qspencer@users.sf.net> 2006.03.17-3
- Add fixes for octcdf (from the author), which changes the dependency
  from netcdf to libnc-dap. (This requires autoconf temporarily.)

* Wed Apr 19 2006 Quentin Spencer <qspencer@users.sf.net> 2006.03.17-2
- New release for octave 2.9.5.
- Patch added for incompatibilities between octave 2.9.4 and 2.9.5.

* Fri Mar 17 2006 Quentin Spencer <qspencer@users.sf.net> 2006.03.17-1
- New release. Remove old patches.

* Sat Feb 18 2006 Quentin Spencer <qspencer@users.sf.net> 2006.01.28-5
- Amend patch0 to correctly deal with 64-bit indexing.

* Thu Feb 16 2006 Quentin Spencer <qspencer@users.sf.net> 2006.01.28-4
- Patch the fixed point code so that g++ 4.1 compiles it.

* Fri Feb  3 2006 Quentin Spencer <qspencer@users.sf.net> 2006.01.28-3
- Fix permissions on octlink.sh and add more to the patch.

* Fri Feb  3 2006 Quentin Spencer <qspencer@users.sf.net> 2006.01.28-2
- Add new build dependencies on ImageMagick-c++-devel and netcdf-devel.
  (The ImageMagick-c++-devel indirectly brings in the necessary
  modular X devel modules, such as libXt-devel and others).
- Define CPPFLAGS so it finds the netcdf headers.

* Fri Feb  3 2006 Quentin Spencer <qspencer@users.sf.net> 2006.01.28-1
- New upstream release.
- Patch so it will build correctly with octave 2.9.x.
- Change installation paths so they now depend on the octave API version
  rather than the octave version, which will make updates less frequent.

* Wed Nov  2 2005 Quentin Spencer <qspencer@users.sf.net> 2005.06.13-5
- Rebuild for new versions of ginac and cln.
- Query octave to get octave version dependency.

* Wed Aug  3 2005 Quentin Spencer <qspencer@users.sf.net> 2005.06.13-4
- Hardcode the octave version dependency. Using rpm to query for this
  information was producing wrong results on the new build system.

* Wed Aug  3 2005 Quentin Spencer <qspencer@users.sf.net> 2005.06.13-3
- Remove some BuildRequires that are now dependencies of octave-devel.

* Tue Aug  2 2005 Quentin Spencer <qspencer@users.sf.net> 2005.06.13-2
- Change GiNaC-devel to ginac-devel to reflect package name change.

* Fri Jun 17 2005 Quentin Spencer <qspencer@users.sf.net> 2005.06.13-1
- New upstream release. Now requires pcre-devel to build.
- Corrected instructions on creating patched source tarball.
- Remove explicit BuildRequires for c++ compiler and libs
  (not needed and causes build failure in the build system for x86_64).
- Add patch for problem with main/plot/legend.m
- Add fftw3-devel to BuildRequires.

* Sat Jun 11 2005 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-7
- Cleanup of unneeded things in build section

* Mon Apr 25 2005 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-7
- Changed license (some functions are GPL, BSD, and public domain,
  so the collection is licensed as public domain).
- Moved ugly path hacks from build to install so that RPM_BUILD_ROOT
  doesn't end up in the code (which it did before).
- Replaced upstream tarball with patched version that removed GPL
  incompatible code.

* Thu Apr 21 2005 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-6
- Added GiNaC-devel BuildRequires

* Tue Mar 29 2005 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-5
- Rebuild for octave-2.1.69

* Mon Mar 28 2005 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-4
- Rebuild for octave-2.1.68

* Thu Feb 24 2005 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-3
- Updated spec file to get octave version at build time.

* Wed Nov 17 2004 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-2
- Revised package description.

* Tue Jun 15 2004 Quentin Spencer <qspencer@users.sf.net>
- Added qhull support.

* Tue Feb  4 2003 Quentin Spencer <qspencer@users.sf.net>
- First Version, loosely based on Red Hat's spec file for octave.
