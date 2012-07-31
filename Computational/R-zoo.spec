# This is the CRAN name
%define packname zoo
# Note that some R packages do not use packrel
%define packrel 3

Name:             R-%{packname}
Version:          1.6
Release:          3%{?dist}
Source0:          http://cran.r-project.org/src/contrib/%{packname}_%{version}-%{packrel}.tar.gz
License:          GPLv2
URL:              http://cran.r-project.org/web/packages/zoo/index.html
Group:            Applications/Engineering
Summary:          Z's ordered observations for irregular time series
BuildRequires:    R-devel
%if 0%{?fedora} >= 9
BuildRequires:    tex(latex)
%else
BuildRequires:    tetex-latex
%endif
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
Requires(post):   R
Requires(postun): R
Requires:         R


%description
An S3 class with methods for totally ordered indexed observations. It is
particularly aimed at irregular time series of numeric vectors/matrices and
factors. zoo's key design goals are independence of a particular index/date/
time class and consistency with with ts and base R by providing methods to
extend standard generics. 


%prep
%setup -q -c -n %{packname}
#Fix line endings
sed -i -e 's/\r//' zoo/inst/doc/zoo*.Rnw


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/R/library
%{_bindir}/R CMD INSTALL -l $RPM_BUILD_ROOT%{_datadir}/R/library %{packname}
# Clean up in advance of check
test -d %{packname}/src && (cd %{packname}/src; rm -f *.o *.so)
rm -rf $RPM_BUILD_ROOT%{_datadir}/R/library/R.css
#Couple other doc files
cp -p zoo/THANKS zoo/WISHLIST $RPM_BUILD_ROOT%{_datadir}/R/library/%{packname}/


%check
#We have to use --no-install because we don't have all of the suggested
#dependencies
%{_bindir}/R CMD check --no-install %{packname}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{_R_make_search_index}

%postun
%{_R_make_search_index}


%files
%defattr(-, root, root, -)
%dir %{_datadir}/R/library/%{packname}
%doc %{_datadir}/R/library/%{packname}/demo
%doc %{_datadir}/R/library/%{packname}/doc
%doc %{_datadir}/R/library/%{packname}/html
%doc %{_datadir}/R/library/%{packname}/CITATION
%doc %{_datadir}/R/library/%{packname}/DESCRIPTION
%doc %{_datadir}/R/library/%{packname}/NEWS
%doc %{_datadir}/R/library/%{packname}/THANKS
%doc %{_datadir}/R/library/%{packname}/WISHLIST
%{_datadir}/R/library/%{packname}/INDEX
%{_datadir}/R/library/%{packname}/NAMESPACE
%{_datadir}/R/library/%{packname}/Meta
%{_datadir}/R/library/%{packname}/R
%{_datadir}/R/library/%{packname}/help


%changelog
* Thu May 13 2010 Orion Poplawski <orion@cora.nwra.com> 1.6-3
- Update to 1.6-3

* Sun Jan 10 2010 Orion Poplawski <orion@cora.nwra.com> 1.6-2
- Update to 1.6-2

* Thu Nov 12 2009 Orion Poplawski <orion@cora.nwra.com> 1.5-9
- Rebuild for R 2.10.0

* Fri Oct 2 2009 Orion Poplawski <orion@cora.nwra.com> 1.5-8
- Update to 1.5-8

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 4 2008 Orion Poplawski <orion@cora.nwra.com> 1.5-5
- Update to 1.5-4

* Tue May 20 2008 Orion Poplawski <orion@cora.nwra.com> 1.5-4
- Add a couple more doc files

* Mon May 12 2008 Orion Poplawski <orion@cora.nwra.com> 1.5-3
- Include time series in summary
- Fix up build requires for older versions

* Fri May 9 2008 Orion Poplawski <orion@cora.nwra.com> 1.5-2
- Fix URL
- Fix line endings
- Change requires to tex(latex)

* Wed May 7 2008 Orion Poplawski <orion@cora.nwra.com> 1.5-1
- Initial package creation
