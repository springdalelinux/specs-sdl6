%{!?ruby_sitelib: %global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname json
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global installroot %{buildroot}%{geminstdir}


Name:           rubygem-%{gemname}
Version:        1.4.6
Release:        3%{?dist}

Summary:        A JSON implementation in Ruby

Group:          Development/Languages

License:        Ruby or GPLv2
URL:            http://json.rubyforge.org
Source0:        http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         %{gemname}-1.4.3-skip-failed-test.patch

BuildRequires:  ruby, ruby-devel
BuildRequires:  rubygem(rake)
Requires:       ruby(abi) = 1.8
Requires:       rubygems
Provides:       rubygem(json) = %{version}

%description
This is a implementation of the JSON specification according
to RFC 4627 in Ruby.
You can think of it as a low fat alternative to XML,
if you want to store data to disk or transmit it over
a network rather than use a verbose markup language.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation

Requires:	%{name} = %{version}-%{release}
Requires:	ruby(rubygems)

%description	doc
This package contains documentation for %{name}.

%package	-n ruby-%{gemname}
Summary:	Non-Gem support package for %{gemname}
Group:		Development/Languages

Requires:	%{name} = %{version}-%{release}
Provides:	ruby(%{gemname}) = %{version}-%{release}

%description	-n ruby-%{gemname}
This package provides non-Gem support for %{gemname}.

%package        -n rubygem-%{gemname}-gui
Summary:        Gtk2 based Editor for ruby JSON.
Group:          User Interface/Desktops

Requires:       %{name} = %{version}-%{release}
Requires:       ruby(gtk2)

%description    -n rubygem-%{gemname}-gui
This package provides UI editor for rubygem-%{gemname}.

%package        -n ruby-%{gemname}-gui
Summary:        Gtk2 based editor for Ruby JSON
Group:          User Interface/Desktop

Requires:       ruby-%{gemname} = %{version}-%{release}
Requires:       ruby(gtk2)

%description    -n ruby-%{gemname}-gui
This package provides UI editor for ruby-%{gemname}.

%prep
%setup -q -c -T

mkdir -p ./%{gemdir}

%build
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --local --install-dir .%{gemdir} -V --force %{SOURCE0}

# change cflags to honor Fedora compiler flags correctly
find . -name extconf.rb | xargs sed -i -e 's|-O3|-O2|'
pushd .%{geminstdir}
cat %PATCH0 | patch -s -p1 --fuzz=0
# compile again
rake clean
rake

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{gemdir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{ruby_sitearch}/%{gemname}/ext
 
cp -a .%{gemdir}/* %{buildroot}/%{gemdir}

# Let's move arch dependent files to %%ruby_sitearch
find . -name "*.so" -exec mv {} \
	$RPM_BUILD_ROOT%{ruby_sitearch}/%{gemname}/ext \;

mv $RPM_BUILD_ROOT%{gemdir}/bin/* $RPM_BUILD_ROOT%{_bindir}

chmod 0755 $RPM_BUILD_ROOT%{geminstdir}/install.rb
chmod 0755 $RPM_BUILD_ROOT%{geminstdir}/bin/*.rb
chmod 0755 $RPM_BUILD_ROOT%{geminstdir}/tests/*.rb
chmod 0755 $RPM_BUILD_ROOT%{geminstdir}/tools/server.rb
chmod 0644 $RPM_BUILD_ROOT%{geminstdir}/tools/fuzz.rb
chmod 0755 $RPM_BUILD_ROOT%{geminstdir}/benchmarks/*.rb

# We don't need those files anymore.
rm -rf $RPM_BUILD_ROOT%{geminstdir}/ext
rm -rf $RPM_BUILD_ROOT%{geminstdir}/install.rb
rm -rf $RPM_BUILD_ROOT%{geminstdir}/.require_paths
rm -rf $RPM_BUILD_ROOT%{gemdir}/doc/%{gemname}-%{version}/rdoc/classes/.src
rm -rf $RPM_BUILD_ROOT%{gemdir}/doc/%{gemname}-%{version}/rdoc/classes/.html

create_symlink_rec(){

ORIGBASEDIR=$1
TARGETBASEDIR=$2

## First calculate relative path of ORIGBASEDIR 
## from TARGETBASEDIR
TMPDIR=$TARGETBASEDIR
BACKDIR=
DOWNDIR=
num=0
nnum=0
while true
do
        num=$((num+1))
        TMPDIR=$(echo $TMPDIR | %{__sed} -e 's|/[^/][^/]*$||')
        DOWNDIR=$(echo $ORIGBASEDIR | %{__sed} -e "s|^$TMPDIR||")
        if [ x$DOWNDIR != x$ORIGBASEDIR ]
        then
                nnum=0
                while [ $nnum -lt $num ]
                do
                        BACKDIR="../$BACKDIR"
                        nnum=$((nnum+1))
                done
                break
        fi
done

RELBASEDIR=$( echo $BACKDIR/$DOWNDIR | %{__sed} -e 's|//*|/|g' )

## Next actually create symlink
pushd %{buildroot}/$ORIGBASEDIR
find . -type f | while read f
do
        DIRNAME=$(dirname $f)
        BACK2DIR=$(echo $DIRNAME | %{__sed} -e 's|/[^/][^/]*|/..|g')
        %{__mkdir_p} %{buildroot}${TARGETBASEDIR}/$DIRNAME
        LNNAME=$(echo $BACK2DIR/$RELBASEDIR/$f | \
                %{__sed} -e 's|^\./||' | %{__sed} -e 's|//|/|g' | \
                %{__sed} -e 's|/\./|/|' )
        %{__ln_s} -f $LNNAME %{buildroot}${TARGETBASEDIR}/$f
done
popd

}

create_symlink_rec %{geminstdir}/lib %{ruby_sitelib}

%clean
rm -rf $RPM_BUILD_ROOT

%check
pushd .%{geminstdir}
rake test_ext --trace
popd



%files
%defattr(-,root,root,-)
%doc %{geminstdir}/[A-Z]*
%dir %{geminstdir}
%dir %{geminstdir}/lib
%dir %{geminstdir}/lib/%{gemname}
%{_bindir}/prettify_json.rb
%{geminstdir}/bin
%{geminstdir}/tools
%{geminstdir}/lib/%{gemname}.rb
%{geminstdir}/lib/%{gemname}/add
%{geminstdir}/lib/%{gemname}/pure
%{geminstdir}/lib/%{gemname}/*.xpm
%{geminstdir}/lib/%{gemname}/common.rb
%{geminstdir}/lib/%{gemname}/ext.rb
%{geminstdir}/lib/%{gemname}/pure.rb
%{geminstdir}/lib/%{gemname}/version.rb
%{ruby_sitearch}/%{gemname}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files      doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/data
%{geminstdir}/tests
%{geminstdir}/benchmarks
#%{geminstdir}/doc-main.txt
%{gemdir}/doc/%{gemname}-%{version}

%files -n   ruby-%{gemname}
%defattr(-,root,root,-)
%dir %{ruby_sitelib}/%{gemname}
%{ruby_sitelib}/%{gemname}/add
%{ruby_sitelib}/%{gemname}/pure
%{ruby_sitelib}/%{gemname}/*.xpm
%{ruby_sitelib}/%{gemname}/common.rb
%{ruby_sitelib}/%{gemname}/ext.rb
%{ruby_sitelib}/%{gemname}/pure.rb
%{ruby_sitelib}/%{gemname}/version.rb
%{ruby_sitelib}/%{gemname}.rb

%files -n   rubygem-%{gemname}-gui
%defattr(-,root,root,-)
%{_bindir}/edit_json.rb
%{geminstdir}/lib/%{gemname}/editor.rb

%files -n   ruby-%{gemname}-gui
%defattr(-,root,root,-)
%{ruby_sitelib}/%{gemname}/editor.rb


%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.4.6-2
- Rebuilt for gcc bug 634757

* Sat Sep 18 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.6-1
- Update release.
- Enabled test stage.

* Fri Jun 11 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-3
- Move ruby's site_lib editor to ruby-json-gui.

* Mon May 10 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-2
- Move editor out of ruby-json sub-package.

* Sun May 09 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-1
- Update release.
- Split-out json editor.

* Thu Oct 29 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.9-1
- Update release.

* Wed Aug 12 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-3
- Fix gem scripts and install_dir.
- Enable %%check stage.

* Wed Aug 05 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-2
- Rebuild in correct buildir process.
- Add sub packages.

* Mon Aug 03 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-1
- Update release.

* Sat Jun 06 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.6-1
- Update release.

* Tue May 12 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.5-1
- Update release.

* Thu Apr 02 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.4-1
- Update release.

* Sat Jul 12 2008 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.3-1
- Initial RPM release.
