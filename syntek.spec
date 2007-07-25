%define svn	49
%define modname syntek

%if %svn
%define rel 0.svn%svn.1
%else
%define rel 1
%endif

Name: 		syntek
Version: 	1.0.0
Release: 	%mkrel %rel
Summary: 	Syntek USB Video Camera driver for DC-1125 and STK-1135
Group: 		System/Configuration/Hardware
License: 	GPL
URL:		http://syntekdriver.sourceforge.net/
%if %svn
Source:		%name.tar.bz2
%else
Source:		http://prdownloads.sourceforge.net/syntekdriver/%name-%version.tar.bz2
%endif
BuildRoot: 	%_tmppath/%name-%version-%release-buildroot
BuildRequires:	ctags
BuildRequires:	doxygen
BuildRequires:	kernel-source >= 2.6.18

%description
Documentation for the syntek USB 2.0 video camera driver for DC-1125 and STK-1135


%package -n dkms-%name
Summary:	DKMS-ready kernel-source for the Syntek USB Video Camera kernel module
Group:		System/Configuration/Hardware
Requires(post):	dkms
Requires(preun):dkms

%description -n dkms-%name
DKMS-ready syntek USB 2.0 video camera driver for DC-1125 and STK-1135


%prep
%if %svn
%setup -qn %name
%else
%setup -q
%endif
#sed -i 's:../doxygen:%buildroot:' doxygen.cfg
#sed -i 's:CREATE_SUBDIRS         = NO:CREATE_SUBDIRS         = YES:' doxygen.cfg

%build
%make doc

%install
rm -rf %buildroot

mkdir -p -m755 %buildroot%_docdir/%name-%version/html
install -m644 %_builddir/doxygen/html/* %buildroot%_docdir/%name-%version/html
install -m644 README %buildroot%_docdir/%name-%version

# DKMS stuff
mkdir -p -m755 %buildroot%_usrsrc/%name-%version
cp -a * %buildroot%_usrsrc/%name-%version
# Configuration for dkms
cat > %buildroot%_usrsrc/%name-%version/dkms.conf << 'EOF'
PACKAGE_VERSION=%version
# Items below here should not have to change with each driver version
PACKAGE_NAME=%name
MAKE[0]="make driver KERNELPATH=${kernel_source_dir}"
BUILT_MODULE_NAME[0]="stk11xx"
DEST_MODULE_LOCATION[0]="/kernel/3rdparty/%name"
REMAKE_INITRD="no"
AUTOINSTALL=yes
EOF


%post -n dkms-%name
dkms add -m %name -v %version --rpm_safe_upgrade || :
dkms build -m %name -v %version --rpm_safe_upgrade || :
dkms install -m %name -v %version --rpm_safe_upgrade || :

%preun -n dkms-%name
dkms remove -m %name -v %version --all --rpm_safe_upgrade || :


%files
%defattr(-,root,root)
%dir %_docdir/%name-%version/
%doc %_docdir/%name-%version/README
%dir %_docdir/%name-%version/html/
%doc %_docdir/%name-%version/html/*

%files -n dkms-%name
%defattr(-,root,root)
%doc README
%dir %_usrsrc/%name-%version/
%_usrsrc/%name-%version/*


%clean
rm -rf %buildroot
