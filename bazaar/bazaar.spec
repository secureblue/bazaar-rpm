# SPDX-FileCopyrightText: Copyright 2025 Tulip Blossom <tulilirockz@proton.me>
# SPDX-FileCopyrightText: Copyright 2025-2026 Kyle Gospodnetich <me@kylegospodneti.ch>
# SPDX-FileCopyrightText: Copyright 2026 The Secureblue Authors
#
# SPDX-License-Identifier: Apache-2.0

%global appid io.github.kolunmi.Bazaar
# renovate: datasource=github-tags depName=bazaar-org/bazaar currentValue=0.7.13
%global release_commit cf24df0aa7ccbbbe79a2089391668eb8fb6b99f0

Name:           bazaar
Version:        0.7.14
Release:        1%{?dist}
Summary:        Flatpak-centric software center and app store

License:        GPL-3.0-only
URL:            https://usebazaar.org/
Source:         https://github.com/bazaar-org/bazaar/archive/%{release_commit}.tar.gz
Patch0:         verified-apps-only.patch
Patch1:         recognize-verified-remote.patch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  systemd-rpm-macros
BuildRequires:  blueprint-compiler >= 0.20
BuildRequires:  desktop-file-utils
BuildRequires:  python3-babel
BuildRequires:  pkgconfig(gtk4) >= 4.22.1
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(xmlb)
BuildRequires:  pkgconfig(flatpak)
BuildRequires:  pkgconfig(libdex-1)
BuildRequires:  pkgconfig(yaml-0.1)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(glycin-2)
BuildRequires:  pkgconfig(glycin-gtk4-2)
BuildRequires:  pkgconfig(webkitgtk-6.0)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(md4c)
BuildRequires:  pkgconfig(libproxy-1.0)

%description
A new app store with a focus on discovering and installing
applications and add-ons from Flatpak remotes, particularly Flathub.
It emphasizes supporting the developers who make the Linux desktop possible.

%package devel
Summary:        Development files for the Bazaar GTK extensions
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for Bazaar GTK extensions

%prep
%autosetup -n %{name}-%{release_commit} -p1

%conf
%meson \
  -Dhardcoded_main_config_path=/usr/share/bazaar/main.yaml

%build
%meson_build

%install
%meson_install
%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop

%post
%systemd_user_post %{appid}.service

%preun
%systemd_user_preun %{appid}.service

%postun
%systemd_user_postun_with_restart %{appid}.service

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_datadir}/applications/%{appid}.desktop
%{_bindir}/%{name}
%{_bindir}/%{name}-dl-worker
%{_libdir}/libbge-0.1.so
%{_userunitdir}/%{appid}.service
%{_datadir}/dbus-1/services/%{appid}.service
%{_datadir}/glib-2.0/schemas/%{appid}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{appid}-symbolic.svg
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/gnome-shell/search-providers/%{appid}.search-provider.ini

%files devel
%{_libdir}/pkgconfig/bge-0.1.pc
%{_includedir}/bge/

%changelog
* Wed Apr 1 2026 Jill Fiore <contact@lumaeris.com>
- Update to version v0.7.13
- Specify GTK4 >= 4.22.1
- Add new dependency python3-babel

* Tue Mar 10 2026 alexvojproc <git@to.alexvp.net>
- Specify blueprint-compiler >= 0.20
- Add devel package for libbge (Bazaar GTK Extensions)

* Mon Jan 19 2026 alexvojproc <git@to.alexvp.net>
- Remove deprecated config paths and Universal Blue references
- Use commit hashes instead of release tags
- Add flathub-verified patches

* Tue Dec 30 2025 Kyle Gospodnetich <me@kylegospodneti.ch>
- Update to version v0.7.0

* Sun Aug 17 2025 Kyle Gospodnetich <me@kylegospodneti.ch>
- Update to version v0.3.1

* Sat May 17 2025 Tulip Blossom <tulilirockz@proton.me>
- Init package
