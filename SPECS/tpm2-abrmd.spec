%global selinuxtype targeted

Name: tpm2-abrmd
Version: 2.4.0
Release: 3%{?dist}
Summary: A system daemon implementing TPM2 Access Broker and Resource Manager

License: BSD
URL:     https://github.com/tpm2-software/tpm2-abrmd
Source0: https://github.com/tpm2-software/tpm2-abrmd/releases/download/%{version}/%{name}-%{version}.tar.gz

%{?systemd_requires}
BuildRequires: make
BuildRequires: systemd
BuildRequires: libtool
BuildRequires: autoconf-archive
BuildRequires: pkgconfig(cmocka)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(tss2-mu)
BuildRequires: pkgconfig(tss2-sys)
# tpm2-abrmd depends on tpm2-tss-devel for tss2-mu/sys libs
BuildRequires: tpm2-tss-devel >= 2.4.0

# tpm2-abrmd depends on the package that contains its SELinux policy module
Requires: (%{name}-selinux >= 2.0.0-1%{?dist} if selinux-policy-%{selinuxtype})

%description
tpm2-abrmd is a system daemon implementing the TPM2 access broker (TAB) and
Resource Manager (RM) spec from the TCG.

%package devel
Summary: Headers, static libraries and package config files of tpm2-abrmd
Requires: %{name}%{_isa} = %{version}-%{release}
# tpm2-abrmd-devel depends on tpm2-tss-devel for tss2-mu/sys libs
Requires: tpm2-tss-devel%{?_isa} >= 2.4.0

%description devel
This package contains headers, static libraries and package config files
required to build applications that use tpm2-abrmd.


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
rm -f %{buildroot}/%{_presetdir}/tpm2-abrmd.preset

%pre
getent group tss >/dev/null || groupadd -f -g 59 -r tss
if ! getent passwd tss >/dev/null ; then
    if ! getent passwd 59 >/dev/null ; then
      useradd -r -u 59 -g tss -d /dev/null -s /sbin/nologin -c "Account used for TPM access" tss
    else
      useradd -r -g tss -d /dev/null -s /sbin/nologin -c "Account used for TPM access" tss
    fi
fi
exit 0

%post
%systemd_post tpm2-abrmd.service

%preun
%systemd_preun tpm2-abrmd.service

%postun
%systemd_postun tpm2-abrmd.service

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_libdir}/libtss2-tcti-tabrmd.so.*
%{_sbindir}/tpm2-abrmd
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/tpm2-abrmd.conf
%{_datarootdir}/dbus-1/system-services/com.intel.tss2.Tabrmd.service
%{_unitdir}/tpm2-abrmd.service
%{_mandir}/man3/Tss2_Tcti_Tabrmd_Init.3*
%{_mandir}/man7/tss2-tcti-tabrmd.7*
%{_mandir}/man8/tpm2-abrmd.8*

%files devel
%{_includedir}/tss2/tss2-tcti-tabrmd.h
%{_libdir}/libtss2-tcti-tabrmd.so
%{_libdir}/pkgconfig/tss2-tcti-tabrmd.pc


%changelog
* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 2.4.0-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 2.4.0-2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Feb 09 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 29 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2.3.3-1
- Update to 2.3.3

* Wed Aug 05 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2.3.2-3
- Rebuild for tpm2-tss 3.0.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 04 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2 release

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Sun Yunying <yunying.sun@intel.com> - 2.3.1-1
- Update to 2.3.1 release

* Mon Nov 18 2019 Sun Yunying <yunying.sun@intel.com> - 2.3.0-1
- Update to 2.3.0 release
- Update dependency to tpm2-tss-devel version

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Sun Yunying <yunying.sun@intel.com> - 2.2.0-1
- Update to 2.2.0 release
- Update .gitignore to exclude source tar ball no matter versions

* Mon Mar 11 2019 Sun Yunying <yunying.sun@intel.com> - 2.1.1-1
- Update to 2.1.1 release

* Wed Mar 06 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.1.0-3
- Remove obsolete scriptlets

* Mon Feb 11 2019 Jerry Snitselaar <jsnitsel@redhat.com> - 2.1.0-2
- Fix tpm2-abrmd-selinux requires

* Mon Feb 11 2019 Sun Yunying <yunying.sun@intel.com> - 2.1.0-1
- Update to 2.1.0 release

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 4 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.0.3-2
- Remove tpm2-abrmd preset file
  Resolves: rhbz#1663124

* Wed Nov 7 2018 Sun Yunying <yunying.sun@intel.com> - 2.0.3-1
- Update to 2.0.3 release
- Remove gdbus related patch and autoreconf scriptlet as it's included in 2.0.3

* Tue Oct 16 2018 Sun Yunying <yunying.sun@intel.com> - 2.0.2-1
- Update to 2.0.2 release
- Add patch to fix configure error, also add autoreconf to update configure

* Tue Aug 14 2018 Sun Yunying <yunying.sun@intel.com> - 2.0.1-1
- Update to 2.0.1 release
- Remove the tcti SONAME patch since it's already included in 2.0.1
- Update dependency of tpm2-abrmd-selinux to fixed version instead dynamic one

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
