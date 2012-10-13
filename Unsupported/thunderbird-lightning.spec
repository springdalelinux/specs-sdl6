%global nspr_version 4.8.9
%global nss_version 3.13.1
%global cairo_version 1.8.8
%global freetype_version 2.1.9
%global sqlite_version 3.6.14
%global libnotify_version 0.4
# Update these two as a pair - see calendar/lightning/install.rdf
%global thunderbird_version 10.0
%global thunderbird_next_version 11.0
# Compatible versions are listed in:
# comm-release/calendar/lightning/install.rdf.rej
# comm-release/calendar/providers/gdata/install.rdf.rej
%global moz_objdir objdir-tb
%global lightning_extname %{_libdir}/mozilla/extensions/{3550f703-e582-4d05-9a08-453d09bdfdc6}/{e2fda1a4-762b-4020-b5ad-a41df1933103}
%global gdata_extname %{_libdir}/mozilla/extensions/{3550f703-e582-4d05-9a08-453d09bdfdc6}/{a62ef8ec-5fdc-40c2-873c-223b8a6925cc}

# The tarball is pretty inconsistent with directory structure.
# Sometimes there is a top level directory.  That goes here.
#
# IMPORTANT: If there is no top level directory, this should be
# set to the cwd, ie: '.'
#global tarballdir .
%global tarballdir comm-release

%global version_internal  2
%global mozappdir         %{_libdir}/%{name}-%{version_internal}

Name:           thunderbird-lightning
Summary:        The calendar extension to Thunderbird
Version:        1.2.3
Release:        1%{?dist}
URL:            http://www.mozilla.org/projects/calendar/lightning/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Productivity
Source0:        http://releases.mozilla.org/pub/mozilla.org/calendar/lightning/releases/%{version}/source/lightning-%{version}.source.tar.bz2
#Source0:        http://releases.mozilla.org/pub/mozilla.org/thunderbird/releases/%{thunderbird_version}/source/thunderbird-%{thunderbird_version}.source.tar.bz2
# This script will generate the language source below
Source1:        mklangsource.sh
Source2:        l10n-%{version}.tar.xz
# Config file for compilation
Source10:       thunderbird-mozconfig
# Finds requirements provided outside of the current file set
Source100:      find-external-requires

# Mozilla (XULRunner) patches
Patch0:         thunderbird-version.patch
# Fixup gcc 4.7 build issues
Patch1:         thunderbird-lightning-gcc47.patch
# Fix build on secondary arches (patches copied from xulrunner)
Patch2:         xulrunner-10.0-secondary-ipc.patch
# Patch from EL6 TB for PCRE issues on ppc
Patch15:        mozilla-691898.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
%if 0%{?fedora} > 15
BuildRequires:  nss-static
%endif
BuildRequires:  cairo-devel >= %{cairo_version}
BuildRequires:  libnotify-devel >= %{libnotify_version}
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= %{freetype_version}
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  hunspell-devel
BuildRequires:  sqlite-devel >= %{sqlite_version}
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf213
BuildRequires:  desktop-file-utils
BuildRequires:  libcurl-devel
BuildRequires:  python
BuildRequires:  yasm
BuildRequires:  mesa-libGL-devel
Requires:       thunderbird >= %{thunderbird_version}
Requires:       thunderbird < %{thunderbird_next_version}
Obsoletes:      thunderbird-lightning-wcap <= 0.8
Provides:       thunderbird-lightning-wcap = %{version}-%{release}
AutoProv: 0
%global _use_internal_dependency_generator 0
%global __find_requires %{SOURCE100}


%description
Lightning brings the Sunbird calendar to the popular email client,
Mozilla Thunderbird. Since it's an extension, Lightning is tightly
integrated with Thunderbird, allowing it to easily perform email-related
calendaring tasks.


%prep
%setup -q -c -a 2
cd %{tarballdir}

sed -e 's/__RPM_VERSION_INTERNAL__/%{version_internal}/' %{P:%%PATCH0} \
    > version.patch
