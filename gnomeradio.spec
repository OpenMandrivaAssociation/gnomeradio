%define name	gnomeradio
%define version	1.8

Summary:	A FM-Tuner program for Gnome
Name:		%{name}
Version:	%{version}
Release:	%mkrel 5
License:	GPLv2+
Group:		Sound
Source0:	http://www.wh-hms.uni-ulm.de/~mfcn/gnomeradio/packages/%{name}-%{version}.tar.gz
Patch0:		gnomeradio-1.8-description.patch
Patch1:		gnomeradio-1.8-glib-threading.patch
Patch4:		gnomeradio-1.8-fix-str-fmt.patch
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
%patch4 -p1

%build
%configure2_5x --disable-scrollkeeper --disable-install-schemas
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Audio;Tuner" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%{find_lang} %{name} --with-gnome

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
%lang(es) %{_datadir}/omf/%{name}/gnomeradio-es.omf
%lang(fr) %{_datadir}/omf/%{name}/gnomeradio-fr.omf
%lang(oc) %{_datadir}/omf/%{name}/gnomeradio-oc.omf
%lang(sv) %{_datadir}/omf/gnomeradio/gnomeradio-sv.omf
%{_iconsdir}/hicolor/*/*/*
