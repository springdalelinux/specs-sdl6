# Patches described below with the patch commands

%define pkg proofgeneral

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

# If the xemacs-devel package has installed a pkgconfig file, use that
# to determine install locations and Emacs version at build time,
# otherwise set defaults.
%if %($(pkg-config xemacs) ; echo $?)
%define xemacs_version 21.5
%define xemacs_lispdir %{_datadir}/xemacs/site-packages/lisp
%define xemacs_startdir %{_datadir}/xemacs/site-packages/lisp/site-start.d
%else
%define xemacs_version %(pkg-config xemacs --modversion)
%define xemacs_lispdir %(pkg-config xemacs --variable sitepkglispdir)
%define xemacs_startdir %(pkg-config xemacs --variable sitestartdir)
%endif

Name:           emacs-common-%{pkg}
Version:        3.7.1
Release:        4%{?dist}
Summary:        Emacs mode for standard interaction interface for proof assistants 

Group:          Applications/Editors
License:        GPLv2
URL:            http://proofgeneral.inf.ed.ac.uk/
Source0:        http://proofgeneral.inf.ed.ac.uk/releases/ProofGeneral-%{version}.tgz

# Patch 0 - Fedora specific, don't do an "install-info" in the make process
# (which would occur at build time), but instead put it into a scriptlet
Patch0:         pg-3.7.1-Makefile.patch

# Patch 1 - Somewhat Fedora specific, patches Proof General starting
# script to include values of build time generated variables (which
# are inserted in the build process with sed) instead of its way of
# getting this information. Also moves around some script parts related
# to emacs version detection.
Patch1:         pg-3.7.1-startscript.patch

# Patch 2 - Display tables were changed in XEmacs 21.5.29 in a way
# that breaks ProofGeneral's X-Symbol code unless changes are made
# Incorporating a patch here from Jerry James. (Of course, right now
# the X-Symbol code is disabled as X-Symbol isn't packaged and
# ProofGeneral makes changes to the X-Symbol code that would have to
# be included somehow anyway, but ProofGeneral's X-Symbol code could
# be activated in the future and the change is necessary to allow the
# code to be byte-compiled).
Patch2:         pg-3.7.1-xemacs-display-table.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  emacs emacs-el xemacs xemacs-devel texinfo-tex xemacs-packages-extra

%description
Proof General is a generic front-end for proof assistants (also known
as interactive theorem provers) based on Emacs.

Proof General allows one to edit and submit a proof script to a proof
assistant in an interactive manner:
- It tracks the goal state, and the script as it is submitted, and
  allows for easy backtracking and block execution.
- It adds toolbars and menus to Emacs for easy access to proof
  assistant features.
- It integrates with X-Symbol for some provers to provide output using
  proper mathematical symbols.
- It includes utilities for generating Emacs tags for proof scripts,
  allowing for easy navigation.

Proof General supports a number of different proof assistants
(Isabelle, Coq, PhoX, and LEGO to name a few) and is designed to be
easily extendable to work with others.

%package -n emacs-%{pkg}
Summary:        Compiled elisp files to run Proof General under GNU Emacs
Group:          Applications/Editors
Requires:       emacs(bin) >= %{emacs_version}
Requires:       emacs-common-%{pkg} = %{version}-%{release}
# MMM Mode is separately packaged for emacs (but not for XEmacs)
Requires:       emacs-mmm

%description -n emacs-%{pkg}
Proof General is a generic front-end for proof assistants based on Emacs.

This package contains the byte compiled elisp packages to run Proof
General with GNU Emacs.

%package -n emacs-%{pkg}-el
Summary:        Elisp source files for Proof General under GNU Emacs
Group:          Applications/Editors
Requires:       emacs-%{pkg} = %{version}-%{release}

%description -n emacs-%{pkg}-el
This package contains the elisp source files for Proof General under
GNU Emacs. You do not need to install this package to run Proof
General. Install the emacs-%{pkg} package to use Proof General with
GNU Emacs.

