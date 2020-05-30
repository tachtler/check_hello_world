%define name check_hello_world
%define version 0.1.2
%define unmangled_version 0.1.2
%define unmangled_version 0.1.2
%define release 1
%define nagios_plugindir %{_libexecdir}/nagios/plugins

Summary: A basic nagios/icinga check plugin for demonstration purpose.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: GNU General Public License v3 or later (GPLv3+)
Group: Development/Libraries
Prefix: %{_prefix}
#BuildArch: noarch
BuildRequires: nagiosplugin
Requires: nagiosplugin
Vendor: Klaus Tachtler <klaus@tachtler.net>
Url: https://github.com/tachtler/check_hello_world

%description
# check\_hello\_world.py

A basic nagios/icinga check plugin for demonstration purpose.

%prep
%setup -n %{name}-%{version}.tar.gz -n %{name}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot} --prefix=%{_prefix} --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%post
mkdir -p %{nagios_plugindir}
ln -s -f /usr/bin/%{name} %{nagios_plugindir}/%{name}

%postun
if [ "$1" = "0" ]; then	
   unlink %{nagios_plugindir}/%{name}
fi

%changelog
* Sun May 17 2020 Klaus Tachtler <klaus@tachtler.net> - 0.1.2-1
- Inital RPM-BUILD for openSUSE Leap 15.1.


