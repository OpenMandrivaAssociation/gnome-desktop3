%define	api_version 2
%define lib_major   17
%define libname	%mklibname %{name}-%{api_version}_ %{lib_major}
%define libnamedev %mklibname -d %{name}-%{api_version}

%define req_startup_notification_version 0.5

Summary:          Package containing code shared among gnome-panel, gnome-session, nautilus, etc
Name:             gnome-desktop
Version: 2.31.2
Release: %mkrel 2
License:          GPLv2+ and LGPLv2+
Group:            Graphical desktop/GNOME
Source0:          http://ftp.gnome.org/pub/GNOME/sources/gnome-desktop/%{name}-%{version}.tar.bz2
BuildRoot:        %{_tmppath}/%{name}-%{version}-root
URL:              http://www.gnome.org
BuildRequires:	  startup-notification-devel >= %{req_startup_notification_version}
BuildRequires: gtk+2-devel >= 2.14.0
BuildRequires: glib2-devel >= 2.19.1
BuildRequires: libGConf2-devel
BuildRequires: gtk-doc
BuildRequires:	  scrollkeeper
BuildRequires:	gnome-doc-utils >= 0.3.2
BuildRequires:	libxslt-proc
BuildRequires:    intltool >= 0.40.0
BuildRequires: ldetect-lst

%description
This package contains some data files and other shared components of the
GNOME user environment.

%package -n %{libname}
Summary:	%{summary}
Group:		System/Libraries
Requires:   %{name}-common >= %{version}-%{release}
Provides:	%{name}-%{api_version} = %{version}-%{release}
Requires: libstartup-notification-1 >= %{req_startup_notification_version}

%description -n %{libname}
This package contains an internal library
(libgnomedesktop) used to implement some portions of the GNOME
desktop.

%package -n %{libnamedev}
Summary:	Static libraries, include files for gnome-desktop
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-%{api_version}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:   libstartup-notification-1-devel >= %{req_startup_notification_version}
Obsoletes: %mklibname -d %{name}-2_ 2

%description -n %{libnamedev}
Static libraries, include files for internal library libgnomedesktop.

%package common
Summary: Data files needed by libgnomedesktop library
Group:	%{group}
Conflicts: %{name} < 2.20.0-1mdv
Requires: ldetect-lst >= 0.1.282

%description common
Data files needed by libgnomedesktop library.

%prep
%setup -q

%build

%configure2_5x --with-gnome-distributor="%vendor" --disable-scrollkeeper --with-pnp-ids-path=%{_datadir}/misc/pnp.ids

%make LIBS=-lm


%install
rm -rf $RPM_BUILD_ROOT %{name}-2.0.lang

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std 
%find_lang %{name}-2.0
for omf in %buildroot%_datadir/omf/*/{*-??.omf,*-??_??.omf,*-???.omf};do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name-2.0.lang
done
for d in `ls -1 %buildroot%_datadir/gnome/help/`; do
  %find_lang $d --with-gnome
  cat $d.lang >> %name-2.0.lang
done

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
%update_scrollkeeper

%postun
%clean_scrollkeeper

%if %mdkversion < 200900
%post -p /sbin/ldconfig -n %{libname}
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig -n %{libname}
%endif

%files 
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/*
%{_mandir}/man1/*
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%{_datadir}/gnome-about
%{_datadir}/applications/*
%{_datadir}/pixmaps/*

%files -n %{libname}
%defattr (-, root, root)
%{_libdir}/libgnome-desktop-%{api_version}.so.%{lib_major}*

%files -n %{libnamedev}
%defattr (-, root, root)
%{_includedir}/*
%{_libdir}/*.a
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%doc %_datadir/gtk-doc/html/*

%files common -f %{name}-2.0.lang
%defattr (-, root, root)
