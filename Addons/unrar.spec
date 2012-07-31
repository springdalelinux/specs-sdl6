Name:           unrar
Version:        3.9.10
Release:        3%{?dist}
Summary:        Utility for extracting, testing and viewing RAR archives
License:        Freeware with further limitations
Group:          Applications/Archiving
URL:            http://www.rarlab.com/rar_archiver.htm
Source0:        http://www.rarlab.com/rar/unrarsrc-%{version}.tar.gz
# Patch to resolve issues noted in #1385:
Patch0:	   	unrar-3.9.10-missing-recvol-symbols.patch
# Debian patch for man page:
Patch1:         unrar-nonfree_3.8.5-2.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): chkconfig
Requires(preun): chkconfig


%description
The unrar utility is a freeware program for extracting, testing and
viewing the contents of archives created with the RAR archiver version
1.50 and above.


%package -n libunrar
Summary:        Decompress library for RAR v3 archives
Group:          System Environment/Libraries

%description -n libunrar
The libunrar library allows programs linking against it to decompress
existing RAR v3 archives.


%package -n libunrar-devel
Summary:        Development files for libunrar
Group:          Development/Libraries
Requires:       libunrar = %{version}-%{release}
Provides:       libunrar3-%{version}

%description -n libunrar-devel
The libunrar-devel package contains libraries and header files for
developing applications that use libunrar.


%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1


%build
make %{?_smp_mflags} -f makefile.unix \
  CXX="%{__cxx}" CXXFLAGS="$RPM_OPT_FLAGS -fPIC -DPIC" STRIP=: RANLIB=ranlib
make %{?_smp_mflags} -f makefile.unix lib \
  CXX="%{__cxx}" CXXFLAGS="$RPM_OPT_FLAGS -fPIC -DPIC" STRIP=: RANLIB=ranlib


%install
rm -rf %{buildroot}
install -Dpm 755 unrar %{buildroot}%{_bindir}/unrar-nonfree
install -Dpm 644 debian/unrar-nonfree.1 %{buildroot}%{_mandir}/man1/unrar-nonfree.1
install -Dpm 755 libunrar.so %{buildroot}%{_libdir}/libunrar.so
install -Dpm 644 dll.hpp %{buildroot}/%{_includedir}/unrar/dll.hpp

# handle alternatives
touch %{buildroot}%{_bindir}/unrar



%clean
rm -rf %{buildroot}


%post
%{_sbindir}/alternatives \
    --install %{_bindir}/unrar unrar %{_bindir}/unrar-nonfree 50 \
    --slave %{_mandir}/man1/unrar.1.gz unrar.1.gz \
    %{_mandir}/man1/unrar-nonfree.1.gz || :

%preun
if [ "$1" -eq 0 ]; then
  %{_sbindir}/alternatives \
      --remove unrar %{_bindir}/unrar-nonfree || :
fi

%post -n libunrar -p /sbin/ldconfig


%postun -n libunrar -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc license.txt readme.txt
%ghost %{_bindir}/unrar
%{_bindir}/unrar-nonfree
%{_mandir}/man1/unrar-nonfree.1*

