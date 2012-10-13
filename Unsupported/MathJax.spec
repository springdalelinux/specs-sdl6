%define gittag g4a4f535

Summary: Open source JavaScript display engine for mathematics that works in modern browsers
Name: MathJax
Version: 2.0
# installation location
%define installoc /var/www/%{name}
Release: 2%{?dist}
License: ASL 2.0
Group: Applications/Internet
BuildArch: noarch
#Source: https://github.com/mathjax/MathJax/zipball/v1.1
Source: mathjax-MathJax-v%{version}-0-%{gittag}.zip
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
URL: http://www.mathjax.org/
Requires: httpd

%description
MathJax is an open-source JavaScript display engine for LaTeX and
MathML that works in all modern browsers.  It was designed with the
goal of consolidating the recent advances in web technologies into a
single, definitive, math-on-the-web platform supporting the major
browsers and operating systems.  It requires no setup on the part of
the user (no plugins to downlaod or software to install), so the page
author can write web documents that include mathematics and be
confident that users will be able to view it naturally and easily.
One simply includes MathJax and some mathematics in a web page, and
MathJax does the rest.

Some of the main features of MathJax include:

  o High-quality display of LaTeX and MathML math notation in HTML pages

  o Supported in most browsers with no plug-ins, extra fonts, or special
    setup for the reader

  o Easy for authors, flexible for publishers, extensible for developers

  o Supports math accessibility, cut and paste interoperability and other
    advanced functionality

  o Powerful API for integration with other web applications

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{installoc}
pushd $RPM_BUILD_ROOT/%{installoc}/..
# main files
unzip -q %{SOURCE0}
find . -name .gitignore | xargs rm -f
mv mathjax-MathJax-*/* MathJax
rmdir mathjax-MathJax-*

# web server config file
mkdir -p  $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/MathJax.conf <<ENDCONF
Alias /MathJax/ "%{installoc}/"
Alias /mathjax/ "%{installoc}/"

<Directory "%{installoc}">
    Options None
    AllowOverride None
    Order allow,deny
    Allow from all
</Directory>
ENDCONF


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{installoc}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/MathJax.conf

%changelog
* Mon Apr 04 2011 Josko Plazonic <plazonic@math.princeton.edu>
- update to version 1.1

* Sun Dec 12 2010 Josko Plazonic <plazonic@math.princeton.edu>
- update otf fonts for firefox 3.6.13 compatibility

* Mon Oct 18 2010 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