%{__patch} -p1 -b --suffix .version --fuzz=0 < version.patch
%patch1 -p2 -b .gcc47

cd mozilla
%patch2 -p3 -b .secondary-ipc
%patch15 -p1 -b .691898
cd ..

%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig

# s390(x) fails to start with jemalloc enabled
%ifarch s390 s390x
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

# Fix permissions
find -name \*.js | xargs chmod -x

#===============================================================================

%build
cd %{tarballdir}

INTERNAL_GECKO=%{version_internal}
MOZ_APP_DIR=%{mozappdir}

# -fpermissive is needed to build with gcc 4.6+ which has become stricter
#
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
# 
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS -fpermissive" | \
                      %{__sed} -e 's/-Wall//' -e 's/-fexceptions/-fno-exceptions/g')
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

%global moz_make_flags -j1
%ifarch ppc ppc64 s390 s390x
%global moz_make_flags -j1
%else
%global moz_make_flags %{?_smp_mflags}
%endif

export LDFLAGS="-Wl,-rpath,%{mozappdir}"
export MAKE="gmake %{moz_make_flags}"
make -f client.mk build STRIP=/bin/true

# Package l10n files
cd objdir-tb/calendar/lightning
make AB_CD=all L10N_XPI_NAME=lightning-all repack-clobber-all
grep -v 'osx' ../../../calendar/locales/shipped-locales | while read lang x
do
   make AB_CD=all L10N_XPI_NAME=lightning-all libs-$lang
done

#===============================================================================

%install
rm -rf $RPM_BUILD_ROOT
cd %{tarballdir}

# Avoid "Chrome Registration Failed" message on first startup and extension installation
mkdir -p $RPM_BUILD_ROOT%{lightning_extname}
touch $RPM_BUILD_ROOT%{lightning_extname}/chrome.manifest
mkdir -p $RPM_BUILD_ROOT%{gdata_extname}
touch $RPM_BUILD_ROOT%{gdata_extname}/chrome.manifest

# Lightning and GData provider for it
unzip -qod $RPM_BUILD_ROOT%{lightning_extname} objdir-tb/mozilla/dist/xpi-stage/lightning-all.xpi
unzip -qod $RPM_BUILD_ROOT%{gdata_extname} objdir-tb/mozilla/dist/xpi-stage/gdata-provider.xpi

# Fix up permissions
find $RPM_BUILD_ROOT -name \*.so | xargs chmod 0755

#===============================================================================

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#===============================================================================

%files
%defattr(-,root,root,-)
%doc %{tarballdir}/mozilla/LEGAL %{tarballdir}/mozilla/LICENSE %{tarballdir}/mozilla/README.txt
%{lightning_extname}
%{gdata_extname}

#===============================================================================

%changelog
* Wed Mar 14 2012 Orion Poplawski <orion@cora.nwra.com> - 1.2.3-1
- Update to 1.2.3
- Add patch from EL6 TB to fix ppc64 pcre build issue

* Wed Mar 14 2012 Orion Poplawski <orion@cora.nwra.com> - 1.2.1-1
- Update to 1.2.1
- Disable using system cairo - too old in EL6

* Fri Feb 17 2012 Orion Poplawski <orion@cora.nwra.com> 1.0-0.44.b3pre
- Build l10n

* Fri Feb 17 2012 Orion Poplawski <orion@cora.nwra.com> 1.0-0.43.b3pre
- Update to thunderbird 3.1.18 source
- EL6 has nss-devel, no nss-static

* Tue Jun 28 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.42.b3pre
- Update to thunderbird 3.1.11 source
- Drop notify patch, fixed upstream
- Change BR nss-devel to nss-static (Bug 717246)
- Add BR python

* Mon Apr 11 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.41.b3pre
- Fix debuginfo builds
- Remove official branding sections
- Don't unpack the .xpi

* Wed Apr 6 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.40.b3pre
- Fixup some file permissions
- Minor review cleanups

* Mon Apr 4 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.39.b3pre
- Initial packaging, based on thunderbird 3.1.9
