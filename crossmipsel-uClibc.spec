
%define		llh_version	2.4.31

Summary:	C library optimized for size (mipsel version)
Summary(pl.UTF-8):	Biblioteka C zoptymalizowana na rozmiar (dla mipsel)
Name:		crossmipsel-uClibc
Version:	0.9.28
Release:	2
Epoch:		0
License:	LGPL
Group:		Libraries
Source0:	http://www.uclibc.org/downloads/uClibc-%{version}.tar.bz2
# Source0-md5:	1ada58d919a82561061e4741fb6abd29
Source1:	http://www.uclibc.org/downloads/toolchain/linux-libc-headers-%{llh_version}.tar.bz2
# Source1-md5:	997d36627baf6825c712431dee4d79d3
Source2:	%{name}.config
URL:		http://www.uclibc.org/
BuildRequires:	crossmipsel-gcc
BuildRequires:	sed >= 4.0
BuildRequires:	which
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		mipsel-pld-linux
%define		arch		%{_prefix}/%{target}

%define		no_install_post_strip			1
%define		no_install_post_chrpath			1

%description
Small libc for building embedded applications. Version compiled for
mipsel.

%description -l pl.UTF-8
Mała libc do budowania aplikacji wbudowanych. Wersja dla mipsel.

%prep
%setup -q -n uClibc-%{version} -a1
install %{SOURCE2} .config
sed -i "s@^.*KERNEL_SOURCE.*\$@KERNEL_SOURCE=\"$PWD/linux-libc-headers-%{llh_version}\"@"	\
	.config

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changelog* DEDICATION.mjn3 MAINTAINERS README TODO docs/threads.txt
%dir %{arch}/lib
%attr(755,root,root) %{arch}/lib/*.so
%attr(755,root,root) %{arch}/lib/*.so.*
%{arch}/lib/*.[ao]
%{arch}/include
