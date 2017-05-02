Name:    lxqt-common
Summary: Common resources for LXQt desktop suite
Version: 0.11.2
Release: 7%{?dist}
License: LGPLv2+
URL:     http://lxqt.org
BuildArch: noarch
Source0: https://github.com/lxde/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz
Source1: lxqt-theme-fedberry.tar.xz
Patch0:  %{name}-fedberry-defaults.patch
Patch1:  %{name}-missing-entry.patch
Patch2:  %{name}-policykit-libexec.patch
Patch3:  %{name}-menu-redhat.patch

BuildRequires: liblxqt-devel
BuildRequires: lxqt-build-tools
BuildRequires: pkgconfig(Qt5Xdg)
BuildRequires: pkgconfig(Qt5Help)
BuildRequires: kf5-kwindowsystem-devel >= 5.5
BuildRequires: desktop-file-utils

Requires: breeze-cursor-theme
Requires: oxygen-icon-theme

%if 0%{?fedora}
Requires: redhat-menus
Requires: fedberry-logos
Requires: desktop-backgrounds-compat
Requires: lxqt-theme
%endif

Requires: dbus-x11

# rhbz#1252581 - Panel does not show main menu entries
Requires: lxmenu-data

%description
%{summary}.

%package -n lxqt-theme-fedberry
Summary: Default FedBerry theme for LXQt
Provides: lxqt-theme = %{version} 

%description -n lxqt-theme-fedberry
%{summary}.


%prep
%setup -q
%if 0%{?fedora}
%patch0 -p1
%endif
%patch1 -p1 -b .missing
%patch2 -p1 -b .policykit
%if 0%{?fedora}
%patch3 -p1 -b .menu-redhat
%endif

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
    %{cmake_lxqt} ..
