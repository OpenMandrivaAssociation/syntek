#%%define svn	49
%define modname stk11xx

%define rel 1

Name: 		syntek
Version: 	2.1.0
Release: 	%mkrel %{?svn:0.%svn.}%rel
Summary: 	Syntek USB Video Camera driver for DC-1125 and STK-1135
Group: 		System/Configuration/Hardware
License: 	GPL
URL:		http://syntekdriver.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/syntekdriver/%{modname}%{?!svn:-%version}.tar.gz
Patch0:		stk11xx-2.1.0-compat.patch
BuildRoot: 	%_tmppath/%name-%version-%release-buildroot
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
%patch0 -p1 -b .compat
#sed -i 's:../doxygen:%buildroot:' doxygen.cfg
#sed -i 's:CREATE_SUBDIRS         = NO:CREATE_SUBDIRS         = YES:' doxygen.cfg

%build
%make -f Makefile.standalone doc

%install
rm -rf %buildroot

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
%defattr(-,root,root)
%dir %_docdir/%name-%version/
%doc %_docdir/%name-%version/README
%dir %_docdir/%name-%version/html/
%doc %_docdir/%name-%version/html/*

%files -n dkms-%name
%defattr(-,root,root)
%doc README
%_usrsrc/%name-%version-%release/


%clean
rm -rf %buildroot
