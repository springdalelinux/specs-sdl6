# -------------------------------------------------------------------------- #
# Copyright 2002-2009, Distributed Systems Architecture Group, Universidad   #
# Complutense de Madrid (dsa-research.org)                                   #
#                                                                            #
# Licensed under the Apache License, Version 2.0 (the "License"); you may    #
# not use this file except in compliance with the License. You may obtain    #
# a copy of the License at                                                   #
#                                                                            #
# http://www.apache.org/licenses/LICENSE-2.0                                 #
#                                                                            #
# Unless required by applicable law or agreed to in writing, software        #
# distributed under the License is distributed on an "AS IS" BASIS,          #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
# See the License for the specific language governing permissions and        #
# limitations under the License.                                             #
#--------------------------------------------------------------------------- #

Summary: OpenNebula
Name: opennebula
Version: 3.0.0
Release: 1%{?dist}
License: Apache
Group: System
URL: http://opennebula.org

Source: opennebula-%{version}.tar.gz
Patch1: clvm.diff
Patch2: addclvm-3.0.0.diff
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: xmlrpc-c-devel, scons, sqlite-devel, mysql-devel
BuildRequires: ruby
Packager: OpenNebula Team <contact.org>

%description
OpenNebula is a Virtual Infrastructure Manager that orchestrates storage,
network and virtualization technologies to enable the dynamic placement of
multi-tier services (groups of interconnected virtual machines) on distributed
infrastructures, combining both data center resources and remote cloud
resources, according to allocation policies. OpenNebula provides internal and
Cloud administration and user interfaces for the full management of the Cloud
platform.

OpenNebula is free software released under the Apache License.

%prep
%setup -q -n opennebula-%{version}
%patch2 -p1 -b .addclvm
cd src/tm_mad
cp -ar lvm clvm
cd clvm
mv tm_lvm.conf tm_clvm.conf
mv tm_lvmrc tm_clvmrc
%patch1 -p6
perl -pi -e 's| lvm/| clvm/|' tm_clvm.conf
perl -pi -e 's|tm_lvmrc|tm_clvmrc|' tm*sh

%build
scons -j2 mysql=yes

%install
DESTDIR=%{buildroot} ./install.sh
mkdir -p %{buildroot}/etc/init.d
cp share/etc/init.d/oned.centos %{buildroot}/etc/init.d/oned

%clean
%{__rm} -rf %{buildroot}

%pre
mkdir -p /etc/one
mkdir -p /usr/lib/one
mkdir -p /usr/share/one
mkdir -p /var/lock/one
mkdir -p /var/log/one
mkdir -p /var/run/one

getent group oneadmin >/dev/null || groupadd -r oneadmin
if ! grep -q oneadmin /etc/passwd
then
	/usr/sbin/useradd -r -m -d /var/lib/one -g oneadmin -s /bin/bash oneadmin 2> /dev/null
else
    /usr/bin/gpasswd -a oneadmin oneadmin > /dev/null
fi

%post
if [ $1 = 1 ]; then
    /sbin/chkconfig --add oned >/dev/null
fi

%preun
if [ $1 = 0 ]; then
    /sbin/service oned stop >/dev/null
    /sbin/chkconfig --del oned >/dev/null
fi

%files
%defattr(-, root, root, 0755)
/etc/init.d/oned
%config /etc/one/ozones-server.conf
#config /etc/one/tm_nfs/tm_nfs.conf
#config /etc/one/tm_nfs/tm_nfsrc
%config /etc/one/tm_shared/tm_shared.conf
%config /etc/one/tm_shared/tm_sharedrc
%config /etc/one/tm_lvm/tm_lvm.conf
%config /etc/one/tm_lvm/tm_lvmrc
%config /etc/one/tm_clvm/tm_clvm.conf
%config /etc/one/tm_clvm/tm_clvmrc
%config /etc/one/defaultrc
%config /etc/one/oned.conf
%config /etc/one/econe.conf
%config /etc/one/vmm_ec2/vmm_ec2rc
%config /etc/one/vmm_ec2/vmm_ec2.conf
%config /etc/one/vmm_exec/vmm_exec_kvm.conf
%config /etc/one/vmm_exec/vmm_execrc
%config /etc/one/vmm_exec/vmm_exec_xen.conf
%config /etc/one/sunstone-plugins.yaml
%config /etc/one/acctd.conf
%config /etc/one/im_ec2/im_ec2.conf
%config /etc/one/im_ec2/im_ec2rc
%config /etc/one/hm/hmrc
%config /etc/one/occi-server.conf
%config /etc/one/group.default
%config /etc/one/occi_templates/medium.erb
%config /etc/one/occi_templates/large.erb
%config /etc/one/occi_templates/custom.erb
%config /etc/one/occi_templates/small.erb
%config /etc/one/occi_templates/common.erb
%config /etc/one/sunstone-server.conf
%config /etc/one/tm_ssh/tm_sshrc
%config /etc/one/tm_ssh/tm_ssh.conf
%config /etc/one/tm_dummy/tm_dummy.conf
%config /etc/one/tm_dummy/tm_dummyrc
%config /etc/one/auth/server_auth.conf
%config /etc/one/auth/quota.conf
%config /etc/one/auth/x509_auth.conf
%config /etc/one/ec2query_templates/m1.small.erb
%config /etc/one/cli/onevm.yaml
%config /etc/one/cli/onehost.yaml
%config /etc/one/cli/onevnet.yaml
%config /etc/one/cli/oneimage.yaml
%config /etc/one/cli/oneacl.yaml
%config /etc/one/cli/onetemplate.yaml
%config /etc/one/cli/oneuser.yaml
%config /etc/one/cli/onegroup.yaml
/usr/bin/*
/usr/include
/usr/lib/one
/usr/share/one
%doc /usr/share/man/man1/
%defattr(-, oneadmin, oneadmin, 0755)
%dir /var/lib/one
/var/lib/one/remotes
/var/lock/one
/var/log/one
/var/run/one
%defattr(-, oneadmin, oneadmin, 3770)
/var/lib/one/images


