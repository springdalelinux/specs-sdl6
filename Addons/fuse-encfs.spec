Name:		fuse-encfs
Version:	1.7.4
Release:	1%{?dist}
Summary:	Encrypted pass-thru filesystem in userspace
License:	GPLv3+
Group:		System Environment/Kernel
Url:		http://www.arg0.net/encfs
Source0:	http://encfs.googlecode.com/files/encfs-%{version}.tgz
Source1:	http://encfs.googlecode.com/files/encfs-%{version}.tgz.asc
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	fuse >= 2.6
Provides:	encfs = %{version}-%{release}
BuildRequires:	rlog-devel >= 1.3
BuildRequires:	openssl-devel
BuildRequires:	boost-devel >= 1.34
BuildRequires:	fuse-devel >= 2.6
BuildRequires:	gettext

%description
EncFS implements an encrypted filesystem in userspace using FUSE.  FUSE
provides a Linux kernel module which allows virtual filesystems to be written
in userspace.  EncFS encrypts all data and filenames in the filesystem and
passes access through to the underlying filesystem.  Similar to CFS except that
it does not use NFS.

%prep
%setup -q -n encfs-%{version}

%build
%configure --disable-static --with-boost-libdir=%{_libdir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}/%{_libdir}/*.so
%find_lang encfs

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -f encfs.lang
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/*
%{_libdir}/libencfs.so*
%{_mandir}/man1/*

%changelog
* Mon Apr 11 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.7.4-1
- Ver. 1.7.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Thomas Spura <tomspur@fedoraproject.org> - 1.7.2-2
- rebuild for new boost

* Tue Sep  7 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.7.2-1
- Ver. 1.7.2

* Sun Sep  5 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.7.1-1
- Fixed three security flaws (see rhbz #630460)
- Cleaned up spec-file a little

* Sun Aug 01 2010 Josh Kayse <jokajak@fedoraproject.org> - 1.6.1-1
- update to 1.6-1
- remove patch because it's been incorporated

* Thu Jul 29 2010 Bill Nottingham <notting@redhat.com> - 1.5-13
- Rebuild for boost-1.44

* Tue Jul 27 2010 Bill Nottingham <notting@redhat.com> - 1.5-12
- Rebuild for boost-1.44

* Fri Jan 22 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 1.5.11
- Rebuild for Boost soname bump

* Sat Oct 17 2009 Peter Lemenkov <lemenkov@gmail.com> 1.5-10
- Added version in Requires for boost-devel

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> 1.5-9
- rebuilt with new fuse

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.5-8
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 03 2009 Caolán McNamara <caolanm@redhat.com> - 1.5-6
- constify ret of strchr(const char*)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> 1.5-4
- rebuild with new openssl

* Tue Dec 30 2008 Peter Lemenkov <lemenkov@gmail.com> 1.5-3
- Fixed URL

* Thu Dec 18 2008 Petr Machata <pmachata@redhat.com> - 1.5-2
- Rebuild with new boost

* Sun Oct 26 2008 Peter Lemenkov <lemenkov@gmail.com> 1.5-1
- Ver. 1.5
- Dropped upstreamed patches

* Tue Aug 12 2008 Peter Lemenkov <lemenkov@gmail.com> 1.4.2-5
- Rebuild with new boost

* Fri Aug  1 2008 Peter Lemenkov <lemenkov@gmail.com> 1.4.2-4
- Fix build with new rlog

* Sat Jul 12 2008 Peter Lemenkov <lemenkov@gmail.com> 1.4.2-3
- rebuild due to rlog soname bump

* Mon May  5 2008 Tomas Hoger <thoger@redhat.com> - 1.4.2-2
- Work-around broken boost library path auto detection causing build failures
  on 64-bit architectures.

* Mon Apr 14 2008 Peter Lemenkov <lemenkov@gmail.com> 1.4.2-1
- Ver. 1.4.2
- add option to pass-through file 'holes'.  Only available in expert mode
- config file format changed to XML via boost serialization
	(config file is now .encfs6.xml)
- remove ulockmgr support, caused numerous locking issues. (bz# 440483)
- fix symlink handling in encfsctl export
- fix stdinpass option parsing, reported by Scott Hendrickson
- fix path suffix in encfsctl

* Fri Mar 28 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.4.1.1-5
- Update patch for building with GCC 4.3 (use <cstring> throughout)

* Tue Mar 25 2008 Peter Lemenkov <lemenkov@gmail.com> 1.4.1.1-4.1
- Another attempt to fix GCC 4.3 builds

* Tue Mar 25 2008 Peter Lemenkov <lemenkov@gmail.com> 1.4.1.1-4
- Another attempt to fix GCC 4.3 builds

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.1.1-3
- Autorebuild for GCC 4.3

* Sat Feb  9 2008 Peter Lemenkov <lemenkov@gmail.com> 1.4.1.1-2
- Rebuild for GCC 4.3

* Wed Jan 23 2008 Peter Lemenkov <lemenkov@gmail.com> 1.4.1.1-1
- Ver. 1.4.1.1
- Changed License tag according to Fedora policy
- Added new BR - boost-devel
- Proper locale handling
- Some other cosmetic changes

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.3.2-2
- Rebuild for deps

* Thu Apr 12 2007 Peter Lemenkov <lemenkov@gmail.com> 1.3.2-1
- Version 1.3.2

* Tue Sep 12 2006 Peter Lemenkov <lemenkov@gmail.com> 1.3.1-3%{?dist}
- Rebuild for FC6

* Sat Aug 26 2006 Peter Lemenkov <lemenkov@newmail.ru> 1.3.1-2%{?dist}
- Added necessary 'requires'field

* Wed May 03 2006 Peter Lemenkov <lemenkov@newmail.ru> 1.3.1-1%{?dist}
- Version 1.3.1

* Thu Mar 30 2006 Peter Lemenkov <lemenkov@newmail.ru> 1.3.0-1%{?dist}
- Version 1.3.0

* Fri Dec 16 2005 Peter Lemenkov <lemenkov@newmail.ru> 1.2.5-1
- Initial build for FE

* Fri Nov 11 2005 Valient Gough <vgough@pobox.com>
- Release 1.2.5
- Fix race condition when using newer versions of GCC.  Fixes problem reported
  by Chris at x.nu.
- add encfssh script, thanks to David Rosenstrauch
* Fri Aug 26 2005 Valient Gough <vgough@pobox.com>
- Release 1.2.4
- fix segfault if small invalid filenames were encountered in the encrypted
  directory, reported by paulgfx.
- try and detect if user tries to mount the filesystem over the top of the
  encrypted directory, problem reported by paulgfx.
- environment variable ENCFS5_CONFIG can be used to override the location of
  the .encfs5 configuration file.
- add encfsctl 'export' command, patch from Janne Hellsten
  
* Tue Apr 19 2005 Valient Gough <vgough@pobox.com>
- Release 1.2.1
- add --public mount option
- add --stdinpass option to read password from stdin for scripting
- import latest rosetta translation updates

* Thu Feb 10 2005 Valient Gough <vgough@pobox.com>
- Release 1.2.0
- Fix bug with MAC headers and files > 2GB, reported by Damian Frank
- Fix bug with external password interface which could result in problems
  communicating with external password program.  Found by Olivier Dournaux.
- Switch to FUSE 2.2 API -- support for FUSE 1.x has been dropped.
- Add support for inode numbering pass-thru (when used 'use_ino' option to
  fuse).  This allows encoded filesystem to use the same inode numbers as the
  underlying filesystem.

* Wed Jan 12 2005 Valient Gough <vgough@pobox.com>
- Release 1.1.11
- add internationalization support.  Thanks to lots of contributors, there are
  translations for serveral languages.
- added workaround for libfuse mount failure with FUSE 1.4
- fix compile failure with FUSE 1.4

* Mon Nov 8 2004 Valient Gough <vgough@pobox.com>
- Release 1.1.10
- fix problems with recursive rename
- fix incorrect error codes from xattr functions

* Tue Aug 15 2004 Valient Gough <vgough@pobox.com>
- Release 1.1.9
- fix another rename bug (affected filesystems with 'paranoia' configuration)

* Mon Aug 14 2004 Valient Gough <vgough@pobox.com>
- Release 1.1.8
- Improve MAC block header processing.

* Sat Aug 12 2004 Valient Gough <vgough@pobox.com>
- Release 1.1.7
- fix bug in truncate() for unopened files.

* Mon Aug 9 2004 Valient Gough <vgough@pobox.com>
- Release 1.1.6
- fix header IV creation when truncate() used to create files.
- add support for IV chaining to old 0.x filesystem support code (useful for
  systems with old OpenSSL, like RedHat 7.x).

* Tue Jul 22 2004 Valient Gough <vgough@pobox.com>
- Release 1.1.5

* Sat Jul 10 2004 Valient Gough <vgough@pobox.com>
- Release 1.1.4
- add external password prompt support.

* Thu Jun 24 2004 Valient Gough <vgough@pobox.com>
- Release 1.1.3

* Fri May 28 2004 Valient Gough <vgough@pobox.com>
- Release 1.1.2
- Fix bug affecting filesystems with small empty directories (like XFS)
- Updates to recursive rename code to undo all changes on failure.
- Fix OpenSSL dependency path inclusion in build.

* Wed May 19 2004 Valient Gough <vgough@pobox.com>
- Release 1.1.1
- Fix MAC header memory size allocation error.
- Add file rename-while-open support needed for Evolution.

* Thu May 13 2004 Valient Gough <vgough@pobox.com>
- Second release candidate for version 1.1
- Add support for block mode filename encryption.
- Add support for per-file initialization vectors.
- Add support for directory IV chaining for per-directory initialization
  vectors.
- Add support for per-block MAC headers for file contents.
- Backward compatibility support dropped for filesystems created by version
  0.x.  Maintains backward compatible support for versions 1.0.x.

* Sun Apr 4 2004 Valient Gough <vgough@pobox.com>
- Release 1.0.5
- Allow truncate call to extend file (only shrinking was supported)

* Fri Mar 26 2004 Valient Gough <vgough@pobox.com>
- Release 1.0.4
- Large speed improvement.
- Add support for FUSE major version 2 API.

* Thu Mar 18 2004 Valient Gough <vgough@pobox.com>
- Release 1.0.3
- Fix bugs in truncation and padding code.

* Sat Mar 13 2004 Valient Gough <vgough@pobox.com>
- Release 1.0.2
- Use pkg-config to check for OpenSSL and RLog build settings
- Add support for '--' argument to encfs to pass arbitrary options to FUSE /
  fusermount.
- Add man pages.

* Tue Mar 2 2004 Valient Gough <vgough@pobox.com>
- Release 1.0.1
- Fix problem with using OpenSSL's EVP_BytesToKey function with variable
  key length ciphers like Blowfish, as it would only generate 128 bit keys.
- Some configure script changes to make it possible to use --with-extra-include
  configure option to pick up any necessary directories for OpenSSL.

* Fri Feb 27 2004 Valient Gough <vgough@pobox.com>
- Release 1.0
- Added some pre-defined configuration options at startup to make filesystem
  creation a bit more user friendly.

* Mon Feb 23 2004 Valient Gough <vgough@pobox.com>
- Merge development branch to mainline.  Source modularized to make it easier
  to support different algorithms.
- Added encfsctl program which can show information about an encrypted
  directory and can change the user password used to store the volume key.
- Added support for AES and BlowFish with user specified keys and block sizes
  (when building with OpenSSL >= 0.9.7).
- Backward compatible with old format, but new filesystems store configuration
  information in a new format which is not readable by old encfs versions.

* Sat Feb 7 2004 Valient Gough <vgough@pobox.com>
- Improved performance by fixing cache bug which caused cached data to not be
  used as often as it could have been.  Random seek performance improved by
  600% according to Bonnie++ benchmark.
- Fixed bugs preventing files larger then 2GB.  Limit should now be around
  128GB (untested - I don't have that much drive space).  > 2GB also requires
  recent version of FUSE module (from Feb 6 or later) and an underlying
  filesystem which supports large files.
- Release 0.6

