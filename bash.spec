Version: 2.04
Name: bash
Summary: The GNU Bourne Again shell (bash) version %{version}.
Release: 21
Group: System Environment/Shells
Copyright: GPL
Source0: ftp://ftp.gnu.org/gnu/bash/bash-%{version}.tar.gz
Source1: bashrc
Source2: ftp://ftp.gnu.org/gnu/bash/bash-doc-%{version}.tar.gz
Source3: dot-bashrc
Source4: dot-bash_profile
Source5: dot-bash_logout
Patch0: bash-2.03-paths.patch
Patch1: bash-2.02-security.patch
Patch2: bash-2.04-arm.patch
Patch3: bash-2.03-profile.patch
Patch5: bash-2.04-requires.patch
Patch6: bash-2.04-compat.patch
Patch7: bash-2.04-shellfunc.patch
Patch8: bash-ia64.patch
Patch9: bash-2.04-export.patch
Prefix: %{_prefix}
Requires: mktemp
Provides: bash2
Obsoletes: bash2 etcskel
BuildRoot: /var/tmp/%{name}-root

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

Documentation for bash version %{version} is contained in the bash-doc 
package.

%package doc
Group: Documentation
Summary: Documentation for the GNU Bourne Again shell (bash) version %{version}.
Obsoletes: bash2-doc

%description doc
The bash-doc package contains documentation for the GNU Bourne
Again shell version %{version}.

%prep
%setup -q -a 2
%patch0 -p1 -b .paths
%patch1 -p1 -b .security
%patch2 -p1 -b .arm
%patch3 -p1 -b .profile
%patch5 -p1 -b .requires
%patch6 -p1 -b .compat
%patch7 -p1 -b .shellfunc
%patch8 -p1 -b .ia64
%patch9 -p0
echo %{version} > _distribution
echo %{release} > _patchlevel

%build
#CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
#    ./configure --prefix=$RPM_BUILD_ROOT/usr $RPM_ARCH-redhat-linux

%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall
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
done

# now turn man.pages into a filelist for the man subpackage
cat man.pages | tr -s ' ' '\n' | sed '
1i\
%defattr(0644,root,root,0755)
s:^:%{_mandir}/man1/:
s/$/.1*/
' > ../man.pages

{ cd $RPM_BUILD_ROOT
  mkdir ./bin
  mv ./usr/bin/bash ./bin
  ln -sf bash ./bin/bash2
  ln -sf bash ./bin/sh
  strip ./bin/* || :
  gzip -9nf .%{_infodir}/bash.info
  rm -f .%{_infodir}/dir
}
mkdir -p $RPM_BUILD_ROOT/etc/skel
install -c -m644 $RPM_SOURCE_DIR/bashrc $RPM_BUILD_ROOT/etc/bashrc
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

%files -f man.pages
%defattr(-,root,root)
%doc CHANGES COMPAT NEWS NOTES CWRU/POSIX.NOTES
%doc doc/FAQ doc/INTRO doc/article.ms
%doc examples/bashdb/ examples/functions/ examples/misc/
%doc examples/scripts.noah/ examples/scripts.v2/ examples/scripts/
%doc examples/startup-files/
%config(noreplace) /etc/bashrc
%config(noreplace) /etc/skel/.b*
/bin/sh
/bin/bash
/bin/bash2
%{_infodir}/bash.info*
%{_mandir}/man1/bash.1*
%{_mandir}/man1/builtins.1*
%{_prefix}/bin/bashbug
%{_mandir}/man1/bashbug.1*

%files doc
%defattr(-,root,root)
%doc doc/*.ps doc/*.0 doc/*.html doc/article.txt

%changelog
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
