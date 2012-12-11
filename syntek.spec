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


%changelog
* Sun Nov 13 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.1.0-5
+ Revision: 730461
- drop dead v4l v1 code breaking module build (P6)
- fix build breakage due to removal of init_MUTEX() (P5)

* Mon May 16 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.1.0-4
+ Revision: 675093
- add good default values & hflip/vflip (#62818)
- drop buildroot as well..

* Mon May 16 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.1.0-3
+ Revision: 675089
- clean out old junk a bit..
- fix suspend/unsuspend (#62817)
- fix race condition in open(), making computer freeze (#62816)
- fix S_FMT and TRY_SMT ioctl - fixing library segfaults (#62815)

* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-2mdv2011.0
+ Revision: 615061
- the mass rebuild of 2010.1 packages

* Wed Nov 11 2009 Alexandre Possebom <alexandre@mandriva.com.br> 2.1.0-1mdv2010.1
+ Revision: 464880
- Update to 2.1.0
- Dropped old patches.

* Sun Sep 20 2009 Thierry Vignaud <tv@mandriva.org> 1.3.1-6mdv2010.0
+ Revision: 445343
- rebuild

* Thu Nov 20 2008 Pascal Terjan <pterjan@mandriva.org> 1.3.1-5mdv2009.1
+ Revision: 305306
- Fix use by HAL
- Include release in DKMS version

* Fri Nov 14 2008 Pascal Terjan <pterjan@mandriva.org> 1.3.1-4mdv2009.1
+ Revision: 302940
- Fix build on x86_64

* Wed Nov 12 2008 Pascal Terjan <pterjan@mandriva.org> 1.3.1-3mdv2009.1
+ Revision: 302490
- Add upstream patch to support 2.6.27

* Mon Mar 31 2008 Olivier Blin <blino@mandriva.org> 1.3.1-2mdv2008.1
+ Revision: 191291
- bump release
- remove hardcoded make command line (broken)

* Tue Feb 26 2008 Olivier Blin <blino@mandriva.org> 1.3.1-1mdv2008.1
+ Revision: 175530
- 1.3.1
- bump release
- fix driver name (use "stk11xx" instead of "usb_stk11xx_driver", #35019)

  + Thierry Vignaud <tv@mandriva.org>
    - fix description-line-too-long

* Fri Jan 18 2008 Pascal Terjan <pterjan@mandriva.org> 1.2.3-1mdv2008.1
+ Revision: 154611
- update to 1.2.3 (support more cameras, kopete, YUV)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Oct 30 2007 Pascal Terjan <pterjan@mandriva.org> 1.1.0-1mdv2008.1
+ Revision: 103897
- 1.1.0 (even if the source thinks it is v1.0.0)
- Fix use of conditionnals
- Move the ctags requirement to the right place

* Mon Oct 29 2007 Pascal Terjan <pterjan@mandriva.org> 1.0.0-0.svn49.3mdv2008.1
+ Revision: 103414
- ctags is required to build the module, not the package (#35006)

* Tue Oct 02 2007 Olivier Blin <blino@mandriva.org> 1.0.0-0.svn49.2mdv2008.0
+ Revision: 94486
- update to new version

* Wed Jul 25 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0.0-0.svn49.1mdv2008.0
+ Revision: 55569
- Import syntek




* Sat Jul 13 2007 Zé <mmodem00@gmail.com> 1.0.0-2
- sync svn (svn release 49)

* Tue May 22 2007 Zé <mmodem00@gmail.com> 1.0.0-1
- first package version 1.0.0