popd
%make_build -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
for desktop in %{buildroot}%{_sysconfdir}/xdg/autostart/*.desktop; do
	desktop-file-edit --remove-only-show-in=LXQt --add-only-show-in=X-LXQt ${desktop}
done
# FedBerry theme
pushd %{buildroot}/%{_datadir}/lxqt/themes/ 
	tar	xfJ %{SOURCE1}
popd

%check
desktop-file-validate %{buildroot}/%{_datadir}/xsessions/lxqt.desktop


%posttrans
update-desktop-database -q &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
update-desktop-database -q &> /dev/null || :
fi


%files
%{_bindir}/startlxqt
%dir %{_sysconfdir}/xdg/lxqt
%{_sysconfdir}/xdg/autostart/lxqt-*
%config(noreplace) %{_sysconfdir}/xdg/lxqt/*
%{_datadir}/xsessions/lxqt.desktop
%dir %{_sysconfdir}/xdg/pcmanfm-qt
%config(noreplace) %{_sysconfdir}/xdg/pcmanfm-qt/lxqt/settings.conf
%dir %{_datadir}/lxqt
%{_datadir}/lxqt/themes
%{_datadir}/lxqt/graphics
%{_datadir}/desktop-directories/lxqt-settings.directory
%{_sysconfdir}/xdg/menus/lxqt-applications.menu
%{_sysconfdir}/xdg/openbox/lxqt-rc.xml
%{_datadir}/desktop-directories/lxqt-leave.directory
%{_datadir}/icons/hicolor/*/*/*
%if 0%{?fedora}
%exclude %{_datadir}/lxqt/themes/fedberry
%endif
%exclude %{_datadir}/kdm/sessions/lxqt.desktop
%if 0%{?fedora}
%files -n lxqt-theme-fedberry
%dir %{_datadir}/lxqt/themes/fedberry
%{_datadir}/lxqt/themes/fedberry/*
%endif
%{_mandir}/man1/startlxqt.*


%changelog
* Tue May 02 2017 Vaughan <devel at agrez.net> - 0.11.2-7
- Default to using breeze icon theme

* Fri Apr 28 2017 Vaughan <devel at agrez.net> - 0.11.2-6
- Update defaults for pcmanfm-qt

* Mon Apr 17 2017 Vaughan <devel at agrez.net> - 0.11.2-5
- More updates to fedberry defaults patch

* Thu Apr 13 2017 Vaughan <devel at agrez.net> - 0.11.2-4
- Update fedberry defaults patch

* Sat Feb 04 2017 Vaughan <devel at agrez.net> - 0.11.2-3
- Bump release to keep above fedora releases

* Sat Feb 04 2017 Vaughan <devel at agrez.net> - 0.11.2-1
- New release
- Add buildrequires for lxqt-build-tools
- Add requires for breeze-cursor-theme
- Drop version from patch names

* Tue Oct 18 2016 Vaughan <devel at agrez.net> - 0.11-3
- Move lxqt-rc.xml to main package
- Update fedberry defaults patch

* Sun Oct 16 2016 Vaughan <devel at agrez.net> - 0.11-2
- Bump release & rebuild

* Sun Oct 16 2016 Vaughan <devel at agrez.net> - 0.11-1
- New release
- Update/refactor patches

* Mon Sep 19 2016 Vaughan <devel at agrez.net> - 0.10-15
- Update fedberry defaults patch

* Tue Sep 13 2016 Vaughan <devel at agrez.net> - 0.10-14
- More fedberry defaults fixes / updates

* Wed Sep 07 2016 Vaughan <devel at agrez.net> - 0.10-13
- Update fedberry defaults patch

* Wed Sep 07 2016 Vaughan <devel at agrez.net> - 0.10-12
- Add fedberry lxqt theme (source1)
- Update defaults

* Fri Aug 26 2016 Vaughan <devel at agrez.net> - 0.10-11
- Bump release
- Sync with upstream package changes
  * lxqt.conf: add fixedFont=Monospace (#1330150)
  * drop explicit BR: cmake (dep pulled in via use of %%cmake_lxqt macro)

* Wed Feb 10 2016 Vaughan <devel at agrez.net> - 0.10-9
- Sync with upstream package changes
  * fix empty panel menu, rhbz#1252581
  * fix menu patch
  * patch for RedHat special submenu Administration, rhbz#1217565
  * add Requires: redhat-menus for the Administration category
  * restructure for better readability
  * add BR: cmake
- Bump release
  
* Wed Dec 30 2015 Vaughan <devel at agrez.net> - 0.10-6
- Drop Requires for fedora-logos (it breaks 'generic' remixes)
- Drop Requires for lxqt-theme
- Update fedora_defaults patch
  * don't default to fedora's theme
  * default terminal commands now use qterminal-qt5

* Sun Dec 13 2015 Helio Chissini de Castro <helio@kde.org> - 0.10.1-5
- Use regular theme under epel for now

* Tue Dec 08 2015 Helio Chissini de Castro <helio@kde.org> - 0.10.1-3
- Prepare to epel7 with new cmake3

* Thu Nov 26 2015 Helio Chissini de Castro <helio@kde.org> - 0.10.1-2
- Missing proper path on policykit .desktop file. This causes the daemon not starts

* Mon Nov 02 2015 Helio Chissini de Castro <helio@kde.org> - 0.10.1-1
- New upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.1-4
- Avoid show in DM if no lxqt-session is available. Thanks to Rex Dieter

* Sat Feb 28 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.1-3
- Fixed xdg entriy preventing session to load proper lxqt resources
- Added Fedora theme and make it default

* Wed Feb 18 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.1-2
- Rebuild (gcc5)

* Sun Feb 15 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.1-1
- New 0.9 series patch release to fix issues related to 0.9.0.

* Wed Feb 11 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.0-5
- Assign ownership of %%{_datadir}/lxqt

* Tue Feb 10 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.0-4
- startlxqt tries to launch dbus-session, so it need requires dbus-x11

* Tue Feb 10 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.0-3
- Major theme issue on 0.9.0 tarball. Recreated from fix master git.

* Sun Feb 08 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.0-2
- Missing upstream files during the tarball release

* Sun Feb 08 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.0-1
- New upstream release 0.9.0

* Tue Feb 03 2015 Helio Chissini de Castro <hcastro@redhat.com> - 0.9.0-0.1
- Preparing 0.9.0

* Mon Dec 29 2014 Helio Chissini de Castro <hcastro@redhat.com> - 0.8.0-10
- Rebuild against new Qt 5.4.0

* Mon Dec 22 2014 Helio Chissini de Castro <hcastro@redhat.com> - 0.8.0-9
- Validate XDG desktop entry. Reenable regular sessions

* Fri Dec 19 2014 Helio Chissini de Castro <hcastro@redhat.com> - 0.8.0-8
- Unify naming as discussed on Fedora IRC

* Fri Dec 19 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.8.0-7
- fix lxqt-policykit autostart (moved to libexec)
- don't mark autostart as %%config

* Mon Nov 10 2014 Helio Chissini de Castro <hcastro@redhat.com> - 0.8.0-6
- For some reason Xdg went away on buildreqs.

* Mon Nov 10 2014 Helio Chissini de Castro <hcastro@redhat.com> - 0.8.0-5
- Validate desktop files adding X- since is not a valif group on freedesktop yet
- Owns xdg/lxqt directory

* Mon Nov 10 2014 Helio Chissini de Castro <hcastro@redhat.com> - 0.8.0-4
- Fix review issues on https://bugzilla.redhat.com/show_bug.cgi?id=1158632
- Moved fedora theme package away as agreed nee to be in a separate package

* Thu Oct 30 2014 Helio Chissini de Castro <hcastro@redhat.com> - 0.8.0-3
- Borrowed an upstream patch for XDG. Thanks to Florian Hubbold from Mageia

* Wed Oct 29 2014 Helio Chissini de Castro <hcastro@redhat.com> - 0.8.0-2
- Small modification to submit package for review

* Mon Oct 27 2014 Helio Chissini de Castro <hcastro@redhat.com> - 0.8.0-1
- First release to LxQt new base
