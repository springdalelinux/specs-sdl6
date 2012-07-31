%if ! (0%{?rhel} > 5)
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

# We include capability for building a doc subpackage for
# documentation. However, building the html documentation requires
# python-basemap, and python-basemap requires python-matplotlib to build, so
# we have a circular dependence, and so we need to be able to turn off
# building of the html documents. Note that when building the html docs,
# python-basemap will pull in the existing python-matplotlib from the
# repos. So, it's important to set PYTHONPATH to use the newly built modules
# from this package. 
%global withhtmldocs 1

# On RHEL 7 onwards, don't build the wx:
%if 0%{?rhel} >= 7
%global with_wx 0
%else
%global with_wx 1
%endif

Name:           python-matplotlib
Version:        1.0.1
Release:        20%{?dist}
Summary:        Python plotting library

Group:          Development/Libraries
License:        Python
URL:            http://sourceforge.net/projects/matplotlib
#Modified Sources to remove the one undistributable file
#See generate-tarball.sh in fedora cvs repository for logic
#sha1sum matplotlib-1.0.1-without-gpc.tar.gz
#a8ccbf4c4b9b90c773380cac83e792673837d3de  matplotlib-1.0.1-without-gpc.tar.gz
Source0:        matplotlib-%{version}-without-gpc.tar.gz
%if %{withhtmldocs}
Source1:        http://downloads.sourceforge.net/matplotlib/mpl_sampledata-%{version}.tar.gz
%endif
Source2:        setup.cfg
# This patch taken from upstream SVN and will not be needed for releases later than 1.0.1
Patch0:         matplotlib-1.0.1-plot_directive.patch
Patch1:         matplotlib-1.0.1-noagg.patch
Patch2:		0001-Bugfix-propagate-timezone-info-in-plot_date-xaxis_da.patch
# fix build when Tkinter doesn't return an expected value in __version__ (FTBFS)
Patch3:         matplotlib-1.0.1-tkinter.patch

# Fix building against libpng 1.5
#   https://github.com/matplotlib/matplotlib/issues/234
# Based on:
#   https://github.com/matplotlib/matplotlib/commit/45c46672648e3b4a277bf7ff42b3baf56a98bcec
Patch4:         use-png-accessor-functions.patch

# Conditionally applied, when disabling wx support:
Patch5:         disable-wx-in-setup.cfg.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-devel, freetype-devel, libpng-devel, zlib-devel
BuildRequires:  pygtk2-devel, gtk2-devel
BuildRequires:  pytz, python-dateutil, numpy
BuildRequires:  agg-devel
BuildRequires:  pyparsing
Requires:       numpy, pytz, python-dateutil
Requires:       pycairo >= 1.2.0
Requires:       dejavu-sans-fonts
Requires:       dvipng
Requires:       pyparsing

%description
Matplotlib is a pure python plotting library with the goal of making
publication quality plots using a syntax familiar to Matlab users. The
library uses numpy for handling large data sets and supports a variety
of output back-ends.


%package        tk
Summary:        Tk backend for python-matplotlib
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  tkinter, tk-devel
Requires:       tkinter

%description    tk
%{summary}

%if 0%{with_wx}
%package        wx
Summary:        wxPython backend for python-matplotlib
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       wxPython
BuildRequires:  wxPython-devel

%description    wx
%{summary}
%endif # if 0%{with_wx}

%package        doc
Summary:        Documentation files for python-matplotlib
Group:          Documentation
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if %{withhtmldocs}
BuildRequires:  python-sphinx
BuildRequires:  tex(latex)
BuildRequires:  dvipng
BuildRequires:  PyQt4
BuildRequires:  python-basemap
# Some of the docs don't build as python-xlwt is needed. However the review
# request isn't yet complete for this package. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=613766 
# BuildRequires: python-xlwt
%endif

%description    doc
%{summary}

%prep
%if %{withhtmldocs}
%setup -q -n matplotlib-%{version} -b1
%else
%setup -q -n matplotlib-%{version}
%endif
%patch0 -p1
%patch2 -p1
%patch3 -p1 -b .tkinter
%patch4 -p1

# Remove bundled libraries
rm -r agg24 lib/matplotlib//pyparsing.py

