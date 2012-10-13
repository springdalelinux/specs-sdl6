Summary:	Use a Razor catalogue server to filter spam messages
Name:		perl-Razor-Agent
Version:	2.85
Release:	6%{?dist}
License:	Artistic 2.0
Group:		Applications/Internet
URL:		http://razor.sourceforge.net/
Source:		http://dl.sourceforge.net/razor/razor-agents-%{version}.tar.bz2
Patch0:         razor-agents-2.85-use-sha-not-sha1.patch
Requires:	perl(Net::DNS), perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:	perl(Net::DNS), perl(Digest::SHA1), perl(Time::HiRes), perl(URI), perl(ExtUtils::MakeMaker)
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Vipul's Razor is a distributed, collaborative, spam detection and
filtering network. Razor establishes a distributed and constantly
updating catalogue of spam in propagation. This catalogue is used
by clients to filter out known spam. On receiving a spam, a Razor
Reporting Agent (run by an end-user or a troll box) calculates and
submits a 20-character unique identification of the spam (a SHA
Digest) to its closest Razor Catalogue Server. The Catalogue Server
echos this signature to other trusted servers after storing it in its
database. Prior to manual processing or transport-level reception,
Razor Filtering Agents (end-users and MTAs) check their incoming mail
against a Catalogue Server and filter out or deny transport in case of
a signature match. Catalogued spam, once identified and reported by
a Reporting Agent, can be blocked out by the rest of the Filtering
Agents on the network.

%prep
%setup -q -n razor-agents-%{version}
%patch0 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS"
%{__perl} Makefile.PL INSTALLDIRS=vendor
cd Razor2-Preproc-deHTMLxs
%{__perl} Makefile.PL INSTALLDIRS=vendor
cd ..
make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"

# Package is lacking Artistic license
perldoc -t perlartistic > COPYING

%install
rm -rf $RPM_BUILD_ROOT

make install -C Razor2-Preproc-deHTMLxs \
  PERL_INSTALL_ROOT=$RPM_BUILD_ROOT \
  INSTALLARCHLIB=$RPM_BUILD_ROOT%{perl_archlib}
make install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT \
  PERL_INSTALL_ROOT=$RPM_BUILD_ROOT \
  INSTALLARCHLIB=$RPM_BUILD_ROOT%{perl_archlib} \
  INSTALLMAN5DIR=%{_mandir}/man5 \
  PERL5LIB=$RPM_BUILD_ROOT%{perl_vendorarch}

