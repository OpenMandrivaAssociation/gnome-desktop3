%define url_ver %(echo %{version}|cut -d. -f1,2)

%define oname	gnome-desktop
%define	appver	3
%define api	3.0
%define major	7
%define libname	%mklibname %{oname} %{appver} %{major}
%define girname	%mklibname %{oname}-gir %{api}
%define devname	%mklibname -d %{oname} %{appver}

Summary:	Package containing code shared among gnome-panel, gnome-session, nautilus, etc
Name:		%{oname}%{appver}
Version:	3.8.4
Release:	5
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{oname}/%{url_ver}/%{oname}-%{version}.tar.xz

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	ldetect-lst
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(xkeyboard-config)
BuildRequires:	iso-codes
Requires:	ldetect-lst >= 0.1.282
Conflicts:	gnome-desktop-common < 2.32.1-2
Conflicts:	%{_lib}gnome-desktop3_4 < 3.6.2-2
%rename 	%{oname}

%description
This package contains some data files and other shared components of the
GNOME user environment.

%package -n %{libname}
Summary:	%{summary}
Group:		System/Libraries

%description -n %{libname}
This package contains an internal library
(libgnomedesktop) used to implement some portions of the GNOME
desktop.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{oname}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{oname}.

%package -n %{devname}
Summary:	Development libraries, include files for %{oname}
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}

%description -n %{devname}
Development libraries, include files for internal library %{oname}.

%prep
%setup -qn %{oname}-%{version}

%build
%configure2_5x \
	--disable-static \
	--with-gnome-distributor="%{_vendor}" \
	--disable-scrollkeeper \
	--with-pnp-ids-path=%{_datadir}/misc/pnp.ids

%make LIBS='-lrt -lgmodule-2.0'

%install
%makeinstall_std 
%find_lang %{oname}-%{api} --with-gnome --all-name

%files -f %{oname}-%{api}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_datadir}/gnome/gnome-version.xml
%{_libexecdir}/gnome-rr-debug

%files -n %{libname}
%{_libdir}/libgnome-desktop-%{appver}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/GnomeDesktop-%{api}.typelib

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/GnomeDesktop-%{api}.gir