%files -n libunrar
%defattr(-,root,root,-)
%doc license.txt readme.txt
%{_libdir}/*.so

%files -n libunrar-devel
%defattr(-,root,root,-)
%doc license.txt readme.txt
%{_includedir}/*


%changelog
* Tue Sep 28 2010 Conrad Meyer <konrad@tylerc.org> - 3.9.10-3
- Patch to fix unresolved symbol issues (#1385).

* Thu Sep 2 2010 Conrad Meyer <konrad@tylerc.org> - 3.9.10-1
- Bump to 3.9.10.

* Sun Feb 21 2010 Conrad Meyer <konrad@tylerc.org> - 3.9.9-1
- Bump to 3.9.9.

* Sun Dec 6 2009 Conrad Meyer <konrad@tylerc.org> - 3.8.5-5
- Fix post to use alternatives to manage unrar manpage as well.

* Mon Nov 30 2009 Conrad Meyer <konrad@tylerc.org> - 3.8.5-4
- Fix preun to refer to the correct alternatives files.

* Fri Nov 20 2009 Conrad Meyer <konrad@tylerc.org> - 3.8.5-3
- Add missing post/preun requires on chkconfig (#956).

* Fri Jul 17 2009 Conrad Meyer <konrad@tylerc.org> - 3.8.5-2
- Fix breakages introduced by dropping the versioned SONAME patch.

* Wed Jul 8 2009 Conrad Meyer <konrad@tylerc.org> - 3.8.5-1
- Bump to 3.8.5.

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.7.8-4
- rebuild for new F11 features

* Sat Oct 25 2008 Andreas Thienemann <andreas@bawue.net> - 3.7.8-3
- Added libunrar sub-packages
- Clarified license
- Added unrar robustness patches

* Thu Jul 24 2008 Conrad Meyer <konrad@tylerc.org> - 3.7.8-2
- Import into RPM Fusion.

* Sat Oct 13 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.8-1
- 3.7.8.

* Sat Sep  8 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.7-1
- 3.7.7, fixes CVE-2007-3726.

* Wed Aug 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.6-2
- Rebuild.

* Sun Jul  8 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.6-1
- 3.7.6.

* Fri May 18 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.5-1
- 3.7.5.

* Sat Mar 10 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.4-1
- 3.7.4.

* Wed Feb 14 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.3-1
- 3.7.3.

* Wed Jan 17 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.2-1
- 3.7.2.

* Wed Sep 13 2006 Ville Skyttä <ville.skytta at iki.fi> - 3.6.8-1
- 3.6.8.

* Wed Jul 12 2006 Ville Skyttä <ville.skytta at iki.fi> - 3.6.6-1
- 3.6.6.

* Wed May 31 2006 Ville Skyttä <ville.skytta at iki.fi> - 3.6.4-1
- 3.6.4.

* Sat May 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 3.6.3-1
- 3.6.3.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Tue Oct 11 2005 Ville Skyttä <ville.skytta at iki.fi> - 3.5.4-0.lvn.1
- 3.5.4.
- Drop zero Epoch.

* Wed Aug 10 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:3.5.3-0.lvn.1
- 3.5.3.

* Thu May 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:3.5.2-0.lvn.1
- 3.5.2.

* Thu Mar 31 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:3.5.1-0.lvn.1
- 3.5.1.

* Wed Nov 24 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.4.3-0.lvn.1
- Update to 3.4.3.

* Sun Sep  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.4.2-0.lvn.1
- Update to 3.4.2, nostrip patch no longer necessary.
- Update Debian patch URL.

* Sat Jul  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.4.1-0.lvn.1
- Update to 3.4.1 and Debian patch to 3.3.6-2.

* Thu May 20 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.3.6-0.lvn.2
- Update Debian patch to 3.3.6-1 (no real changes, just a working URL again).

* Sun Feb  8 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.3.6-0.lvn.1
- Update to 3.3.6.

* Mon Jan 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.3.4-0.lvn.1
- Update to 3.3.4.

* Sat Dec 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.3.3-0.lvn.1
- Update to 3.3.3.

* Sun Dec 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.3.2-0.lvn.1
- Update to 3.3.2.

* Wed Nov 26 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.3.1-0.lvn.1
- Update to 3.3.1.

* Sun Sep 14 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.2.3-0.fdr.1
- Update to 3.2.3.
- Sync with current Fedora spec template.

* Wed Apr 16 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.2.1-0.fdr.1
- Update to 3.2.1.

* Sat Apr  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.2.0-0.fdr.1
- Update to 3.2.0 and current Fedora guidelines.

* Sun Feb  9 2003 Ville Skyttä <ville.skytta at iki.fi> - 3.1.3-1.fedora.1
- First Fedora release, based on Matthias Saou's and PLD work.
