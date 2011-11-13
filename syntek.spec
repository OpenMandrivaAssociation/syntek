%define modname stk11xx

Name: 		syntek
Version: 	2.1.0
Release: 	5
Summary: 	Syntek USB Video Camera driver for DC-1125 and STK-1135
Group: 		System/Configuration/Hardware
License: 	GPL
URL:		http://syntekdriver.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/syntekdriver/%{modname}%{?!svn:-%version}.tar.gz
Patch0:		stk11xx-2.1.0-compat.patch
# mdvbz#62815
Patch1:		stk11xx-v4l.c.patch
# mdvbz#62816
Patch2:		stk11xx-2.1.0-fix-race-conditions.patch
# mdvbz#62817
Patch3:		stk11xx-2.1.0-fix-suspend.patch
# mdvbz#62818
Patch4:		stk11xx-2.1.0-default-values-and-add-hflip-vlip.patch
Patch5:		stk11xx-usb.patch
Patch6:		stk11xx-2.1.0-drop-v4l1-support.patch
BuildRequires:	doxygen

%description
Documentation for the syntek USB 2.0 video camera driver for DC-1125 and
STK-1135


%package -n dkms-%name
Summary:	DKMS-ready kernel-source for the Syntek USB Video Camera kernel module
Group:		System/Configuration/Hardware
Requires(post):	ctags
Requires(post):	dkms
Requires(preun):dkms

%description -n dkms-%name
DKMS-ready syntek USB 2.0 video camera driver for DC-1125 and STK-1135


%prep
%setup -qn %{modname}%{?!svn:-%version}
%patch0 -p1 -b .compat~
%patch1 -p0 -b .62815~
%patch2 -p0 -b .62816~
%patch3 -p0 -b .62817~
%patch4 -p1 -b .62818~
%patch5 -p1 -b .usb~
%patch6 -p1 -b .v4l2~
#sed -i 's:../doxygen:%buildroot:' doxygen.cfg
#sed -i 's:CREATE_SUBDIRS         = NO:CREATE_SUBDIRS         = YES:' doxygen.cfg

%build
%make -f Makefile.standalone doc

mkdir -p -m755 %buildroot%_docdir/%name-%version/html
install -m644 %_builddir/doxygen/html/* %buildroot%_docdir/%name-%version/html
install -m644 README %buildroot%_docdir/%name-%version

# DKMS stuff
mkdir -p -m755 %buildroot%_usrsrc/%name-%version-%release
cp -a * %buildroot%_usrsrc/%name-%version-%release
# Configuration for dkms
cat > %buildroot%_usrsrc/%name-%version-%release/dkms.conf << 'EOF'
PACKAGE_VERSION=%version-%release
# Items below here should not have to change with each driver version
PACKAGE_NAME=%name
BUILT_MODULE_NAME[0]="%modname"
DEST_MODULE_LOCATION[0]="/kernel/3rdparty/%name"
REMAKE_INITRD="no"
AUTOINSTALL=yes
EOF


%post -n dkms-%name
dkms add -m %name -v %version-%release --rpm_safe_upgrade || :
dkms build -m %name -v %version-%release --rpm_safe_upgrade || :
dkms install -m %name -v %version-%release --rpm_safe_upgrade || :

%preun -n dkms-%name
dkms remove -m %name -v %version-%release --all --rpm_safe_upgrade || :


%files
%dir %_docdir/%name-%version/
%doc %_docdir/%name-%version/README
%dir %_docdir/%name-%version/html/
%doc %_docdir/%name-%version/html/*

%files -n dkms-%name
%doc README
%_usrsrc/%name-%version-%release/
