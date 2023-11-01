%global selinuxtype targeted

Name: tpm2-abrmd
Version: 2.3.3
Release: 3%{?dist}
Summary: A system daemon implementing TPM2 Access Broker and Resource Manager

License: BSD
URL:     https://github.com/tpm2-software/tpm2-abrmd
Source0: https://github.com/tpm2-software/tpm2-abrmd/releases/download/%{version}/%{name}-%{version}.tar.gz

%{?systemd_requires}
BuildRequires: systemd
BuildRequires: libtool
BuildRequires: autoconf-archive
BuildRequires: pkgconfig(cmocka)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(tss2-mu)
BuildRequires: pkgconfig(tss2-sys)
# tpm2-abrmd depends on tpm2-tss-devel for tss2-mu/sys libs
BuildRequires: tpm2-tss-devel >= 2.3.1-2%{?dist}

Patch0: 0001-tabrmd-options-fix-memory-leak.patch
Patch1: 0002-resource-manager-rm-ref-count-inc-of-handle_entry.patch
Patch2: 0003-tabrmd-init.c-fix-leaks-on-main-to-thread-tpm2-insta.patch
Patch3: 0004-init_thread_func-fix-deadlock.patch
Patch4: 0005-ResourceManager-Avoid-double-free-in-resource-manage.patch
Patch5: 0006-tcti-initialize-GError-to-NULL.patch

# tpm2-abrmd depends on the package that contains its SELinux policy module
Requires: (%{name}-selinux >= 2.0.0-1%{?dist} if selinux-policy-%{selinuxtype})

%description
tpm2-abrmd is a system daemon implementing the TPM2 access broker (TAB) and
Resource Manager (RM) spec from the TCG.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure --disable-static --disable-silent-rules \
           --with-systemdsystemunitdir=%{_unitdir} \
           --with-systemdpresetdir=%{_presetdir}
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -type f -name \*.la -delete

%pre
getent group tss >/dev/null || groupadd -g 59 -r tss
getent passwd tss >/dev/null || \
useradd -r -u 59 -g tss -d /dev/null -s /sbin/nologin \
 -c "Account used by the tpm2-abrmd package to sandbox the tpm2-abrmd daemon" tss
exit 0

%files
%doc README.md CHANGELOG.md
%license LICENSE
%{_libdir}/libtss2-tcti-tabrmd.so.*
%{_sbindir}/tpm2-abrmd
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/tpm2-abrmd.conf
%{_datarootdir}/dbus-1/system-services/com.intel.tss2.Tabrmd.service
%{_unitdir}/tpm2-abrmd.service
%{_presetdir}/tpm2-abrmd.preset
%{_mandir}/man3/Tss2_Tcti_Tabrmd_Init.3.gz
%{_mandir}/man7/tss2-tcti-tabrmd.7.gz
%{_mandir}/man8/tpm2-abrmd.8.gz


%package devel
Summary: Headers, static libraries and package config files of tpm2-abrmd
Requires: %{name}%{_isa} = %{version}-%{release}
# tpm2-abrmd-devel depends on tpm2-tss-devel for tss2-mu/sys libs
Requires: tpm2-tss-devel%{?_isa} >= 2.0.0-1%{?dist}

%description devel
This package contains headers, static libraries and package config files
required to build applications that use tpm2-abrmd.

%files devel
%{_includedir}/tss2/tss2-tcti-tabrmd.h
%{_libdir}/libtss2-tcti-tabrmd.so
%{_libdir}/pkgconfig/tss2-tcti-tabrmd.pc

# on package installation
%post
/sbin/ldconfig
%systemd_post tpm2-abrmd.service

%preun
%systemd_preun tpm2-abrmd.service

%postun
/sbin/ldconfig
%systemd_postun tpm2-abrmd.service

%changelog
* Thu Aug 11 2022 Štěpán Horáček <shoracek@redhat.com> - 2.3.3-3
- Fix memory leaks and double free
  resolves: rhbz#2041912

* Mon Nov 23 2020 Jerry Snitselaar <jsnitsel@redhat.com> - 2.3.3-2
- Update tpm2-tss-devel BuildRequires
resolves: rhbz#1855177

* Wed Nov 11 2020 Jerry Snitselaar <jsnitsel@redhat.com> - 2.3.3-1
- Rebase to 2.3.3 release.
resolves: rhbz#1855177

* Tue May 28 2019 Jerry Snitselaar <jsnitsel@redhat.com> - 2.1.1-3
- Update CI gating to use test.
resolves: rhbz#1682416

* Tue May 14 2019 Jerry Snitselaar <jsnitsel@redhat.com> - 2.1.1-2
- Add initial CI gating.
resolves: rhbz#1682416

* Tue Apr 30 2019 Jerry Snitselaar <jsnitsel@redhat.com> - 2.1.1-1
- Rebase to release 2.1.1
resolves: rhbz#1664499

* Wed Feb 06 2019 Jerry Snitselaar <jsnitsel@redhat.com> - 2.0.0-3
- Fix tpm2-abrmd-selinux Requires
resolves: rhbz#1642000

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Javier Martinez Canillas <javierm@redhat.com> - 2.0.0-1
- Download the distributed tarball instead of the source code tarball
- Update URLs to point to the new project location
- Update to 2.0.0 release

* Fri Feb 23 2018 Javier Martinez Canillas <javierm@redhat.com> - 1.1.0-12
- Don't install udev rule for TPM character devices

* Wed Feb 21 2018 Javier Martinez Canillas <javierm@redhat.com> - 1.1.0-11
- Remove ExclusiveArch: x86_64 directive

* Thu Feb 15 2018 Javier Martinez Canillas <javierm@redhat.com> - 1.1.0-10
- Remove %%{_isa} from BuildRequires (RHBZ#1545210)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 25 2017 Peter Jones <pjones@redhat.com> - 1.1.0-8
- Make only tpm2-abrmd-devel have a runtime dep on tpm2-tools-devel

* Wed Oct 18 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 1.1.0-7
- tcti-abrmd: Fix null deref

* Fri Oct 13 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-6
- Add tss user if doesn't currently exist - PR#1 from Jerry Snitselaar
- Removed source tarball and cleared it from .gitignore

* Wed Aug 16 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-5
- Updated source0 URL to fix rpmlint warnings

* Tue Aug 15 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-4
- Rename and relocate udev rules file to _udevrulesdir
- Update scriptlet to add service name after systemd_postrun

* Tue Aug 1 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-3
- Use config option with-systemdsystemunitdir to set systemd unit file location

* Mon Jul 31 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-2
- Removed BuildRequires for gcc
- Move tpm2-abrmd systemd service to /usr/lib/systemd/system
- Added scriptlet for tpm2-abrmd systemd service
- Use autoreconf instead of bootstrap

* Wed Jul 26 2017 Sun Yunying <yunying.sun@intel.com> - 1.1.0-1
- Initial packaging
