Version: 2.05b
Name: bash
Summary: The GNU Bourne Again shell (bash) version %{version}.
Release: 39
Group: System Environment/Shells
License: GPL
Source0: ftp://ftp.gnu.org/gnu/bash/bash-%{version}.tar.bz2
Source2: ftp://ftp.gnu.org/gnu/bash/bash-doc-%{version}.tar.bz2
Source3: dot-bashrc
Source4: dot-bash_profile
Source5: dot-bash_logout
Source6: http://www.caliban.org/files/bash/bash-completion-20020220.tar.gz
Patch0: bash-2.03-paths.patch
Patch1: bash-2.02-security.patch
Patch3: bash-2.03-profile.patch
Patch5: bash-2.05a-requires.patch
Patch6: bash-2.04-compat.patch
Patch7: bash-2.05a-shellfunc.patch
Patch8: bash-2.05-ia64.patch
Patch11: bash-2.05a-loadables.patch
Patch12: bash-2.05a-interpreter.patch
Patch15: bash-2.05b-readline-oom.patch
Patch16: bash-2.05b-utf8.patch
Patch17: bash-2.05b-mbinc.patch
Patch18: ftp://ftp.gnu.org/pub/gnu/bash/bash-2.05b-patches/bash205b-001
Patch19: ftp://ftp.gnu.org/pub/gnu/bash/bash-2.05b-patches/bash205b-002
Patch20: ftp://ftp.gnu.org/pub/gnu/bash/bash-2.05b-patches/bash205b-003
Patch21: ftp://ftp.gnu.org/pub/gnu/bash/bash-2.05b-patches/bash205b-004
Patch22: bash-2.05b-locale.patch
Patch23: bash-2.05b-readline-init.patch
Patch24: bash-2.05b-restrict.patch
Patch26: bash-2.05b-xcc.patch
Patch27: bash-2.05b-pgrp_sync.patch
Patch28: bash-2.05b-003fix.patch
Patch29: bash-2.05b-display.patch
Patch30: bash-2.05b-manso.patch
Patch31: bash-2.05b-debuginfo.patch
Patch32: bash-2.05b-warnings.patch
Patch33: bash-2.05b-complete.patch
Patch34: ftp://ftp.gnu.org/pub/gnu/bash/bash-2.05b-patches/bash205b-005
Patch35: ftp://ftp.gnu.org/pub/gnu/bash/bash-2.05b-patches/bash205b-006
Patch36: ftp://ftp.gnu.org/pub/gnu/bash/bash-2.05b-patches/bash205b-007
Patch37: bash-2.05b-slow.patch
Patch38: bash-2.05b-subst.patch
Patch39: bash-2.05b-rereadline.patch
Patch40: bash-2.05b-overread.patch
Prefix: %{_prefix}
Requires: mktemp
Provides: bash2
Obsoletes: bash2 etcskel
Obsoletes: bash2-doc bash-doc
BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires: texinfo
BuildRequires: libtermcap-devel

%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh). Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh). Most sh scripts can be run by bash without modification. This
package (bash) contains bash version %{version}, which improves POSIX
compliance over previous versions. However, many old shell scripts
will depend upon the behavior of bash 1.14, which is included in the
bash1 package. Bash is the default shell for Red Hat Linux.  It is
popular and powerful, and you'll probably end up using it.

