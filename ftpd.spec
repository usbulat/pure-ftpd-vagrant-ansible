Name:           pure-ftpd
Version:        1.0.42
Release:        1
Summary:        FTP Server
Group:			System Environment/Daemons
License:        BSD
URL:            http://www.pureftpd.org
Source0:        ftp://ftp.pureftp.org/pub/pure-ftpd/releases/%{name}-%{version}.tar.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-buildroot
Prefix:			%{_prefix}
BuildRequires:	pam-devel, openldap-devel, mysql-devel, postgresql-devel
Requires:		perl
Provides:		ftp-server
Conflicts:		wu-ftpd proftpd ftpd in.ftpd anonftp publicfile wuftpd ftpd-BSD

%description
Pure-FTPd is a fast, production-quality, and standard-conforming FTP
server, based-on Troll-FTPd. Unlike other popular FTP servers, it has
no known security flaws, is trivial to set up, and is especially
designed for modern Linux kernels (setfsuid and sendfile capabilities)
. Features include: PAM support, IPv6, chroot()ed home directories,
virtual domains, built-in LS, anti-warez system, bandwidth throttling,
FXP, bounded ports for passive downloads, upload and download ratios,
Apache log files, and more.

%prep
%setup -n %{name}-%{version}

%build
./configure --with-everything
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_sysconfdir} \
				  %{buildroot}%{_sysconfdir}/pam.d/ \
				  %{buildroot}%{_sbindir} \
				  %{buildroot}%{_initrddir}

%makeinstall

sed -e "s|/usr/local|%{_prefix}|g" contrib/redhat.init > contrib/redhat.init_mod
install -m 755 contrib/redhat.init_mod %{buildroot}%{_initrddir}/pure-ftpd

install -m 755 configuration-file/pure-config.pl %{buildroot}%{_sbindir}
install -m 744 configuration-file/pure-ftpd.conf %{buildroot}%{_sysconfdir}

install -m 744 pam/pure-ftpd %{buildroot}%{_sysconfdir}/pam.d/

%post
chkconfig --levels 235 pure-ftpd on
systemctl start pure-ftpd.service

%clean
# rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README*
%doc %{_mandir}/man8/*
%config %{_sysconfdir}/pure-ftpd.conf
%config(noreplace) %{_initrddir}/pure-ftpd
%config(noreplace) %{_sysconfdir}/pam.d/*
%{_sbindir}/*
%{_bindir}/*

%changelog
* Sat Sep 24 2016 Bulat Yusupov <usbulat@gmail.com> - 1.0.42-0
- Initial package.
