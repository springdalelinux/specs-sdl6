%define pkg mmm

# Check version defaults

# If the emacs-el package has installed a pkgconfig file, use that to
# determine install locations and Emacs version at build time, otherwise
# set defaults.
%if %($(pkg-config emacs) ; echo $?)
%define emacs_version 22.1
%define emacs_lispdir %{_datadir}/emacs/site-lisp
%define emacs_startdir %{_datadir}/emacs/site-lisp/site-start.d
%else
%define emacs_version %(pkg-config emacs --modversion)
%define emacs_lispdir %(pkg-config emacs --variable sitepkglispdir)
%define emacs_startdir %(pkg-config emacs --variable sitestartdir)
%endif

Name:           emacs-%{pkg}
Version:        0.4.8
Release:        2%{?dist}
Summary:        Emacs minor mode allowing different major modes in the same file

Group:          Applications/Editors
License:        GPLv2+
URL:            http://mmm-mode.sourceforge.net/
Source0:        mmm-mode-%{version}.tar.gz
Patch0:         emacs-mmm-fix-compile-warnings-%{version}.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  emacs, texinfo-tex
Requires:       emacs(bin)
Requires(post): info
Requires(preun): info

%description
MMM Mode is an emacs add-on package providing a minor mode that allows
Multiple Major Modes to coexist in one buffer. It is particularly
well-suited to editing embedded code or code that generates other
code, such as Mason or Embperl server-side Perl code, or HTML output
by CGI scripts.

MMM Mode defines a general syntax--the "submode class"--for telling it
how one major mode should be embedded in another. At present, the list
of supplied submode classes is rather limited, but that will hopefully
change soon. Contributions are always welcome; writing a submode class
can be a good introduction to Emacs Lisp, and is usually a simple
excercise for those already proficient. MMM Mode was originally
designed to work in Emacs 19 and 20 and XEmacs 20 and 21.

This has been created as an emacs-only package as it already exists
for XEmacs in xemacs-packages-extra.

%package -n %{name}-el
Summary:        Elisp source files for %{pkg} under GNU Emacs
Group:          Applications/Editors
Requires:       %{name} = %{version}-%{release}

%description -n %{name}-el

This package contains the elisp source files for %{pkg} under GNU
Emacs. You do not need to install this package to run %{pkg}. Install
the %{name} package to use %{pkg} with GNU Emacs.

%prep
%setup -q -n mmm-mode-%{version}

# Fix a number of compile warnings. Fixes courtesy Jerry James
# (see:
%patch0 -p1

%build
export EMACS=%{_bindir}/emacs

%configure
make

# Fix encoding with iconv for info page
mv mmm.info-2 mmm.info-2.tmp && \
   iconv -f ISO-8859-1 -t UTF-8 < mmm.info-2.tmp > mmm.info-2  &&\
   rm mmm.info-2.tmp

# The texinfo.tex here is stale, using it causes errors, so this will
# get the system one to be used instead
rm texinfo.tex
make mmm.pdf

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Fix an issue that occurs in the info files (not quite sure where in
# the process, so doing it here):

mv %{buildroot}%{_infodir}/mmm.info-2.gz \
   %{buildroot}%{_infodir}/mmm.info-2 && \
   gzip %{buildroot}%{_infodir}/mmm.info-2

# We don't want this either, but otherwise we need to do a more complicated
# make command
rm %{buildroot}%{_infodir}/dir

%clean
rm -rf %{buildroot}

%post
/sbin/install-info %{_infodir}/mmm.info.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ] ; then
   /sbin/install-info --delete %{_infodir}/mmm.info.gz %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog FAQ NEWS README README.Mason %{pkg}.pdf
%{emacs_lispdir}/*.elc
%{_infodir}/*.gz

%files -n %{name}-el
%defattr(-,root,root,-)
%{emacs_lispdir}/*.el

%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 08 2009 Alan Dunn <amdunn@gmail.com> 0.4.8-1
- Initial Fedora RPM.
