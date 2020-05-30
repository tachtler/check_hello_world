%define name nagiosplugin
%define version 1.3.2
%define unmangled_version 1.3.2
%define unmangled_version 1.3.2
%define release 1

Summary: The nagiosplugin library
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: Zope Public License 2.1 (ZPL), a BSD-style Open Source license.
Group: System/Monitoring
Prefix: %{_prefix}
#BuildArch: noarch
Vendor: Matthew Pounsett <matt@conundrum.com>
Url: https://nagiosplugin.readthedocs.io/en/stable/

%description
# nagiosplugin

The nagiosplugin library

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

%changelog
* Sun May 17 2020 Klaus Tachtler <klaus@tachtler.net> - 1.3.2-1
- Inital RPM-BUILD for openSUSE Leap 15.1.


