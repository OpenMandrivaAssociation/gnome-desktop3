%define oname gnome-desktop
%define	api_version 3
%define api 3.0
%define lib_major   0
%define libname	%mklibname %{oname}-%{api_version}_ %{lib_major}
%define libnamedev %mklibname -d %{oname}-%{api_version}

%define req_startup_notification_version 0.5
Summary:          Package containing code shared among gnome-panel, gnome-session, nautilus, etc
Name: %{oname}3
Version: 3.0.1
Release: %mkrel 1
License:          GPLv2+ and LGPLv2+
Group:            Graphical desktop/GNOME
Source0:          http://ftp.gnome.org/pub/GNOME/sources/gnome-desktop/%{oname}-%{version}.tar.bz2
BuildRoot:        %{_tmppath}/%{oname}-%{version}-root
URL:              http://www.gnome.org
BuildRequires: startup-notification-devel >= 0.5
BuildRequires: gtk+3-devel >= 3.0
BuildRequires: glib2-devel >= 2.19.1
BuildRequires: libgdk_pixbuf2.0-devel >= 2.21.3
BuildRequires: gtk-doc
BuildRequires: scrollkeeper
BuildRequires: gnome-doc-utils >= 0.3.2
BuildRequires: gsettings-desktop-schemas-devel >= 0.1.4
BuildRequires: gobject-introspection-devel >= 0.9.7
BuildRequires: libxslt-proc
BuildRequires: intltool >= 0.40.0
BuildRequires: ldetect-lst
Requires: ldetect-lst >= 0.1.282
Obsoletes: %{name}-common < 2.91.92
Conflicts: gnome-desktop-common < %{version}

%description
This package contains some data files and other shared components of the
GNOME user environment.

%package -n %{libname}
Summary:	%{summary}
Group:		System/Libraries
Requires:   %{name} >= %{version}-%{release}
Provides:	%{oname}-%{api_version} = %{version}-%{release}
Requires: libstartup-notification-1 >= %{req_startup_notification_version}

%description -n %{libname}
This package contains an internal library
(libgnomedesktop) used to implement some portions of the GNOME
desktop.

%package -n %{libnamedev}
Summary:	Static libraries, include files for gnome-desktop
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{oname}-%{api_version}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:   libstartup-notification-1-devel >= %{req_startup_notification_version}

%description -n %{libnamedev}
Static libraries, include files for internal library libgnomedesktop.

%prep
%setup -qn %oname-%version

%build
%configure2_5x --with-gnome-distributor="%vendor" --disable-scrollkeeper --with-pnp-ids-path=%{_datadir}/misc/pnp.ids
%make

%install
rm -rf $RPM_BUILD_ROOT *.lang

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std 
%find_lang %{oname}-%api
for omf in %buildroot%_datadir/omf/*/{*-??.omf,*-??_??.omf,*-???.omf};do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %oname-%api.lang
done
for d in `ls -1 %buildroot%_datadir/gnome/help/`; do
  %find_lang $d --with-gnome
  cat $d.lang >> %oname-%api.lang
done

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
%update_scrollkeeper

%postun
%clean_scrollkeeper

%files -f %{oname}-%api.lang
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_datadir}/gnome/gnome-version.xml
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf

%files -n %{libname}
%defattr (-, root, root)
%{_libdir}/libgnome-desktop-%{api_version}.so.%{lib_major}*
%{_libdir}/girepository-1.0/GnomeDesktop-3.0.typelib

%files -n %{libnamedev}
%defattr (-, root, root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/GnomeDesktop-3.0.gir
%doc %_datadir/gtk-doc/html/*
