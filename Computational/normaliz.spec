Name:           normaliz
Version:        2.2
Release:        3%{?dist}
Summary:        A tool for mathematical computations

Group:          Applications/Engineering
License:        GPLv3
URL:            http://www.mathematik.uni-osnabrueck.de/normaliz/
# Warning: This zip-ball contains binaries, source only zip-ball not
# available
Source0:        http://www.mathematik.uni-osnabrueck.de/normaliz/Normaliz%{version}Linux64.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gmp-devel

%description
Normaliz is a (command line) tool for computations in affine
monoids, vector configurations, lattice polytopes,  and rational
cones.

Documentation and examples can be found in %{_docdir}/%{name}-%{version}, 
in particular you may find Normaliz%{version}Documentation.pdf useful.  
An example configuration file normaliz.cfg is also included.

%prep
%setup -q -n Normaliz%{version}Linux
# Delete the compiled version
rm -f norm32 norm64 normbig

%build
pushd source
# We want to use our build flags
sed -i 's/^\(CXXFLAGS\s*=\)/#\1/' Makefile
# Static linking should be avoided
sed -i 's/^\(N[A-Z0-9]*FLAGS\s*=.*\s\)-static/\1/' Makefile

CXXFLAGS="%{optflags}" \
make %{?_smp_mflags}
popd

mkdir -p docs/example

# Correct the end of line encodings for use on Linux
pushd example
for file in *.out *.in 
do
    sed 's/\r//' "$file" > "../docs/example/$file"
    touch -r "$file" "../docs/example/$file"
done
popd

mv doc/Normaliz%{version}Documentation.pdf docs
mv "doc/Computing the integral closure of an affine semigroup.pdf" \
    docs/Computing_the_integral_closure_of_an_affine_semigroup.pdf

sed -i 's/\r//' normaliz.cfg

%install
rm -rf %{buildroot}

pushd source
mkdir -p %{buildroot}%{_bindir}
install -m 755 norm32 %{buildroot}%{_bindir}
install -m 755 norm64 %{buildroot}%{_bindir}
install -m 755 normbig %{buildroot}%{_bindir}
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%doc docs/*
%doc normaliz.cfg
%{_bindir}/norm32
%{_bindir}/norm64
%{_bindir}/normbig

%changelog
* Thu Feb 25 2010 Mark Chappell <tremble@fedoraproject.org> - 2.2-3
- Preserve timestamps on examples
- Ensure that the first command in install is to wipe the buildroot
- Tweak to description

* Thu Feb 25 2010 Mark Chappell <tremble@fedoraproject.org> - 2.2-2
- Move examples into a subdirectory
- Correct inconsistant use of macros
- Provide a reference to the documentation in the description

* Wed Feb 24 2010 Mark Chappell <tremble@fedoraproject.org> - 2.2-1
- Initial build
