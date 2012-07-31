Summary: The LAM (Local Area Multicomputer) programming environment.
Name: lam
Version: 7.1.2
Release: 14%{?dist}
License: BSD
Epoch: 2
Group: Development/Libraries
Source: lam-%{version}-rh1.tar.bz2
Source1: lam.pc.in
Source2: lam.module.in
Source3: lam.sh.in
Source4: lam.csh.in
Patch0: lam-7.1.2-no_darwin.patch
Patch1: lam-7.1.2-archinc.patch
URL: http://www.lam-mpi.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: perl gcc gcc-c++ gcc-gfortran libaio libaio-devel autoconf automake libtool
Requires: openssh-server openssh-clients
Requires: %{name}-libs = %{epoch}:%{version}-%{release}

%description 
LAM (Local Area Multicomputer) is an Message-Passing Interface (MPI)
programming environment and development system for heterogeneous
computers on a network. With LAM/MPI, a dedicated cluster or an
existing network computing infrastructure can act as one parallel
computer to solve one problem. LAM/MPI is considered to be "cluster
friendly" because it offers daemon-based process startup/control as
well as fast client-to-client message passing protocols. LAM/MPI can
use TCP/IP and/or shared memory for message passing (different RPMs
are supplied for this -- see the main LAM website at
http://www.mpi.nd.edu/lam/ for details).<

LAM features a full implementation of MPI version 1 (with the
exception that LAM does not support cancelling of sends), and much of
version 2. Compliant applications are source code portable between LAM
and any other implementation of MPI. In addition to meeting the
standard, LAM/MPI offers extensive monitoring capabilities to support
debugging. Monitoring happens on two levels: On one level, LAM/MPI has
the hooks to allow a snapshot of a process and message status to be
taken at any time during an application run. The status includes all
aspects of synchronization plus datatype map/signature, communicator
group membership and message contents (see the XMPI application on the
main LAM website). On the second level, the MPI library can produce a
cumulative record of communication, which can be visualized either at
runtime or post-mortem.

%package libs
Summary:        Libraries for LAM
Group:          System/Libraries
Requires(post):  mpi-selector, /usr/sbin/alternatives
Requires(preun): mpi-selector

%description libs
Runtime libraries for LAM

%package devel
Summary:        Development files for LAM
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:	libaio-devel gcc gcc-c++ gcc-gfortran

%description devel
Contains development headers and libraries for LAM

%prep
%setup -q -n lam-%{version}-rh1
%patch0 -p1 -b .no_darwin
%patch1 -p1 -b .archinc

%build
%ifarch x86_64
CFLAGS="$RPM_OPT_FLAGS -fPIC"
CXXFLAGS="$RPM_OPT_FLAGS -fPIC"
FFLAGS="$RPM_OPT_FLAGS -fPIC"
%endif 

%ifarch i386 ppc
%define mode 32
%else
  %ifarch s390
  %define mode 31
  %else
  %define mode 64
  %endif
%endif

export CPPFLAGS="-DLAM_MODE=\\\"%{mode}\\\""
export FC=f95
%ifarch i386 s390 ppc
./configure --with-rsh="/usr/bin/ssh -x -a" --prefix=%{_libdir}/%{name} --libdir=%{_libdir}/%{name}/lib --with-trillium --enable-shared --disable-deprecated-names
%else
#
# Disable TotalView on non-32 bit architectures.
#
./configure --with-rsh="/usr/bin/ssh -x -a" --prefix=%{_libdir}/%{name} --libdir=%{_libdir}/%{name}/lib --disable-tv --disable-tv-dll --with-trillium --enable-shared --disable-deprecated-names
%endif

make %{?_smp_mflags} all

%install
[ ! -z "${RPM_BUILD_ROOT}" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

# rm some doc files that install put in the wrong place
rm -fr ${RPM_BUILD_ROOT}%{_libdir}/%{name}/share

# links we use to reference files in doc macros in the files section
ln -f romio/COPYRIGHT romio/ROMIO-COPYRIGHT
ln -f romio/doc/README romio/ROMIO-README
ln -f romio/doc/users-guide.ps.gz romio/doc/romio-users-guide.ps.gz 
ln -f romio/README_LAM romio/ROMIO-README_LAM

# Remove .la files:
find ${RPM_BUILD_ROOT}%{_libdir} -name \*.la | xargs rm

# Create the lam.pc, pkgconfig, and mpivars files
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
sed 's#@VERSION@#'%{version}'#g;s#@MPIDIR@#'%{_libdir}/%{name}'#g' < %SOURCE1 > ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/%{name}.pc
sed 's#@MPIDIR@#'%{_libdir}/%{name}'#g' < %SOURCE2 > ${RPM_BUILD_ROOT}%{_libdir}/%{name}/lib/%{name}.module
sed 's#@MPIDIR@#'%{_libdir}/%{name}'#g' < %SOURCE3 > ${RPM_BUILD_ROOT}%{_libdir}/%{name}/etc/mpivars.sh
sed 's#@MPIDIR@#'%{_libdir}/%{name}'#g' < %SOURCE4 > ${RPM_BUILD_ROOT}%{_libdir}/%{name}/etc/mpivars.csh

%clean
[ ! -z "${RPM_BUILD_ROOT}" ] && rm -rf ${RPM_BUILD_ROOT}

%post
# In order to work when upgrading from older packages that used alternatives
# instead, we will need to forcably remove all the old incarnations of the
# alternatives support, and then install our mpi-selector support.

# We never used anything other than lamrun for the mpi-run link
/usr/sbin/alternatives --remove mpi-run /usr/bin/lamrun 2&>/dev/null

# but, we used lamcc, and then later lamcc-mode for mpicc....this little
# grep/awk thing catches all of them that might still be installed
/usr/sbin/alternatives --display mpicc | grep priority | grep lamcc | awk '{ system("/usr/sbin/alternatives --remove mpicc "$1) }'

# ditto for possible variants of mpilibs and mpilibs%{mode}
for i in mpilibs mpilibs%{mode}; do /usr/sbin/alternatives --display $i | grep priority | grep lam | awk '{ system("/usr/sbin/alternatives --remove '$i' "$1) }'; done

# OK, we've removed all the old alternatives configurations, now we can add
# the new mpi-selector configuration for this install.  It's safe to redo
# the add on each install/upgrade, they just reinstall in place if they
# already exist
mpi-selector --register %{name}-%{_arch} --source-dir %{_libdir}/%{name}/etc --yes 2&>/dev/null || /bin/true

%preun
if [ $1 -eq 0 ]; then
    mpi-selector --unregister %{name}-%{_arch} --yes 2&>/dev/null || /bin/true
fi

%files
%defattr(-,root,root,-)
%dir %{_libdir}/%{name}/etc
%dir %{_libdir}/%{name}/bin
%dir %{_libdir}/%{name}/man
%config(noreplace) %{_libdir}/%{name}/etc/*
%{_libdir}/%{name}/bin/*
%exclude %{_libdir}/%{name}/bin/mpic*
%exclude %{_libdir}/%{name}/bin/mpiC*
%exclude %{_libdir}/%{name}/bin/mpif*
%{_libdir}/%{name}/man/man1/*
%exclude %{_libdir}/%{name}/man/man1/mpic*
%exclude %{_libdir}/%{name}/man/man1/mpiC*
%exclude %{_libdir}/%{name}/man/man1/mpif*
%{_libdir}/%{name}/man/man5/*
%{_libdir}/%{name}/man/man7/*
%{_libdir}/%{name}/man/mans/*

%files libs
%defattr(-,root,root,-)
%doc LICENSE HISTORY INSTALL README AUTHORS
%doc doc/user.pdf doc/install.pdf
%doc share/memory/ptmalloc/ptmalloc-COPYRIGHT share/memory/ptmalloc2/ptmalloc2-COPYRIGHT
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/lib
%{_libdir}/%{name}/lib/*.so.*
%ifarch i386 s390 ppc
# TotalView modules
%dir %{_libdir}/%{name}/lib/lam
%{_libdir}/%{name}/lib/lam/*.so*
%endif

%files devel
%defattr(-,root,root,-)
%doc romio/ROMIO-COPYRIGHT romio/ROMIO-README romio/ROMIO-README_LAM  romio/doc/romio-users-guide.ps.gz
%{_libdir}/%{name}/bin/mpic*
%{_libdir}/%{name}/bin/mpiC*
%{_libdir}/%{name}/bin/mpif*
%{_libdir}/%{name}/man/man1/mpic*
%{_libdir}/%{name}/man/man1/mpiC*
%{_libdir}/%{name}/man/man1/mpif*
%{_libdir}/%{name}/man/man2/*
%{_libdir}/%{name}/man/man3/*
%dir %{_libdir}/%{name}/include
%{_libdir}/%{name}/include/*
%{_libdir}/%{name}/lib/*.a
%{_libdir}/%{name}/lib/*.so
%{_libdir}/%{name}/lib/lam.module
%ifarch i386 s390 ppc
# TotalView modules
%{_libdir}/%{name}/lib/lam/*.so
%endif
%config %{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Apr 03 2008 Doug Ledford <dledford@redhat.com> - 2:7.1.2-14
- Oops, I had the post/preun scripts attached to the -libs packages, while
  the mpivars.* files mpi-selector needed was installed in the base
  package.  This presented a race condition where the mpivars.* files might
  or might not be present by the time the post script ran.  We attach to the
  right package now.
- Resolves: bz440397
- Related: bz428199

* Wed Apr 02 2008 Doug Ledford <dledford@redhat.com> - 2:7.1.2-12
- Convert over to use mpi-selector and resolve the alternatives links
  issue once and for all
- Related: bz428199

* Tue Feb 12 2008 Doug Ledford <dledford@redhat.com> - 2:7.1.2-11
- On upgrade we loose our alternatives links.  This is because of a bug in
  the previous lam package.  Correct our pre/post scripts so the bug will
  no longer exist, but it will require running upgrade twice in order to
  recreate the missing alternatives links.

* Thu May 17 2007 Doug Ledford <dledford@redhat.com> - 2:7.1.2-10
- Fix the sed substitutions to be global so they catch all the items
  that need to be substituted
- RESOLVES: bz240457

* Thu Mar 22 2007 Florian La Roche <laroche@redhat.com> - 2:7.1.2-9
- add alternatives to some more deps

* Fri Oct 13 2006 Doug Ledford <dledford@redhat.com> - 2:7.1.2-8
- @!#^!@ copy-n-paste error...fix up incorrect priority so alternatives will
  work again

* Wed Oct 11 2006 Doug Ledford <dledford@redhat.com> - 2:7.1.2-6
- Fix alternatives setup of mpi.conf in /etc/ld.so.conf.d so we find both
  sets of libs on multilib arches

* Sun Oct 08 2006 Doug Ledford <dledford@redhat.com> - 2:7.1.2-5
- Add s390x into the mode/priority config list

* Tue Oct 03 2006 Doug Ledford <dledford@redhat.com> - 2:7.1.2-4
- Remove Apple Public Source License licensed files from the tarball (they
  aren't used anyway since we aren't the Darwin OS, but the license language
  is problematic for people distributing the files regardless) (bz205998)
- Fix up file conflicts for lam_build_info.h and lam_config.h (bz205218)

* Sun Aug 27 2006 Doug Ledford <dledford@redhat.com> - 2:7.1.2-3
- Make the %post and %preun only run at the right times (new install and
  final package removal)

* Fri Aug 25 2006 Doug Ledford <dledford@redhat.com> - 2:7.1.2-2
- Get rid of mpi_alternatives and just use alternatives to match openmpi

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:7.1.2-1.fc6.1
- rebuild

* Mon Jun 12 2006 Jason Vas Dias<jvdias@redhat.com> - 2:7.1.2-1.fc6
- Upgrade to upstream version 7.1.2
- fix bug 191433 - Split into -libs and -devel packages
  ( apply .spec file patch from Orion Poplawski <orion@cora.nwra.com> )
- fix bug 194747 - fix BuildRequires for mock

* Tue Feb 21 2006 Jason Vas Dias<jvdias@redhat.com> - 2:7.1.1-11
- ld.so.conf.d/mpi.conf integration with openmpi

* Thu Feb 16 2006 Jason Vas Dias<jvdias@redhat.com> - 2:7.1.1-10.FC5
- Enable co-existence with OpenMPI

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2:7.1.1-8.FC5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jason Vas Dias <jvdias@redhat.com> - 2:7.1.1-8.2
- rebuild for new gcc, glibc, glibc-kernheaders

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 15 2005 Jason Vas Dias <jvdias@redhat.com> - 2:7.1.1-8
- Rebuild for FC-5

* Tue Aug 02 2005 Jason Vas Dias <jvdias@redhat.com> - 2:7.1.1-7
- fix bug 164898: 7.0.6's '--enable-trillium' -> 7.1.1's '--with-trillium'

* Fri Jul 08 2005 Jason Vas Dias <jvdias@redhat.com> - 2:7.1.1-6
- fix bug 161028
- build for FC4 updates

* Mon Jun 27 2005 Tom "spot" Callaway <tcallawa@redhat.com> - 2:7.1.1-5
- enable shared libraries
- don't list %{_datadir}/* in files

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2:7.1.1-4
- use -fPIC on x86_64 (reported by spot to get things building for Extras)

* Tue Mar 08 2005 Jason Vas Dias <jvdias@redhat.com>
- add test for f95 to configure

* Mon Mar 07 2005 Florian La Roche <laroche@redhat.com>
- require gcc-gfortran instead of gcc-g77

* Tue Feb 01 2005 Jason Vas Dias <jvdias@redhat.com>
- Upgraded to version 7.1.1 ; fixed bug 126824 .

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 10 2004 Lon Hohberger <lhh@redhat.com> 7.0.6-2
- Build for correct libaio deps.

* Wed Jun 09 2004 Lon Hohberger <lhh@redhat.com> 7.0.6-1
- Really re-enable C++; import 7.0.6 from upstream

* Thu Apr 15 2004 Lon Hohberger <lhh@redhat.com> 7.0.3-6.4
- Rebuild for libaio deps.

* Mon Apr 05 2004 Lon Hohberger <lhh@redhat.com> 7.0.3-6.3
- Fix RPM build on x86-64

* Mon Apr 05 2004 Lon Hohberger <lhh@redhat.com> 7.0.3-6.2
- Remove .debug from main RPM; users wishing to use TotalView
will need to install the -debuginfo RPM. (#119523)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec 09 2003 Lon Hohberger <lhh@redhat.com> 7.0.3-5
- Rebuild

* Fri Dec 05 2003 Lon Hohberger <lhh@redhat.com> 7.0.3-4
- Enable Trillium support.

* Tue Dec 02 2003 Lon Hohberger <lhh@redhat.com> 7.0.3-3
- Import 7.0.3 from upstream.  Re-enable C++ (#91790) and ROMIO.
- Remove lam.sh and lam.csh environment settings during
installation (#111238).
- Remove deprecated/unnecessary symlinking.
- Preserve .debug info for things which need the debugging
information (eg, TotalView) on appropriate platforms (eg,
32-bit platforms).  According to the configure.in file for
TotalView, it only really works on 32-bit platforms at
the moment.
- Removed --with-rpi=usysv; it's now a runtime option.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 15 2003 Lon Hohberger <lhh@redhat.com> 6.5.9-2
- Rebuilt

* Tue Mar 25 2003 Lon Hohberger <lhh@redhat.com> 6.5.9-1
- Import of 6.5.9 from upstream

* Mon Mar 10 2003 Lon Hohberger <lhh@redhat.com> 6.5.8-5
- Enabled s390[x]

* Fri Feb 7 2003 Lon Hohberger <lhh@redhat.com> 6.5.8-4
- Disabled s390 and s390x architectures for now.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Bill Nottingham <notting@redhat.com> 2:6.5.8-2
- rebuild, shrink

* Fri Dec 20 2002 Elliot Lee <sopwith@redhat.com> 2:6.5.8-1
- Update to new version in hopes of a fix for varargs problems
- Since it doesn't fix it, turn off mpi2c++ altogether - a package
  that builds without C++ wrappers is preferable to a package that doesn't
  build at all

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 2:6.5.6-10
- remove unpackaged files from the buildroot

* Wed Nov 20 2002 Jakub Jelinek <jakub@redhat.com> 6.5.6-9
- Always #include <errno.h> instead of declaring errno by hand.
- Start tweaking for Hammer
- Remove unpackaged files

* Thu Jul 18 2002 Trond Eivind Glomsrød <teg@redhat.com> 6.5.6-8
- Fix  #63548

* Thu Jun 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 6.5.6-7
- Remove malplaced and malformatted manpage (#67955). 
- Fix hpf77. A wrapper was a little to zealous in avoiding
 /usr for includes and libs (#67321)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 6.5.6-4
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Dec  4 2001 Trond Eivind Glomsrød <teg@redhat.com> 6.5.6-2
- use ssh (#56946)

* Tue Nov 27 2001 Trond Eivind Glomsrød <teg@redhat.com> 6.5.6-1
- 6.5.6

* Fri Nov  2 2001 Trond Eivind Glomsrød <teg@redhat.com> 6.5.5-1
- 6.5.5
- License change - from a  BSDish license to BSD

* Fri Aug 17 2001 Trond Eivind Glomsrød <teg@redhat.com> 6.5.4-1
- 6.5.4, from the stable branch. Minor bugfixes, more docs. This also
  made allmost all references to the buildroot go away.
- fix the remaining reference
- Don't include examples as they are too tied with the buildroot.
- Add perl and file-utils as build dependencies
- don't include doc/* as documentation, that directory disappeared a
  long time ago (rpm doesn't fail if something in the doc section is
  missing )

* Mon Jul 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 6.5.3
- remove now obsolete patches and workarounds during the build process

* Fri May 25 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 6.5.2
- No longer exclude IA64

* Sat Apr  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Fix from CVS so hpc and hf77 (C++ and FORTRAN compiler interfaces) 
  don't specify -I/usr/include - this breaks some compilations of MPI
  programs (#34796)

* Wed Apr  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 6.5.1 final
- update URL
- add epoch, as rpm thought 6.5.1 newer than 6.5b7 newer 
  than  6.5.1 etc.

* Tue Mar 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 6.5b7
- fix lamhelpdir problems

* Fri Mar  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 6.5b5 - this is just a renaming of the 6.3.3b series,
  and should hopefully be indentical to 6.5 final

* Mon Feb 12 2001 Trond Eivind Glomsrød <teg@redhat.com>
- make a link from mpi++.h, not mpi++, to mpi2c++/mpi++.h
  (#27249)
- 6.3.3b58, which should work better on SMP machines in
  a cluster

* Tue Nov 28 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 6.3.3b47

* Thu Aug 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 6.3.3b28, which should match the release. One known
  problem on SCO, otherwise none. This includes 
  fixing some programs which didn't work in the 
  last build.
 
* Thu Jul 27 2000 Harald Hoyer <harald@redhat.com>
- fixed the install process, that the lam tools have the
  right path set. make all;make DESTDIR install is 
  our friend.

* Wed Jul 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- a new and better world without dirty tricks necesarry. 
  All hail the 6.3.3beta (beta 20 - all my requests and 
  patches seem to be in now :)

* Fri Jun 16 2000 Trond Eivind Glomsrød <teg@redhat.com>
- substituted some old dirty tricks for new ones to make
  it build. More needed.
- Removed C++ (won't build) and ROMIO (who cares) support

* Thu Jun 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- ugly tricks to make it use %%{_mandir}
- patch to make it build with current compiler and glibc
- don't build on IA64

* Tue Apr 25 2000 Trond Eivind Glomsrød <teg@redhat.com>
- changed RPI to usysv - this should be good for
  (clusters of) SMPs.

* Wed Mar 28 2000 Harald Hoyer <harald@redhat.com>
- patched scheme Makefile

* Tue Mar 28 2000 Harald Hoyer <harald@redhat.com>
- new subminor version
- patched Makefile to build otb daemons, to satisfy conf.otb and build all
  stuff

* Sat Mar 04 2000 Cristian Gafton <gafton@redhat.com>
- fixed the whole tree the hard way - get into each Makefile and fix
  brokeness on a case by case basis. Traces of Buildroot should be 
  erradicated by now.

* Thu Mar 02 2000 Cristian Gafton <gafton@redhat.com>
- put back the mpi2c++ stuff. 

* Tue Feb 29 2000 Cristian Gafton <gafton@redhat.com>
- take out the mpi2c++ in a separate package

* Fri Feb 04 2000 Cristian Gafton <gafton@redhat.com>
- first version of the package
