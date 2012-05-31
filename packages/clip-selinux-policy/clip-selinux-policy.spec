%define distro redhat 
%define polyinstatiate n
%define monolithic n
%if %{?BUILD_TARGETED:0}%{!?BUILD_TARGETED:1}
%define BUILD_TARGETED 1
%endif
%if %{?BUILD_MLS:0}%{!?BUILD_MLS:1}
%define BUILD_MLS 1
%endif
%define POLICYVER 24
%define libsepolver 2.0.41-1
%define POLICYCOREUTILSVER 2.0.78-1
%define CHECKPOLICYVER 2.0.21-1
Name:   %{pkgname}
Version: %{version}
Release: %{release}
Summary: Certifiable Linux Integration Platform Policy configuration
Version: 4.0.0
Release: 0%{?dist}
License: GPLv2+
Group: System Environment/Base
Source: %{pkgname}-%{version}.tar.bz2

Url: http://oss.tresys.com/repos/refpolicy/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description 
Certifiable Linux Integration Platform SELinux Base package

%files 
%defattr(-,root,root,-)
%{_mandir}/man*/*
# policycoreutils owns these manpage directories, we only own the files within them
%{_mandir}/ru/*/*
%dir %{_usr}/share/selinux
%dir %{_usr}/share/selinux/devel
%dir %{_usr}/share/selinux/devel/include
%dir %{_usr}/share/selinux/packages
%dir %{_sysconfdir}/selinux
%ghost %config(noreplace) %{_sysconfdir}/selinux/config
%ghost %{_sysconfdir}/sysconfig/selinux
%{_usr}/share/selinux/devel/include/*
%{_usr}/share/selinux/devel/Makefile
%{_usr}/share/selinux/devel/policygentool
%{_usr}/share/selinux/devel/example.*
%{_usr}/share/selinux/devel/policy.*

%package doc
Summary: Certifiable Linux Integration Platform SELinux policy documentation
Group: System Environment/Base
Requires(pre): clip-selinux-policy = %{version}-%{release}
Requires: /usr/bin/xdg-open

%description doc
Certifiable Linux Integration Platform SELinux policy documentation package

%files doc
%defattr(-,root,root,-)
%doc %{_usr}/share/doc/%{name}-%{version}
%attr(755,root,root) %{_usr}/share/selinux/devel/policyhelp

%check
if /usr/sbin/selinuxenabled; then
/usr/bin/sepolgen-ifgen -i %{buildroot}%{_usr}/share/selinux/devel/include -o /dev/null 
fi

%define makeCmds() \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 bare \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024  conf \

%define installCmds() \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 base.pp \
make validate UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 modules \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 install \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 install-appconfig \
#%{__cp} *.pp %{buildroot}/%{_usr}/share/selinux/%1/ \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/policy \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/modules/active \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/contexts/files \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/booleans \
touch %{buildroot}%{_sysconfdir}/selinux/%1/seusers \
touch %{buildroot}%{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
install -m0644 config/setrans.conf %{buildroot}%{_sysconfdir}/selinux/%1/setrans.conf \
bzip2 %{buildroot}/%{_usr}/share/selinux/%1/*.pp \
awk '$1 !~ "/^#/" && $2 == "=" && $3 == "module" { printf "%%s.pp.bz2 ", $1 }' ./policy/modules.conf > %{buildroot}/%{_usr}/share/selinux/%1/modules.lst
%nil

%define fileList() \
%defattr(-,root,root) \
%dir %{_usr}/share/selinux/%1 \
%{_usr}/share/selinux/%1/*.pp.bz2 \
%{_usr}/share/selinux/%1/modules.lst \
%dir %{_sysconfdir}/selinux/%1 \
%config(noreplace) %{_sysconfdir}/selinux/%1/setrans.conf \
%ghost %{_sysconfdir}/selinux/%1/seusers \
%dir %{_sysconfdir}/selinux/%1/modules \
%verify(not mtime) %{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
%verify(not mtime) %{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
%attr(700,root,root) %dir %{_sysconfdir}/selinux/%1/modules/active \
#%verify(not md5 size mtime) %attr(600,root,root) %config(noreplace) %{_sysconfdir}/selinux/%1/modules/active/seusers \
%dir %{_sysconfdir}/selinux/%1/policy/ \
%ghost %{_sysconfdir}/selinux/%1/policy/policy.* \
%dir %{_sysconfdir}/selinux/%1/contexts \
%config %{_sysconfdir}/selinux/%1/contexts/customizable_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/securetty_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/dbus_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/x_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/default_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/sepgsql_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_type \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/failsafe_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/initrc_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/removable_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/userhelper_context \
%dir %{_sysconfdir}/selinux/%1/contexts/files \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
%config %{_sysconfdir}/selinux/%1/contexts/files/media \
%dir %{_sysconfdir}/selinux/%1/contexts/users \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/root \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/guest_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/xguest_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/user_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/staff_u 

%define saveFileContext() \
if [ -s /etc/selinux/config ]; then \
     . %{_sysconfdir}/selinux/config; \
     FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
     if [ "${SELINUXTYPE}" = %1 -a -f ${FILE_CONTEXT} ]; then \
        [ -f ${FILE_CONTEXT}.pre ] || cp -f ${FILE_CONTEXT} ${FILE_CONTEXT}.pre; \
     fi \
fi

%define loadpolicy() \
. %{_sysconfdir}/selinux/config; \
( cd /usr/share/selinux/%1; semodule -n -b base.pp.bz2 -i %2 -s %1 2>&1 ); \

%define relabel() \
. %{_sysconfdir}/selinux/config; \
FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
selinuxenabled; \
if [ $? = 0  -a "${SELINUXTYPE}" = %1 -a -f ${FILE_CONTEXT}.pre ]; then \
     fixfiles -C ${FILE_CONTEXT}.pre restore; \
     restorecon -R /root /var/log /var/run 2> /dev/null; \
     rm -f ${FILE_CONTEXT}.pre; \
fi; 

%description
Certifiable Linux Integration Platform SELinux Reference Policy - modular.

%build

%prep 
%setup -q

%install
# Build clip policy
%{__rm} -fR %{buildroot}
mkdir -p %{buildroot}%{_mandir}
cp -R  man/* %{buildroot}%{_mandir}
mkdir -p %{buildroot}%{_sysconfdir}/selinux
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/selinux/config
touch %{buildroot}%{_sysconfdir}/sysconfig/selinux

# Always create policy module package directories
mkdir -p %{buildroot}%{_usr}/share/selinux/{clip,mls,modules}/

# Install devel
make clean
%if %{BUILD_TARGETED}
# Build clip policy
%makeCmds clip mcs n y allow
%installCmds clip mcs n y allow
%endif

%if %{BUILD_MLS}
# Build mls policy
%makeCmds mls mls n y deny
%installCmds mls mls n y deny
%endif

make UNK_PERMS=allow NAME=clip TYPE=mcs DISTRO=%{distro} UBAC=n DIRECT_INITRC=n MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} PKGNAME=%{name}-%{version} POLY=y MLS_CATS=1024 MCS_CATS=1024 install-headers install-docs
mkdir %{buildroot}%{_usr}/share/selinux/devel/
mkdir %{buildroot}%{_usr}/share/selinux/packages/
mv %{buildroot}%{_usr}/share/selinux/clip/include %{buildroot}%{_usr}/share/selinux/devel/include
install -m 644 config/Makefile.devel %{buildroot}%{_usr}/share/selinux/devel/Makefile
install -m 644 doc/example.* %{buildroot}%{_usr}/share/selinux/devel/
install -m 644 doc/policy.* %{buildroot}%{_usr}/share/selinux/devel/
echo  "xdg-open file:///usr/share/doc/clip-selinux-policy-%{version}/html/index.html"> %{buildroot}%{_usr}/share/selinux/devel/policyhelp
chmod +x %{buildroot}%{_usr}/share/selinux/devel/policyhelp
%clean
%{__rm} -fR %{buildroot}

%post
if [ ! -s /etc/selinux/config ]; then
#
#     New install so we will default to clip policy
#
echo "
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of these two values:
#     clip - Targeted processes are protected,
#     mls - Multi Level Security protection.
SELINUXTYPE=clip 

" > /etc/selinux/config

     ln -sf ../selinux/config /etc/sysconfig/selinux 
     restorecon /etc/selinux/config 2> /dev/null || :
else
     . /etc/selinux/config
     # if first time update booleans.local needs to be copied to sandbox
     [ -f /etc/selinux/${SELINUXTYPE}/booleans.local ] && mv /etc/selinux/${SELINUXTYPE}/booleans.local /etc/selinux/clip/modules/active/
     [ -f /etc/selinux/${SELINUXTYPE}/seusers ] && cp -f /etc/selinux/${SELINUXTYPE}/seusers /etc/selinux/${SELINUXTYPE}/modules/active/seusers
fi
exit 0

%postun
if [ $1 = 0 ]; then
     setenforce 0 2> /dev/null
     if [ ! -s /etc/selinux/config ]; then
          echo "SELINUX=disabled" > /etc/selinux/config
     else
          sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config
     fi
fi
exit 0

%if %{BUILD_TARGETED}
%package clip
Summary: Certifiable Linux Integration Platform SELinux clip base policy
Provides: clip-selinux-policy-base = %{version}-%{release}
Group: System Environment/Base
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): clip-selinux-policy = %{version}-%{release}
Requires: clip-selinux-policy = %{version}-%{release}
Conflicts:  audispd-plugins <= 1.7.7-1
Conflicts:  seedit

%description clip
Certifiable Linux Integration Platform policy clip base module.
Based off of reference policy refpolicy-2.20110726.tar.bz2

%pre clip
%saveFileContext clip

%post clip
packages=`cat /usr/share/selinux/clip/modules.lst`
if [ $1 -eq 1 ]; then
   %loadpolicy clip $packages
   restorecon -R /root /var/log /var/run 2> /dev/null
else
   semodule -n -s clip 2>/dev/null
   %loadpolicy clip $packages
   %relabel clip
fi
exit 0

%files clip
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/selinux/clip/contexts/users/unconfined_u
%fileList clip
%endif

%if %{BUILD_MLS}
%package mls 
Summary: Certifiable Linux Integration Platform SELinux mls base policy
Group: System Environment/Base
Provides: clip-selinux-policy-base = %{version}-%{release}
Requires: policycoreutils-newrole >= %{POLICYCOREUTILSVER} setransd
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): clip-selinux-policy = %{version}-%{release}
Requires: clip-selinux-policy = %{version}-%{release}
Conflicts:  seedit

%description mls 
Certifiable Linux Integration Platform policy mls base module.
Based off of reference policy refpolicy-2.20110726.tar.bz2

%pre mls 
%saveFileContext mls

%post mls 
semodule -n -s mls 2>/dev/null
packages=`cat /usr/share/selinux/mls/modules.lst`
%loadpolicy mls $packages

if [ $1 -eq 1 ]; then
   restorecon -R /root /var/log /var/run 2> /dev/null
else
%relabel mls
fi
exit 0

%files mls
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/selinux/mls/contexts/users/unconfined_u
%fileList mls

%endif

%changelog
