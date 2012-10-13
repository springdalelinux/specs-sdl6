%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname sqlite3-ruby
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')}

Summary:        Allows Ruby scripts to interface with a SQLite3 database
Name:           rubygem-%{gemname}
Version:        1.2.4
Release:        5%{?dist}
Group:          Development/Languages
License:        BSD
URL:            http://sqlite-ruby.rubyforge.org/sqlite3
Source0:        http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       rubygems
Requires:       ruby(abi) = 1.8
BuildRequires:  ruby(rubygems)
BuildRequires:  ruby-devel
BuildRequires:  sqlite-devel
BuildRequires:  rubygem(rake)
Provides:       rubygem(%{gemname}) = %{version}-%{release}

%description
SQLite3/Ruby is a module to allow Ruby scripts to interface with a SQLite3
database.

%package	-n ruby-sqlite3
Summary:	A Ruby interface for the SQLite database engine
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Provides:	ruby(sqlite3) = %{version}-%{release}

%description	-n ruby-sqlite3
Database driver to access SQLite v.3 databases from Ruby.

%prep
%setup -q -c -T

%build
mkdir -p ./%{gemdir}
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install \
	--local \
	--install-dir ./%{gemdir} \
	-V --force \
	%{SOURCE0}

# Permission
find . -name \*.rb -or -name \*.gem | xargs chmod 0644

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

install -d -m0755 %{buildroot}%{ruby_sitearch}
mv %{buildroot}%{geminstdir}/lib/sqlite3_api.so %{buildroot}%{ruby_sitearch}
rm -rf %{buildroot}%{geminstdir}/ext/

# The following method is completely copied from rubygem-gettext
# spec file
#
# Create symlinks
##
## Note that before switching to gem %%{ruby_sitelib}/sqlite3
## already existed as a directory, so this cannot be replaced
## by symlink (cpio fails)
## Similarly, all directories under %%{ruby_sitelib} cannot be
## replaced by symlink
#

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
	TMPDIR=$(echo $TMPDIR | sed -e 's|/[^/][^/]*$||')
	DOWNDIR=$(echo $ORIGBASEDIR | sed -e "s|^$TMPDIR||")
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

RELBASEDIR=$( echo $BACKDIR/$DOWNDIR | sed -e 's|//*|/|g' )

## Next actually create symlink
pushd %{buildroot}/$ORIGBASEDIR
find . -type f | while read f
do
	DIRNAME=$(dirname $f)
	BACK2DIR=$(echo $DIRNAME | sed -e 's|/[^/][^/]*|/..|g')
	mkdir -p %{buildroot}${TARGETBASEDIR}/$DIRNAME
	LNNAME=$(echo $BACK2DIR/$RELBASEDIR/$f | \
		sed -e 's|^\./||' | sed -e 's|//|/|g' | \
		sed -e 's|/\./|/|' )
	ln -s -f $LNNAME %{buildroot}${TARGETBASEDIR}/$f
done
popd

}

create_symlink_rec %{geminstdir}/lib %{ruby_sitelib}

%check
# Requires mocha, not available on Fedora yet, disabling
exit 0

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{ruby_sitearch}/sqlite3_api.so

%dir %{geminstdir}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/doc/
%{geminstdir}/lib/
%doc %{geminstdir}/test/

%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files -n ruby-sqlite3
%defattr(-,root,root,-)
%{ruby_sitelib}/sqlite3.rb
%{ruby_sitelib}/sqlite3/


%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.4-4
- F-12: Rebuild to create valid debuginfo rpm again (ref: #505774)

* Tue Jun 16 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.4-3
- Create ruby-sqlite3 as subpackage (ref: #472621, #472622)
- Use gem as source

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 13 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.2.4-1
- Fix items from review (#459881)
- New upstream version

* Sun Aug 31 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.2.2-2
- Fix items from review (#459881)

* Sun Jul 13 2008 Matt Hicks <mhicks@localhost.localdomain> - 1.2.2-1
- Initial package
