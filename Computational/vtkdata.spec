Summary: Example data file for VTK
Name: vtkdata
Version: 5.8.0
Release: 1
# This is a variant BSD license, a cross between BSD and ZLIB.
# For all intents, it has the same rights and restrictions as BSD.
# http://fedoraproject.org/wiki/Licensing/BSD#VTKBSDVariant
# This file tree has no indication of license, but upstream confirms it
# is the same as the vtk code.
License: BSD
Group: Development/Libraries
URL: http://www.vtk.org/
Source0: http://www.vtk.org/files/release/5.8/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
Example data file for VTK

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}
cd %{buildroot}%{_datadir}
tar -zpxf %{SOURCE0}
mv VTKData %{name}-%{version}

# (Verbosely) fix 0555 permissions
find . -type f -perm 0555 | xargs -r echo chmod 0755 | sh -x
# Remove execute bits from not-scripts
for file in `find . -type f -perm 0755`; do
  head -1 $file | grep '^#!' > /dev/null && continue
  chmod 0644 $file
done

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_datadir}/*

%changelog
* Tue Oct 11 2011 Orion Poplawski <orion@cora.nwra.com> - 5.8.0-1
- Update to 5.8.0

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-1
- Update to 5.6.1

* Mon Jul  5 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.6.0-12
- Update to 5.6.0.

* Sat Jun  6 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.4.2-11
- Update to 5.4.2.

* Wed Mar 11 2009 Orion Poplawski <orion@cora.nwra.com> - 5.2.1-10
- Update to 5.2.1

* Sun Oct  5 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.2.0-9
- Update to 5.2.0.

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.0.4-8
- fix license tag

* Sat Feb 23 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-7
- Update to 5.0.4.

* Sun Apr 15 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.3-6
- Update to 5.0.3.

* Mon Sep 11 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.2-5
- Update to 5.0.2.

* Wed Jul 19 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-4
- Fix some permissions.

* Thu Jul 13 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-3
- Update to 5.0.1.

* Thu Jun  1 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.

