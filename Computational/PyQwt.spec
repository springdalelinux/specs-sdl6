Name:           PyQwt
Version:        5.2.0
Release:        11%{?dist}
Summary:        Python bindings for Qwt

Group:          Development/Languages
# GPLv2+ exceptions (see COPYING.PyQwt)
License:        GPLv2+ with exceptions
URL:            http://pyqwt.sourceforge.net/
Source0:        http://downloads.sourceforge.net/pyqwt/%{name}-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  sip-devel
BuildRequires:  PyQt4-devel
BuildRequires:  numpy-f2py
BuildRequires:  qwt-devel

Requires:       PyQt4
Requires:       numpy
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}

# prevent rpm's auto-generated provides mechanism to include PyQwt's private
# libraries
%{?filter_setup:
%filter_provides_in %{python_sitearch}/PyQt4/Qwt5/.*\.so$
%filter_setup
}

%description
PyQwt is a set of Python bindings for the Qwt C++ class library which extends
the Qt framework with widgets for scientific and engineering applications. It
provides a widget to plot 2-dimensional data and various widgets to display and
control bounded or unbounded floating point values.


%package devel
Summary: Files needed to build other bindings on PyQwt
Group:   Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: PyQt4-devel
Requires: qwt-devel

%description devel
Files needed to build other bindings for Qwt C++ classes that inherit from
any of the PyQwt classes.


%prep
%setup -q

# mark examples non-executable
find qt4examples/ -name "*.py" | xargs chmod a-x


%build
QWTDIR=%{_includedir}/qwt
cd configure
%{__python} configure.py -I$QWTDIR -lqwt --disable-numarray --disable-numeric
make %{?_smp_mflags}

%install
cd configure
make DESTDIR=%{buildroot} install
# move the generated pdf and html documentation to devel-doc directory
cd ..
mkdir devel-doc
mv sphinx/build/latex/PyQwt.pdf devel-doc
rm sphinx/build/html/.buildinfo
mv sphinx/build/html devel-doc

# non-executable scripts
chmod 755 %{buildroot}/%{python_sitearch}/PyQt4/Qwt5/grace.py
chmod 755 %{buildroot}/%{python_sitearch}/PyQt4/Qwt5/qplt.py

#FIXME!!! temporarily remove qwt.py* files which conflict with PyQt4 package
rm -rf %{buildroot}/%{python_sitearch}/PyQt4/uic


%files
%defattr(-,root,root,-)
%doc ANNOUNCEMENT-%{version} README
%doc COPYING*
%{python_sitearch}/PyQt4/*


%files devel
%defattr(-,root,root,-)
%doc devel-doc/*
%doc qt4examples/ 
%{_datadir}/sip/PyQt4/Qwt5/


%changelog
* Mon Jan 03 2011 Tadej Janež <tadej.janez@tadej.hicsalta.si> - 5.2.0-11
- changes to the spec file that follow the latest Packaging Guidelines:
  - removed BuildRoot tag
  - removed %%clean section
- removed private shared object provides that were reported by rpmlint
- removed the manual definition of the python_sitearch macro
- simplified the handling of devel documentation files
- minor cosmetic cleanups

* Fri Dec 10 2010 Rex Dieter <rdieter@fedoraproject.org> -  5.2.0-10
- rebuild (sip, #662039))

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-9
- rebuild(sip)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 5.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr 21 2010 Tadej Janež <tadej.janez@tadej.hicsalta.si> - 5.2.0-7
- another rebuild (for qwt-5.2.1, f11+)

* Mon Apr 19 2010 Tadej Janež <tadej.janez@tadej.hicsalta.si> - 5.2.0-6
- rebuild (for qwt-5.2.1, f11+)

* Mon Apr 12 2010 Tadej Janež <tadej.janez@tadej.hicsalta.si> - 5.2.0-5
- rebuild (for qwt-5.2.0, f11+)

* Thu Jan 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-4 
- rebuild (sip)

* Thu Nov 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-3.1 
- rebuild (for qt-4.6.0-rc1, f13+)

* Mon Nov 16 2009 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- Requires: sip-api(%%_sip_api_major) >= %%_sip_api (#537894)

* Wed Oct 28 2009 Tadej Janež <tadej.janez@tadej.hicsalta.si> 5.2.0-2
- made qplt.py executable (to fix a rpmlint error)
- removed html/.buildinfo from sphinx documentation (to fix a rpmlint error)
- changed BuildRequires from numpy to numpy-f2py to cope with the numpy
  package split
- temporarily removed qwt.py* files which conflict with the ones provided
  by the PyQt4 package

* Sun Sep  6 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 5.2.0-1
- Fix FTBFS: Update to 5.2.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Tadej Janež <tadej.janez@tadej.hicsalta.si> 5.1.0-3
- made grace.py executable again

* Fri Jan 09 2009 Tadej Janež <tadej.janez@tadej.hicsalta.si> 5.1.0-2
- disabled support for Numeric and Numarray
- incorporated fixes from package review in BZ472229

* Tue Nov 18 2008 Tadej Janež <tadej.janez@tadej.hicsalta.si> 5.1.0-1
- initial package

