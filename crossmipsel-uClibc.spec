#
%bcond_with	bootstrap	# Build only headers
#
# TODO:
#	- compile for m5307
#	- add support for flat shared libraries (-mid-shared-library)
#	- make less ugly ?

%define		llh_version	2.4.31

Summary:	C library optimized for size (mipsel version)
Summary(pl):	Biblioteka C zoptymalizowana na rozmiar (dla mipsel)
Name:		crossmipsel-uClibc
Version:	0.9.28
Release:	1
Epoch:		0
License:	LGPL
Group:		Libraries
Source0:	http://www.uclibc.org/downloads/uClibc-%{version}.tar.bz2
# Source0-md5:	1ada58d919a82561061e4741fb6abd29
Source1:	http://www.uclibc.org/downloads/toolchain/linux-libc-headers-%{llh_version}.tar.bz2
# Source1-md5:	997d36627baf6825c712431dee4d79d3
Source2:	crossmipsel-uClibc.config
URL:		http://www.uclibc.org/
%{?!with_bootstrap:BuildRequires:	crossmipsel-gcc}
BuildRequires:	sed >= 4.0
BuildRequires:	which
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		mipsel-pld-linux
%define		arch		%{_prefix}/%{target}

%define         _noautostrip    .*%{arch}/lib/.*\\.[ao]$

%description
Small libc for building embedded applications.
Version compiled for mipsel.

%description -l pl
Ma³a libc do budowania aplikacji wbudowanych.
Wersja dla mipsel.

%prep
%setup -q -n uClibc-%{version} -a1

install %{SOURCE2} .config

sed -i "s@^.*KERNEL_SOURCE.*\$@KERNEL_SOURCE=\"$PWD/linux-libc-headers-%{llh_version}\"@"	\
	.config

cd linux-libc-headers-%{llh_version}/include/asm-mips
grep '#include[[:space:]]\+<asm-mipsel/.\+\.h>' * | cut -f1 -d: | while read file; do
    cat "../asm-mipsel/$file" > "$file"
done

%build
%if %{with bootstrap}
    %{__make} headers < /dev/null
%else
    _build () {
	local MULTILIB_SUBDIR=$1
	local PIC_CODE=$2
	local COMPILE_FLAGS=$3
	
	cat .config	| grep -v "HAVE_SHARED"		> .config.tmp
	cat .config.tmp | grep -v "BUILD_UCLIBC_LDSO"	> .config
	
	if [ $PIC_CODE -ne 0 ]; then
    	    sed -i 's/^.*DOPIC.*$/DOPIC=y/'		.config
	    echo "HAVE_SHARED=n"		>>	.config
	else
    	    sed -i 's/^.*DOPIC.*$/# DOPIC is not set/'	.config
	fi

        %{__make} clean						|| exit 1
        %{__make} all	ARCH_CFLAGS="$COMPILE_FLAGS" </dev/null	|| exit 1
	
	install -d		$RPM_BUILD_ROOT%{arch}/lib/$MULTILIB_SUBDIR
	install lib/*.[ao]	$RPM_BUILD_ROOT%{arch}/lib/$MULTILIB_SUBDIR
	%{target}-strip --strip-debug -R.comment -R.note	\
				$RPM_BUILD_ROOT%{arch}/lib/$MULTILIB_SUBDIR/*.[ao]
    }

    rm -rf $RPM_BUILD_ROOT
    
		_build	"mipsel"	0 "-Wall -march=mips32 -mtune=mips32  -nostdinc -mno-split-addresses"
		_build	"mipsel"	1 "-Wall -march=mips32 -mtune=mips32  -nostdinc -mno-split-addresses"

%endif

%install
install -d		$RPM_BUILD_ROOT%{arch}/include
cp -RL include/*	$RPM_BUILD_ROOT%{arch}/include
ln -s include		$RPM_BUILD_ROOT%{arch}/sys-include

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changelog* DEDICATION.mjn3 MAINTAINERS README TODO docs/threads.txt
%{arch}/include
%{arch}/lib
%{arch}/sys-include
