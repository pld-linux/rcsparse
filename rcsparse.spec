# TODO:
# - ruby subpackage
#
%define	snap	20090405
Summary:	Library for parsing RCS files
Summary(pl.UTF-8):	Moduł do analizy plików RCS
Name:		rcsparse
Version:	0.1
Release:	0.%{snap}.1
License:	BSD
Group:		Libraries
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	b0fce6886163f58a6ba3816b9dc25e69
URL:		http://ww2.fs.ei.tum.de/~corecode/hg/rcsparse/
BuildRequires:	libtool
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library for parsing RCS files.

%package devel
Summary:	Header files and develpment documentation for rcsparse
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and develpment documentation for rcsparse.

%package -n python-rcsparse
Summary:	rcsparse Python bindings
Group:		Development/Languages/Python
%pyrequires_eq  python
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n python-rcsparse
rcsparse Python bindings.

%prep
%setup -q -n %{name}

%build
libtool --mode=compile %{__cc} %{rpmcppflags} %{rpmcflags} -shared -c rcsparse.c
libtool --mode=link %{__cc} %{rpmldflags} -shared -o librcsparse.la -rpath %{_libdir} rcsparse.lo

libtool --mode=compile %{__cc} %{rpmcppflags} %{rpmcflags} -I%{py_incdir} -shared -c py-rcsparse.c
libtool --mode=link %{__cc} %{rpmldflags} -avoid-version -module -shared -o rcsparse.la -rpath %{py_sitedir} py-rcsparse.lo librcsparse.la

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_libdir},%{py_sitedir},%{_includedir}/%{name}}

libtool --mode=install install -c librcsparse.la $RPM_BUILD_ROOT%{_libdir}
libtool --mode=install install -c rcsparse.la $RPM_BUILD_ROOT%{py_sitedir}

install *.h $RPM_BUILD_ROOT%{_includedir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}

%files -n python-rcsparse
%defattr(644,root,root,755)
%doc *.py
%attr(755,root,root) %{py_sitedir}/*.so