%package -n xemacs-%{pkg}
Summary:        Compiled elisp files to run Proof General under XEmacs
Group:          Applications/Editors
Requires:       xemacs(bin) >= %{xemacs_version}
Requires:       emacs-common-%{pkg} = %{version}-%{release}
# For MMM mode (and X-Symbol, whose use in this package currently
# doesn't work - disabled until X-Symbol can be separately packaged)
Requires:       xemacs-packages-extra

%description -n xemacs-%{pkg}
Proof General is a generic front-end for proof assistants based on Emacs.

This package contains the byte compiled elisp packages to run Proof
General with XEmacs.

%package -n xemacs-%{pkg}-el
Summary:        Elisp source files for Proof General under XEmacs
Group:          Applications/Editors
Requires:       emacs-%{pkg} = %{version}-%{release}

%description -n xemacs-%{pkg}-el
This package contains the elisp source files for Proof General under
XEmacs. You do not need to install this package to run Proof
General. Install the xemacs-%{pkg} package to use Proof General with
XEmacs.

%prep
%setup -q -n ProofGeneral-%{version}

%patch0
%patch1
%patch2 -p1

%build

# Fix rpmlint complaints:

# Correct permissions for isartags script
chmod 755 isar/isartags
# Correct permissions for x-symbol ChangeLog
chmod 644 x-symbol/lisp/ChangeLog
# Correct permissions for x-symbol Makefile
chmod 644 x-symbol/etc/fonts/Makefile
# Remove .cvsignore file
rm images/gimp/.cvsignore

# Fix non UTF-8 documentation and theory files

# File listing taken from the Makefile
%define doc_files AUTHORS BUGS COMPATIBILITY CHANGES COPYING INSTALL README REGISTER acl2/*.acl2 hol98/*.sml isar/*.thy lclam/*.lcm lego/*.l pgshell/*.pgsh phox/*.phx plastic/*.lf twelf/*.elf
for f in `find %{doc_files}`; do mv $f $f.old && iconv -f iso-8859-1 -t utf8 < $f.old > $f && rm $f.old; done

# Make full copies of emacs and xemacs versions, set options in the proofgeneral start script
make clean
make EMACS=emacs compile bashscripts perlscripts doc
sed -e 's|^EMACS_LISPDIR=.*$|EMACS_LISPDIR=%{emacs_lispdir}|' -e 's|^XEMACS_LISPDIR=.*$|XEMACS_LISPDIR=%{xemacs_lispdir}|' -e 's|^PACKAGE=.*$|PACKAGE=%{pkg}|' < bin/proofgeneral > .tmp && cat .tmp > bin/proofgeneral
mkdir emacs
for f in `find . -maxdepth 1 -mindepth 1 ! -name emacs`; do cp -pr $f emacs/$f; done
make clean
make EMACS=xemacs compile bashscripts perlscripts doc
sed -e 's|^EMACS_LISPDIR=.*$|EMACS_LISPDIR=%{emacs_lispdir}|' -e 's|^XEMACS_LISPDIR=.*$|XEMACS_LISPDIR=%{xemacs_lispdir}|' -e 's|^PACKAGE=.*$|PACKAGE=%{pkg}|' < bin/proofgeneral > .tmp && cat .tmp > bin/proofgeneral
mkdir xemacs
for f in `find . -maxdepth 1 -mindepth 1 ! -name emacs ! -name xemacs`; do cp -pr $f xemacs/$f; done

%install
rm -rf %{buildroot}

%define full_doc_dir %{_datadir}/doc/%{pkg}
%define full_man_dir %{_mandir}/man1
%define full_data_dir %{_datadir}/%{pkg}

%define doc_options DOCDIR=%{buildroot}%{full_doc_dir} MANDIR=%{buildroot}%{full_man_dir} INFODIR=%{buildroot}%{_infodir}
%define common_options PREFIX=%{buildroot}%{_prefix} DEST_PREFIX=%{_prefix} DESKTOP=%{buildroot}%{full_data_dir} BINDIR=%{buildroot}%{_bindir} %{doc_options}

%define emacs_options ELISP_START=%{buildroot}%{emacs_startdir} ELISP=%{buildroot}%{emacs_lispdir}/%{pkg} DEST_ELISP=%{emacs_lispdir}/%{pkg}
%define xemacs_options ELISP_START=%{buildroot}%{xemacs_startdir} ELISP=%{buildroot}%{xemacs_lispdir}/%{pkg} DEST_ELISP=%{xemacs_lispdir}/%{pkg}

cp -pr `find xemacs/ -maxdepth 1 -mindepth 1` .
make EMACS=xemacs %{common_options} %{xemacs_options} install install-doc
cp -pr `find emacs/ -maxdepth 1 -mindepth 1` .
make EMACS=emacs %{common_options} %{emacs_options} install install-doc

# Don't accidentally install an infodir file over an existing one
rm -f %{buildroot}%{_infodir}/dir

%clean
rm -rf %{buildroot}

%post
/sbin/install-info %{_infodir}/ProofGeneral.info* %{_infodir}/dir 2>/dev/null || :
/sbin/install-info %{_infodir}/PG-adapting.info* %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/ProofGeneral.info* %{_infodir}/dir 2>/dev/null || :
  /sbin/install-info --delete %{_infodir}/PG-adapting.info* %{_infodir}/dir 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%{full_doc_dir}
%{full_data_dir}
%{full_man_dir}/*
%{_infodir}/*
%{_bindir}/*

%files -n emacs-%{pkg}
%defattr(-,root,root,-)
%{emacs_lispdir}/%{pkg}/*
# Exclude bundled X-symbol, which should be separately packaged but
# is not critical for the core functionality of the package
%exclude %{emacs_lispdir}/%{pkg}/x-symbol
# Exclude bundled mmm-mode, packaged separately
%exclude %{emacs_lispdir}/%{pkg}/mmm
%exclude %{emacs_lispdir}/%{pkg}/*/*.el
%{emacs_startdir}/*.el
%dir %{emacs_lispdir}/%{pkg}

%files -n emacs-%{pkg}-el
%defattr(-,root,root,-)
%{emacs_lispdir}/%{pkg}/*/*.el