find $RPM_BUILD_ROOT -type f -a \( -name perllocal.pod -o -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc BUGS Changes COPYING CREDITS FAQ README SERVICE_POLICY
%{_bindir}/*
%{perl_vendorlib}/Razor2
%{perl_vendorlib}/auto/Razor2
%{perl_vendorarch}/Razor2
%{perl_vendorarch}/auto/Razor2
%{_mandir}/man*/*

%changelog
* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.85-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.85-5
- rebuild against perl 5.10.1

* Sun Nov 01 2009 Warren Togami <wtogami@redhat.com> - 2.85-4
- Use Digest::SHA instead of Digest::SHA1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 2.85-2
- Rebuilt against gcc 4.4 and rpm 4.6

* Wed Jul 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.85-1
- update to 2.85, relicensed to Artistic 2.0

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.84-4
- Rebuild for new perl

* Sun Feb 10 2008 Robert Scheck <robert@fedoraproject.org> 2.84-3
- Rebuilt against gcc 4.3

* Wed Aug 29 2007 Robert Scheck <robert@fedoraproject.org> 2.84-2
- Rebuilt (missing BuildID)

* Sat Aug 11 2007 Robert Scheck <robert@fedoraproject.org> 2.84-1
- Upgrade to 2.84 (#250869)
- Added build requirement to perl(ExtUtils::MakeMaker)

* Sat Sep 16 2006 Warren Togami <wtogami@redhat.com> - 2.82-1
- 2.82

* Thu Mar 16 2006 Warren Togami <wtogami@redhat.com> - 2.77-3
- rebuild for FC5

* Fri Nov 11 2005 Warren Togami <wtogami@redhat.com> - 2.77-2
- 2.77

* Fri Aug 05 2005 Warren Togami <wtogami@redhat.com> - 2.75-1
- 2.75

* Thu Jun 16 2005 Warren Togami <wtogami@redhat.com> - 2.71-1
- 2.71 and buildroot patch (#160629 mschwendt)

* Thu May 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.67-2
- Fix SMP build flags.

* Sun Feb 06 2005 Warren Togami <wtogami@redhat.com> 0:2.67-0.FC3
- 2.67

* Mon Mar 29 2004 Warren Togami <wtogami@redhat.com> 0:2.40-0.fdr.2
- #1428 man error patch0

* Sat Mar 27 2004 Warren Togami <wtogami@redhat.com> 0:2.40-0.fdr.1
- Update to 2.40
  no longer needs taintsafe patch
  no longer uses Digest-Nilsimsa
- Explicit Requires perl(Net::DNS) so razor-admin -register does not fail

* Sat Mar 13 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 0:2.36-0.fdr.7
- Don't create patch backup files as they would be included.
- Own fewer directories because Fedora Core perl package has been fixed.

* Sun Nov 30 2003 Warren Togami <warren@togami.com> - 0:2.36-0.fdr.6
- Add Nicolas ls bug workaround to fix FC1 build #377

* Sat Nov 29 2003 Warren Togami <warren@togami.com> - 0:2.36-0.fdr.5
- Add taint safe patch from spamassassin.org
- Add check macro workaround for rpm < 4.1.1

* Fri Sep 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.36-0.fdr.4
- Specfile cleanup, using vendor dirs, PERL_INSTALL_ROOT and INSTALLARCHLIB.

* Sun Aug 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.36-0.fdr.3
- Rewrite specfile, using fedora-rpm-helper.
- Use perl(XXX) -style dependencies.
- Drop seemingly spurious MailTools dependency.
- Update %%doc list.
- Run make test in %%check.
- Drop MDK specfile since we don't have much common with it any more.

* Sun Jun 15 2003 Warren Togami <warren@togami.com> - 2.34-0.fdr.2
- Apply anvil's fixes

* Sat Jun 14 2003 Warren Togami <warren@togami.com> - 2.34-0.fdr.1
- Minimal Fedora conversion attempt

* Wed Jun  4 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.34-2mdk
- Fix man install for Mdk 8.0

* Mon Jun  2 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.34-1mdk
- Release 2.34

* Mon May 12 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.22-2mdk
- isteamization (Mdk Linux 8.0) (Nicolas Chipaux)

* Sat Mar 29 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.22-1mdk
- Release 2.22

* Wed Oct 30 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.20-2mdk
- ISTEAM powered = add support for Mdk 8.0

* Tue Oct 29 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.20-1mdk
- Release 2.20

* Fri Sep 13 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.14-1mdk
- Release 2.14

* Fri Jul 12 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.12-1mdk
- From Ben Reser <ben@reser.org> :
 - Release 2.12

* Thu Jul 11 2002 Pixel <pixel@mandrakesoft.com> 2.08-5mdk
- drop the explicit depency on perl 5.6.1

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 2.08-4mdk
- handle man5 pages by hand
- rebuild for perl 5.8.0

* Thu Jun 27 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.08-3mdk
- Fix BuildRequires

* Tue Jun 18 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.08-2mdk
- Add missing depencency on perl-URI and perl-MIME-Base64

* Tue Jun 18 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.08-1mdk
- Release 2.0.8
- Remove patch0 (no longer needed)

* Tue Apr  9 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.20-1mdk
- First Mdk package

* Sun Jan 27 2002 Scott Pakin <pakin@uiuc.edu>
- Initial version