%prep
%setup -q -a 2 -a 6
%patch0 -p1 -b .paths
%patch1 -p1 -b .security
%patch3 -p1 -b .profile
%patch5 -p1 -b .requires
%patch6 -p1 -b .compat
%patch7 -p1 -b .shellfunc
%patch8 -p1 -b .ia64
%patch11 -p1 -b .loadables
%patch12 -p1 -b .interpreter
%patch15 -p1 -b .readline-oom
%patch16 -p1 -b .utf8
%patch17 -p1 -b .mbinc
%patch18 -p0 -b .001
%patch19 -p0 -b .002
%patch20 -p0 -b .003
%patch21 -p0 -b .004
%patch22 -p1 -b .locale
%patch23 -p1 -b .readline-init
%patch24 -p1 -b .restrict
%patch26 -p1 -b .xcc
%patch27 -p1 -b .pgrp_sync
%patch28 -p1 -b .003fix
%patch29 -p1 -b .display
%patch30 -p1 -b .manso
%patch31 -p1 -b .debuginfo
%patch32 -p1 -b .warnings
%patch33 -p1 -b .complete
%patch34 -p0 -b .005
%patch35 -p0 -b .006
%patch36 -p0 -b .007
%patch37 -p1 -b .slow
%patch38 -p1 -b .subst
%patch39 -p1 -b .rereadline
%patch40 -p1 -b .overread
echo %{version} > _distribution
echo %{release} > _patchlevel

%build
if ! autoconf; then
	# Yuck. We're using autoconf 2.1x.
	ln -s /bin/true autoconf
	export PATH=.:$PATH
fi
%configure --with-bash-malloc=no
make CPPFLAGS=`getconf LFS_CFLAGS`
make check

%install
rm -rf $RPM_BUILD_ROOT

if [ -e autoconf ]; then
	# Yuck. We're using autoconf 2.1x.
	export PATH=.:$PATH
fi

# Fix bug #83776
perl -pi -e 's,bashref\.info,bash.info,' doc/bashref.info

%makeinstall

mkdir -p $RPM_BUILD_ROOT/etc

# make manpages for bash builtins as per suggestion in DOC/README
cd doc
sed -e '
/^\.SH NAME/, /\\- bash built-in commands, see \\fBbash\\fR(1)$/{
/^\.SH NAME/d
s/^bash, //
s/\\- bash built-in commands, see \\fBbash\\fR(1)$//
s/,//g
b
}
d
' builtins.1 > man.pages
for i in echo pwd test kill; do
  perl -pi -e "s,$i,,g" man.pages
  perl -pi -e "s,  , ,g" man.pages
done

install -c -m 644 builtins.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/builtins.1

for i in `cat man.pages` ; do
  echo .so man1/builtins.1 > ${RPM_BUILD_ROOT}%{_mandir}/man1/$i.1
  chmod 0644 ${RPM_BUILD_ROOT}%{_mandir}/man1/$i.1
done

# Link bash man page to sh so that man sh works.
ln -s bash.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/sh.1

# Not for printf (conflict with coreutils)
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/printf.1

pushd $RPM_BUILD_ROOT
mkdir ./bin
mv ./usr/bin/bash ./bin
ln -sf bash ./bin/bash2
ln -sf bash ./bin/sh
gzip -9nf .%{_infodir}/bash.info
rm -f .%{_infodir}/dir
popd
mkdir -p $RPM_BUILD_ROOT/etc/skel
install -c -m644 $RPM_SOURCE_DIR/dot-bashrc $RPM_BUILD_ROOT/etc/skel/.bashrc
install -c -m644 $RPM_SOURCE_DIR/dot-bash_profile \
	$RPM_BUILD_ROOT/etc/skel/.bash_profile
install -c -m644 $RPM_SOURCE_DIR/dot-bash_logout \
	$RPM_BUILD_ROOT/etc/skel/.bash_logout

%clean
rm -rf $RPM_BUILD_ROOT

# ***** bash doesn't use install-info. It's always listed in %{_infodir}/dir
# to prevent prereq loops

%post

HASBASH2=""
HASBASH=""
HASSH=""

if [ ! -f /etc/shells ]; then
	> /etc/shells
fi

(while read line ; do
	if [ $line = /bin/bash ]; then
		HASBASH=1
	elif [ $line = /bin/sh ]; then
		HASSH=1
	elif [ $line = /bin/bash2 ]; then
		HASBASH2=1
	fi
 done

 if [ -z "$HASBASH2" ]; then
	echo "/bin/bash2" >> /etc/shells
 fi
 if [ -z "$HASBASH" ]; then
	echo "/bin/bash" >> /etc/shells
 fi
 if [ -z "$HASSH" ]; then
	echo "/bin/sh" >> /etc/shells
fi) < /etc/shells