%files -n xemacs-%{pkg}
%defattr(-,root,root,-)
%{xemacs_lispdir}/%{pkg}/*
# Exclude bundled X-symbol, which should be separately packaged but
# is not critical for the core functionality of the package
%exclude %{xemacs_lispdir}/%{pkg}/x-symbol
# Exclude bundled mmm-mode, packaged separately
%exclude %{xemacs_lispdir}/%{pkg}/mmm
%exclude %{xemacs_lispdir}/%{pkg}/*/*.el
%{xemacs_startdir}/*.el
%dir %{xemacs_lispdir}/%{pkg}

%files -n xemacs-%{pkg}-el
%defattr(-,root,root,-)
%{xemacs_lispdir}/%{pkg}/*/*.el

%changelog
* Wed Jul 29 2009 Alan Dunn <amdunn@gmail.com> 3.7.1-4
- Incorporated comments from Jerry James about applying his patch:
  patch now applied unconditionally (regardless of Fedora version
  which was used as a somewhat imperfect way to control XEmacs
  version).
- Patch descriptions moved upward in spec file in accordance with
  examples in guidelines.

* Thu Jul 09 2009 Alan Dunn <amdunn@gmail.com> 3.7.1-3
- Added xemacs patch that fixes compilation problems for X-Symbol code.

* Thu Jul 02 2009 Alan Dunn <amdunn@gmail.com> 3.7.1-2
- Excluded bundled X-symbol, mmm-mode.
- Changed requires for these bundled packages.

* Tue Apr 07 2009 Alan Dunn <amdunn@gmail.com> 3.7.1-1
- Initial Fedora RPM.
