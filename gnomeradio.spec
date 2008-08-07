%define name	gnomeradio
%define version	1.7
%define cvs	%{nil}

Summary:	A FM-Tuner program for Gnome
Name:		%{name}
Version:	%{version}
Release:	%mkrel 2
License:	GPLv2+
Group:		Sound
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}_16.png
Source2:	%{name}_32.png
Source3:	%{name}_48.png
Patch0: fix_missing_description_in_gnomeradio.xml.patch
Patch1: GLib_threading.patch
Patch2: gnomeradio.desktop.patch
Patch3: trayicon.c.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
URL:		http://mfcn.ilo.de/gnomeradio/
BuildRequires:	pkgconfig
BuildRequires:	libgnomeui2-devel
BuildRequires:	scrollkeeper
BuildRequires:	liblirc-devel
BuildRequires:	gnome-common
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	perl-XML-Parser
BuildRequires:	desktop-file-utils
BuildRequires:	libcddb-slave2-devel
BuildRequires:  libgstreamer-plugins-base-devel
BuildRequires:  gnome-doc-utils

%description
Gnomeradio is a FM radio tuner for the GNOME desktop.
It should work with every FM tuner card that is supported
by video4linux. Remote controls are supported via
lirc-support. Gnomeradio can also record radio as Wave,
MP3 or Ogg files.


%prep
%setup -q -n %{name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure2_5x
make

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL


desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Sound" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


install -d %buildroot/%_miconsdir
install -d %buildroot/%_liconsdir
install -d %buildroot/%_iconsdir

install -m644 %{SOURCE1} %buildroot/%_miconsdir/%{name}.png
install -m644 %{SOURCE2} %buildroot/%_iconsdir/%{name}.png
install -m644 %{SOURCE3} %buildroot/%_liconsdir/%{name}.png

# Are these needed?
rm -rf %buildroot/var/lib/scrollkeeper/*

%{find_lang} %{name}

%if %mdkversion < 200900
%post
%update_menus
%update_scrollkeeper
%post_install_gconf_schemas %name
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas %name

%if %mdkversion < 200900
%postun
%clean_menus
%clean_scrollkeeper
%clean_icon_cache hicolor
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS ChangeLog README.lirc README.recording TODO
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/gnomeradio.schemas
%{_datadir}/applications/gnomeradio.desktop
%dir %{_datadir}/omf/gnomeradio
%{_datadir}/omf/gnomeradio/gnomeradio-C.omf
%dir %{_datadir}/gnome/help/gnomeradio
%{_datadir}/gnome/help/gnomeradio/C/*
%{_datadir}/gnome/help/gnomeradio/sv/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/icons/hicolor/*
%{_datadir}/omf/gnomeradio/gnomeradio-sv.omf
