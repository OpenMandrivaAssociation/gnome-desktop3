%define oname gnome-desktop

%define	api_version	3
%define api			3.0
%define lib_major	2

%define libname		%mklibname %{oname} %{api_version} %{lib_major}
%define develname	%mklibname -d %{oname} %{api_version}
%define gi_libname	%mklibname %{oname}-gir %{api}

Summary:	Package containing code shared among gnome-panel, gnome-session, nautilus, etc
Name:		%{oname}3
Version:	3.2.1
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org
Source0:	http://download.gnome.org/sources/%{oname}/3.2/%{oname}-%{version}.tar.xz

BuildRequires:	gnome-doc-utils >= 0.3.2
BuildRequires:	gtk-doc
BuildRequires:	intltool >= 0.40.0
BuildRequires:	ldetect-lst
BuildRequires:	scrollkeeper
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.21.3
BuildRequires:  pkgconfig(gio-2.0) >= 2.19.1
BuildRequires:  pkgconfig(glib-2.0) >= 2.19.1
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gsettings-desktop-schemas) >= 0.1.4
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.0
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext) >= 1.2
BuildRequires:  pkgconfig(xrandr) >= 1.2

Requires:	ldetect-lst >= 0.1.282
Obsoletes:	%{name}-common < 2.91.92
Conflicts:	gnome-desktop-common < 2.32.1-2

%description
This package contains some data files and other shared components of the
GNOME user environment.

%package -n %{libname}
Summary:	%{summary}
Group:		System/Libraries
%rename		%{_lib}%{oname}-3_2

%description -n %{libname}
This package contains an internal library
(libgnomedesktop) used to implement some portions of the GNOME
desktop.

%package -n %{gi_libname}
Summary:	GObject Introspection interface description for %{oname}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{gi_libname}
GObject Introspection interface description for %{oname}.

%package -n %{develname}
Summary:	Static libraries, include files for %{oname}
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
Static libraries, include files for internal library libgnomedesktop.

%prep
%setup -qn %{oname}-%{version}

%build
%configure2_5x \
	--disable-static \
	--with-gnome-distributor="%_vendor" \
	--disable-scrollkeeper \
	--with-pnp-ids-path=%{_datadir}/misc/pnp.ids

%make

%install
rm -rf %{buildroot} *.lang

%makeinstall_std 
rm -f %{buildroot}%{_libdir}/*.la

%find_lang %{oname}-%api
for omf in %{buildroot}%{_datadir}/omf/*/{*-??.omf,*-??_??.omf,*-???.omf};do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%{buildroot}!!)" >> %{oname}-%api.lang
done

for d in `ls -1 %{buildroot}%{_datadir}/gnome/help/`; do
  %find_lang $d --with-gnome
  cat $d.lang >> %{oname}-%api.lang
done


%files -f %{oname}-%api.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_datadir}/gnome/gnome-version.xml
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf

%files -n %{libname}
%{_libdir}/libgnome-desktop-%{api_version}.so.%{lib_major}*

%files -n %{gi_libname}
%{_libdir}/girepository-1.0/GnomeDesktop-%{api}.typelib

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/GnomeDesktop-%{api}.gir
%doc %{_datadir}/gtk-doc/html/*