# Remove references to bundled libraries
%patch1 -p1 -b .noagg
sed -i -e s/matplotlib\.pyparsing/pyparsing/g lib/matplotlib/*.py

chmod -x lib/matplotlib/mpl-data/images/*.svg

cp %{SOURCE2} ./setup.cfg
%if !0%{with_wx}
# Patch the new copy of setup.cfg to remove wx support:
%patch5 -p1
%endif

%if %{withhtmldocs}
pushd doc
echo "examples.download : False" >> matplotlibrc
echo "examples.directory : %{_builddir}/mpl_sampledata-%{version}" >> matplotlibrc
popd
%endif

%build
%{__python} setup.py build

%if %{withhtmldocs}
pushd doc
# Set PYTHONPATH in order to use the just built modules
export PYTHONPATH=`find %{_builddir} -name lib.linux*`
# This really does need to be ran twice
%{__python} make.py --small html && %{__python} make.py --small html
rm -f build/html/.buildinfo
chmod -x build/html/pyplots/make.py
sed -i 's/\r//' build/html/_sources/devel/add_new_projection.txt
sed -i 's/\r//' build/html/examples/api/font_family_rc.py
popd
%endif

# Ensure all example files are non-executable so that the -doc package doesn't
# drag in dependencies
find examples -name '*.py' -exec chmod a-x '{}' \;

# Fix line ending in this example file
sed -i 's/\r//' examples/api/font_family_rc.py

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT
chmod +x $RPM_BUILD_ROOT%{python_sitearch}/matplotlib/dates.py
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/matplotlib/mpl-data/fonts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.txt license/LICENSE license/LICENSE_enthought.txt
%doc license/LICENSE_PAINT license/LICENSE_PIL
%doc CHANGELOG CXX INSTALL INTERACTIVE KNOWN_BUGS
%doc PKG-INFO TODO
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
%{python_sitearch}/*egg-info
%endif
%{python_sitearch}/matplotlib/
%{python_sitearch}/mpl_toolkits/
%{python_sitearch}/pylab.py*
%exclude %{python_sitearch}/matplotlib/backends/backend_tkagg.*
%exclude %{python_sitearch}/matplotlib/backends/tkagg.*
%exclude %{python_sitearch}/matplotlib/backends/_tkagg.so
%exclude %{python_sitearch}/matplotlib/backends/backend_wx.*
%exclude %{python_sitearch}/matplotlib/backends/backend_wxagg.*

%files tk
%defattr(-,root,root,-)
%{python_sitearch}/matplotlib/backends/backend_tkagg.py*
%{python_sitearch}/matplotlib/backends/tkagg.py*
%{python_sitearch}/matplotlib/backends/_tkagg.so

%if 0%{with_wx}
%files wx
%defattr(-,root,root,-)
%{python_sitearch}/matplotlib/backends/backend_wx.py*
%{python_sitearch}/matplotlib/backends/backend_wxagg.py*
%endif # if 0%{with_wx}


%files doc
%defattr(-,root,root,-)
%doc examples
%if %{withhtmldocs}
%doc doc/build/html
%endif

%changelog
* Wed Apr 18 2012 David Malcolm <dmalcolm@redhat.com> - 1.0.1-20
- remove wx support for rhel >= 7

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-19
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec  6 2011 David Malcolm <dmalcolm@redhat.com> - 1.0.1-17
- fix the build against libpng 1.5

* Tue Dec  6 2011 David Malcolm <dmalcolm@redhat.com> - 1.0.1-16
- fix egg-info conditional for RHEL

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.0.1-15
- Rebuild for new libpng

* Mon Oct 31 2011 Dan Horák <dan[at]danny.cz> - 1.0.1-14
- fix build with new Tkinter which doesn't return an expected value in __version__

* Thu Sep 15 2011 Jef Spaleta <jspaleta@fedoraproject.org> - 1.0.1-13
- apply upstream bugfix for timezone formatting (Bug 735677) 

* Fri May 20 2011 Orion Poplawski <orion@cora.nwra.com> - 1.0.1-12
- Add Requires dvipng (Bug 684836)
- Build against system agg (Bug 612807)
- Use system pyparsing (Bug 702160)

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-11
- Set PYTHONPATH during html doc building using find to prevent broken builds

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-10
- Spec file cleanups for readability

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-9
- Bump and rebuild

* Sat Feb 26 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-8
- Fix spec file typos so package builds

* Fri Feb 25 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-7
- Remove a debugging echo statement from the spec file
- Fix some line endings and permissions in -doc sub-package

* Fri Feb 25 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-6
- Spec file cleanups to silence some rpmlint warnings

* Mon Feb 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-5
- Add default attr to doc sub-package file list
- No longer designate -doc subpackage as noarch
- Add arch specific Requires for tk, wx and doc sub-packages

* Mon Feb 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-4
- Enable wxPython backend
- Make -doc sub-package noarch

* Mon Feb 21 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-3
- Add conditional for optionally building doc sub-package
- Add flag to build low res images for documentation
- Add matplotlib-1.0.1-plot_directive.patch to fix build of low res images
- Remove unused patches

* Sat Feb 19 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-2
- Build and package HTML documentation in -doc sub-package
- Move examples to -doc sub-package
- Make examples non-executable

* Fri Feb 18 2011 Thomas Spura <tomspur@fedoraproject.org> - 1.0.1-1
- update to new bugfix version (#678489)
- set file attributes in tk subpackage
- filter private *.so

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 8 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 1.0.0-1
- New upstream release  
- Remove undistributable file from bundled agg library 

* Thu Jul 1 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.3-1
- New upstream release  

* Thu May 27 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.1.2-4
- Upstream patch to fix deprecated gtk tooltip warning.  

* Mon Apr 12 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.1.2-2
- Bump to rebuild against numpy 1.3  

* Thu Apr 1 2010 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.99.1.2-1
- Bump to rebuild against numpy 1.4.0  

* Fri Dec 11 2009 Jon Ciesla <limb@jcomserv.net> - 0.99.1.2
- Update to 0.99.1.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 06 2009 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.5-4
- Fixed font dep after font guideline change

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.5-2
- Add dep on DejaVu Sans font for default font support

* Mon Dec 22 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.5-1
- Latest upstream release
- Strip out included fonts

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.98.3-2
- Rebuild for Python 2.6

* Wed Aug  6 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.3-1
- Latest upstream release

* Fri Jul  1 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 0.98.1-1
- Latest upstream release

* Fri Mar  21 2008 Jef Spaleta <jspaleta[AT]fedoraproject org> - 0.91.2-2
- gcc43 cleanups

* Fri Mar  21 2008 Jef Spaleta <jspaleta[AT]fedoraproject org> - 0.91.2-1
- New upstream version
- Adding Fedora specific setup.cfg from included template
- removed numarry and numerics build requirements

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.90.1-6
- Autorebuild for GCC 4.3

* Fri Jan  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.90.1-5
- Fixed typo in spec.

* Fri Jan  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.90.1-4
- Support for Python Eggs for F9+

* Thu Jan  3 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.90.1-3
- Rebuild for new Tcl 8.5

* Thu Aug 23 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.1-2
- Update license tag to Python
- Rebuild for BuildID

* Mon Jun 04 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.1-1
- Update to 0.90.1

* Wed Feb 14 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.0-2
- Rebuild for Tcl/Tk downgrade

* Sat Feb 10 2007 Jef Spaleta <jspaleta@gmail.com> 0.90.0-2
- Release bump for rebuild against new tk 

* Fri Feb 09 2007 Orion Poplawski <orion@cora.nwra.com> 0.90.0-1
- Update to 0.90.0

* Tue Jan  5 2007 Orion Poplawski <orion@cora.nwra.com> 0.87.7-4
- Add examples to %%docs

* Mon Dec 11 2006 Jef Spaleta <jspaleta@gmail.com> 0.87.7-3
- Release bump for rebuild against python 2.5 in devel tree

* Tue Dec  5 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.7-2
- Force build of gtk/gtkagg backends in mock (bug #218153)
- Change Requires from python-numeric to numpy (bug #218154)

* Tue Nov 21 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.7-1
- Update to 0.87.7 and fix up the defaults to use numpy
- Force build of tkagg backend without X server
- Use src.rpm from Jef Spaleta, closes bug 216578

* Fri Oct  6 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.6-1
- Update to 0.87.6

* Thu Sep  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.5-1
- Update to 0.87.5

* Thu Jul 27 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.4-1
- Update to 0.87.4

* Wed Jun  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.3-1
- Update to 0.87.3

* Mon May 15 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.2-2
- Rebuild for new numpy

* Tue Mar  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.2-1
- Update to 0.87.2

* Tue Mar  7 2006 Orion Poplawski <orion@cora.nwra.com> 0.87.1-1
- Update to 0.87.1
- Add pycairo >= 1.0.2 requires (FC5+ only)

* Fri Feb 24 2006 Orion Poplawski <orion@cora.nwra.com> 0.87-1
- Update to 0.87
- Add BR numpy and python-numarray
- Add patch to keep Numeric as the default numerix package
- Add BR tkinter and tk-devel for TkInter backend
- Make separate package for Tk backend

* Tue Jan 10 2006 Orion Poplawski <orion@cora.nwra.com> 0.86-1
- Update to 0.86

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> 0.85-2
- Rebuild

* Sun Nov 20 2005 Orion Poplawski <orion@cora.nwra.com> 0.85-1
- New upstream version 0.85

* Mon Sep 19 2005 Orion Poplawski <orion@cora.nwra.com> 0.84-1
- New upstream version 0.84

* Tue Aug 02 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.2-3
- bump release 

* Tue Aug 02 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.2-2
- Add Requires: python-numeric, pytz, python-dateutil

* Fri Jul 29 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.2-1
- New upstream version matplotlib 0.83.2

* Thu Jul 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.1-2
- Bump rel to fix botched tag

* Thu Jul 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.83.1-1
- New upstream version matplotlib 0.83.1

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-4
- BuildRequires: pytz, python-dateutil - use upstream
- Don't use INSTALLED_FILES, list dirs
- Fix execute permissions

* Fri Jul 01 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-3
- Use %%{python_sitearch}

* Thu Jun 30 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-2
- Rename to python-matplotlib
- Remove unneeded Requires: python
- Add private directories to %%files

* Tue Jun 28 2005 Orion Poplawski <orion@cora.nwra.com> 0.82-1
- Initial package for Fedora Extras