%postun
if [ "$1" = 0 ]; then
    grep -v '^/bin/bash2$' < /etc/shells | \
	grep -v '^/bin/bash$' | \
	grep -v '^/bin/sh$' > /etc/shells.new
    mv /etc/shells.new /etc/shells
fi

%files
%defattr(-,root,root)
%doc CHANGES COMPAT NEWS NOTES POSIX
%doc doc/FAQ doc/INTRO doc/article.ms
%doc -P examples/bashdb/ examples/functions/ examples/misc/
%doc -P examples/scripts.noah/ examples/scripts.v2/ examples/scripts/
%doc -P examples/startup-files/ examples/complete/ examples/loadables/
%config(noreplace) /etc/skel/.b*
/bin/sh
/bin/bash
/bin/bash2
%{_prefix}/bin/bashbug
%{_infodir}/bash.info*
%{_mandir}/*/*
%{_mandir}/*/..1*
%doc doc/*.ps doc/*.0 doc/*.html doc/article.txt

%changelog
* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 2.05b-39
- Build requires libtermcap-devel (bug #125068).

* Wed May 19 2004 Tim Waugh <twaugh@redhat.com>
- Don't ship empty %%{_libdir}/bash (bug #123556).

* Thu Mar 11 2004 Tim Waugh <twaugh@redhat.com> 2.05b-38
- Apply patch from Nalin Dahyabhai fixing an overread.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 22 2004 Tim Waugh <twaugh@redhat.com> 2.05b-36
- Fix the bug causing bindings to need reparsing .inputrc (bug #114101).

* Mon Jan  5 2004 Tim Waugh <twaugh@redhat.com> 2.05b-35
- Fix parameter expansion in multibyte locales (bug #112657).
- Run 'make check'.

* Tue Dec  9 2003 Tim Waugh <twaugh@redhat.com> 2.05b-34
- Build requires texinfo (bug #111171).

* Fri Nov 28 2003 Tim Waugh <twaugh@redhat.com> 2.05b-33
- Speed up UTF-8 command-line redrawing in the common case (bug #102353,
  bug #110777).

* Thu Nov  6 2003 Tim Waugh <twaugh@redhat.com> 2.05b-32
- Apply upstream patches (bug #109269 among others).

* Fri Oct 31 2003 Tim Waugh <twaugh@redhat.com>
- Fix bash.info (bug #83776).

* Tue Oct 28 2003 Tim Waugh <twaugh@redhat.com> 2.05b-31
- Add bash205b-007 patch to fix bug #106876.

* Thu Oct 23 2003 Tim Waugh <twaugh@redhat.com> 2.05b-30
- Rebuilt.

* Thu Sep 18 2003 Tim Waugh <twaugh@redhat.com> 2.05b-29.1
- Rebuilt.

* Thu Sep 18 2003 Tim Waugh <twaugh@redhat.com> 2.05b-29
- Avoid crashing on multibyte input when locale is set incorrectly
  (bug #74266).

* Fri Sep  5 2003 Tim Waugh <twaugh@redhat.com> 2.05b-28.1
- Rebuilt.

* Fri Sep  5 2003 Tim Waugh <twaugh@redhat.com> 2.05b-28
- Avoid built-in malloc implementation (bug #103768).

* Wed Sep  3 2003 Tim Waugh <twaugh@redhat.com> 2.05b-27.1
- Rebuilt.

* Wed Sep  3 2003 Tim Waugh <twaugh@redhat.com> 2.05b-27
- LFS support (bug #103627).

* Thu Jul 31 2003 Tim Waugh <twaugh@redhat.com> 2.05b-26.1
- Rebuilt.

* Thu Jul 31 2003 Tim Waugh <twaugh@redhat.com> 2.05b-26
- Merge bash-doc into main package (bug #100632).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 2.05b-25
- rebuilt

* Mon May 12 2003 Tim Waugh <twaugh@redhat.com> 2.05b-24
- Fix completion display when multibyte or control characters are to be
  shown (bug #90201).

* Tue Mar 26 2003 Tim Waugh <twaugh@redhat.com> 2.05b-23
- Fix a warning message (bug #79629).
- Don't remove generated source during build, for debuginfo package.
- Don't build with AFS support (bug #86514).

* Tue Mar 25 2003 Tim Waugh <twaugh@redhat.com> 2.05b-22
- Really fix bug #78455.

* Tue Mar 11 2003 Tim Waugh <twaugh@redhat.com> 2.05b-21
- Don't explicitly strip binaries (bug #85995).

* Tue Feb 11 2003 Tim Waugh <twaugh@redhat.com> 2.05b-20
- Really fix bug #83331 for good.

* Mon Feb 10 2003 Tim Waugh <twaugh@redhat.com> 2.05b-19
- Fix builtins.1.

* Fri Feb  7 2003 Tim Waugh <twaugh@redhat.com> 2.05b-18
- Actually apply the patch (bug #83331).

* Wed Feb  5 2003 Tim Waugh <twaugh@redhat.com> 2.05b-17
- Fix history/UTF-8 bug (bug #83331).

* Sun Jan 26 2003 Tim Waugh <twaugh@redhat.com> 2.05b-16
- More tab-completion fixing (bug #72512).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 2.05b-15
- rebuilt

* Wed Jan 15 2003 Tim Waugh <twaugh@redhat.com> 2.05b-14
- Force pgrp synchronization (bug #81653).

* Thu Dec 05 2002 Elliot Lee <sopwith@redhat.com> 2.05b-13
- (patch26) Don't call 'size' in makefile. Pointless, and interferes with 
  cross compiles.

* Tue Dec  3 2002 Tim Waugh <twaugh@redhat.com> 2.05b-12
- Prevent prompt overwriting output (bug #74383).

* Wed Nov 27 2002 Tim Waugh <twaugh@redhat.com> 2.05b-11
- Fix '-rbash' (bug #78455).

* Thu Nov 21 2002 Tim Waugh <twaugh@redhat.com> 2.05b-10
- Rebuild.

* Wed Nov 20 2002 Elliot Lee <sopwith@redhat.com>
- Use the configure macro instead of calling ./configure directly

* Wed Nov 13 2002 Tim Waugh <twaugh@redhat.com>
- Revert previous change.

* Wed Nov 13 2002 Tim Waugh <twaugh@redhat.com> 2.05b-8
- PreReq libtermcap.

* Fri Oct 18 2002 Tim Waugh <twaugh@redhat.com> 2.05b-7
- Add readline-init patch (bug #74925).

* Wed Oct 16 2002 Tim Waugh <twaugh@redhat.com> 2.05b-6
- Add the (4) patches from ftp.gnu.org (bug #75888, bug #72512).
- Ship '.' man page, which doesn't get picked up by glob.
- Don't install files not shipped when building.
- Locale shell variables fix (bug #74701).

* Fri Aug 23 2002 Tim Powers <timp@redhat.com> 2.05b-5
- re-bzip the docs, something was corrupted

* Thu Aug 22 2002 Tim Waugh <twaugh@redhat.com> 2.05b-4
- Fix history substitution modifiers in UTF-8 (bug #70294, bug #71186).
- Fix ADVANCE_CHAR at end of string (bug #70819).
- docs: CWRU/POSIX.NOTES no longer exists, but ship POSIX.

* Wed Aug 07 2002 Phil Knirsch <pknirsch@redhat.com> 2.05b-3
- Fixed out of memory problem with readline.

* Tue Jul 23 2002 Phil Knirsch <pknirsch@redhat.com> 2.05b-2
- Added symlink for sh.1 in man1 section so that man sh works (#44039).

* Mon Jul 22 2002 Phil Knirsch <pknirsch@redhat.com> 2.05b-1
- Update to 2.05b

* Wed Jul 10 2002 Phil Knirsch <pknirsch@redhat.com> 2.05a-16
- Fixed readline utf8 problem (#68313).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.05a-15
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com> 2.05a-14
- automated rebuild

* Fri Apr 12 2002 Tim Powers <timp@redhat.com> 2.05a-13
- don't build the stuff in examples/loadables. It breaks FHS
  compliance

* Fri Apr  5 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.05a-12
- Fix the fix for #62418

* Thu Apr  4 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.05a-11
- Fix kill builtin (#62418)

* Mon Mar 25 2002 Trond Eivind Glomsr�d <teg@redhat.com> 2.0.5a-10
- Get rid of completion subpackage
- Use %%{_tmppath}

* Mon Mar 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.05a-9
- Add patch from Ulrich Drepper to get better error messages when trying
  to launch an application with a bad ELF interpreter (e.g. libc5 ld.so)
  (#60870)

* Fri Feb 22 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.05a-8
- Update completion

* Wed Jan 30 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.05a-7
- Update completion stuff and move it to a separate package

* Sat Jan 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.05a-6
- Add patches from Ian Macdonald <ian@caliban.org>

* Wed Jan 23 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.05a-5
- Add programmable completion (optional)

* Thu Jan 17 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.05a-4
- Fix mailcheck (#57792)

* Tue Jan 15 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.05a-3
- Fix autoconf mess
- Build --with-afs, some users may be using it

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Nov 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.05a-2
- Fix conflict with sh-utils (printf builtin manpage vs. printf binary manpage)
  (#56590)

* Tue Nov 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.05a-1
- 2.05a

* Wed Oct 10 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- disable s390x fix, not needed anymore

* Mon Oct  1 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.05-9
- Add patch from readline 4.2-3 to bash's internal libreadline

* Mon Jul  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.05-8
- Merge Pekka Savola's patch (RFE#47762)

* Mon Jul  2 2001 Pekka Savola <pekkas@netcore.fi>
- Add IPv6 patch from PLD (only redirection to /dev/{tcp,udp}/host/port
  support)

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.05-7
- Add some bugfix patches from the maintainer

* Mon Jun 11 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- added patch for s390x from <oliver.paukstadt@millenux.com>

* Wed May 23 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.05-5
- Don't set BASH_ENV in .bash_profile, it causes .bashrc to be sourced
  twice in interactive non-login shells.
- s/Copyright/License/

* Fri May  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.05-4
- Fix tempfile creation in bashbug

* Wed May  2 2001 Preston Brown <pbrown@redhat.com> 2.05-3
- bashrc moved to setup package

* Tue Apr 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.05-2
- bash comes with its own copy of readline... Add the patches we're
  applying in the readline package.

* Tue Apr 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.05-1
- Update to 2.05
- Change PROMPT_COMMAND in bashrc for xterms
  to something less space consuming (#24159)
- Provide plugs for alternate prompt commands (#30634), but don't
  default to them

* Mon Mar 19 2001 Preston Brown <pbrown@redhat.com>
- add default aliases for 'dir' and 'df' to have human readable output

* Wed Feb 28 2001 Matt Wilson <msw@redhat.com>
- don't Prereq: /sbin/install-info!

* Tue Feb 27 2001 Preston Brown <pbrown@redhat.com>
- noreplace config files
- don't own /etc/skel directory

* Wed Feb 22 2001 Harald Hoyer <harald@redhat.de>
- changed /etc/bashrc to work with backspace = 0177 (rxvt)

* Wed Feb 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- changed /etc/skel/.bash_profile to "unset USERNAME"

* Mon Feb  5 2001 Yukihiro Nakai <ynakai@redhat.com>
- Delete Japanese resources from dot-bashrc
  and move them to each package.

* Fri Dec 15 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese resource to dot-bashrc

* Mon Dec 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild to get rid of 0777 doc dirs

* Thu Nov 16 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- restore the ^Hs in documentation, they're highlighting sequences
  for less (#20654) 

* Fri Sep 15 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- bash-2.04-export.patch is reported to fix compilation
  of older glibc-2.1 sources

* Tue Aug 22 2000 Matt Wilson <msw@redhat.com>
- fixed the summary of bash-doc to use %%{version} instead of "2.03"

* Tue Aug  8 2000 Bill Nottingham <notting@redhat.com>
- 'exit' in bashrc is very bad.

* Tue Aug  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- minor bashrc fix (Bug #8518)

* Mon Jul 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't use tput etc. in bashrc if /usr isn't available (Bug #14116)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 22 2000 Bill Nottingham <notting@redhat.com>
- fix for some IA-64 issues from Stephane Eranian

* Thu Jun 15 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix summary and description, they had old version numbers (Bug #12092)

* Tue Jun  6 2000 Bill Nottingham <notting@redhat.com>
- add /etc/skel/.bash* ; obsolete etcskel

* Tue May  2 2000 Bill Nottingham <notting@redhat.com>
- fix for shell functions on 64-bit architectures...

* Wed Mar 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add some backwards compatibility (for i in ; do something; done)

* Tue Mar 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.04 final
- remove the echo, pwd, test and kill man pages from the package,
  we're getting them from sh-utils

* Sun Mar 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.04beta5
- adapt patches
- Fix up bashrc
- Don't put in bashrc1, this should be done by the bash1 package
- use install -c instead of plain install to work on *BSD
- remove the collected patches - they're now in the base version.
- make compressed man pages optional

* Thu Mar 16 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add some collected patches for bash2
- change it over to be the main bash package
- install man-pages root:root
- obsolete bash2, bash2-doc

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description

* Thu Dec  2 1999 Ken Estes <kestes@staff.mail.com>
- updated patch to detect what executables are required by a script.

* Fri Sep 14 1999 Dale Lovelace <dale@redhat.com>
- Remove annoying ^H's from documentation

* Fri Jul 16 1999 Ken Estes <kestes@staff.mail.com>
- patch to detect what executables are required by a script.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- strip binaries.
- include bash-doc correctly.

* Thu Mar 18 1999 Preston Brown <pbrown@redhat.com>
- fixed post/postun /etc/shells work.

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- updated again text in the spec file

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- updated text in spec file.
- update to 2.03.

* Fri Feb 12 1999 Cristian Gafton <gafton@redhat.com>
- build it as bash2 instead of bash

* Tue Feb  9 1999 Bill Nottingham <notting@redhat.com>
- set 'NON_INTERACTIVE_LOGIN_SHELLS' so profile gets read

* Thu Jan 14 1999 Jeff Johnson <jbj@redhat.com>
- rename man pages in bash-doc to avoid packaging conflicts (#606).

* Wed Dec 02 1998 Cristian Gafton <gafton@redhat.com>
- patch for the arm
- use $RPM_ARCH-redhat-linux as the build target

* Tue Oct  6 1998 Bill Nottingham <notting@redhat.com>
- rewrite %pre, axe %postun (to avoid prereq loops)

* Wed Aug 19 1998 Jeff Johnson <jbj@redhat.com>
- resurrect for RH 6.0.

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- update to 2.02.1

* Thu Jun 11 1998 Jeff Johnson <jbj@redhat.com>
- Package for 5.2.

* Mon Apr 20 1998 Ian Macdonald <ianmacd@xs4all.nl>
- added POSIX.NOTES doc file
- some extraneous doc files removed
- minor .spec file changes

* Sun Apr 19 1998 Ian Macdonald <ianmacd@xs4all.nl>
- upgraded to version 2.02
- Alpha, MIPS & Sparc patches removed due to lack of test platforms
- glibc & signal patches no longer required
- added documentation subpackage (doc)

* Fri Nov 07 1997 Donnie Barnes <djb@redhat.com>
- added signal handling patch from Dean Gaudet <dgaudet@arctic.org> that
  is based on a change made in bash 2.0.  Should fix some early exit
  problems with suspends and fg.

* Mon Oct 20 1997 Donnie Barnes <djb@redhat.com>
- added %clean

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- added comment explaining why install-info isn't used
- added mips patch 

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc