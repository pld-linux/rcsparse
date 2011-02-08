# TODO
# - make ruby bindings use -base lib?
#
# Conditional build:
%bcond_without	python	# build python bindings
%bcond_without	ruby	# build ruby bindings

%define		snap	20090807
%define		rel		1
Summary:	Library for parsing RCS files
Summary(pl.UTF-8):	Moduł do analizy plików RCS
Name:		rcsparse
Version:	0.1
Release:	0.%{snap}.%{rel}
License:	BSD
Group:		Libraries
Source0:	http://ww2.fs.ei.tum.de/~corecode/hg/rcsparse/archive/tip.tar.bz2#/%{name}.tbz2
# Source0-md5:	360ad1d3e0410d30abea710ce758c396
Patch0:		ruby19.patch
URL:		http://ww2.fs.ei.tum.de/~corecode/hg/rcsparse/
BuildRequires:	libtool
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
%endif
%if %{with ruby}
BuildRequires:	rpmbuild(macros) >= 1.272
BuildRequires:	ruby >= 1:1.8
BuildRequires:	ruby-devel
BuildRequires:	ruby-modules
%endif
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

%package -n ruby-rcsparse
Summary:	rcsparse Ruby bindings
Group:		Development/Languages
%{?ruby_mod_ver_requires_eq}
# does not link with base
#Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n ruby-rcsparse
rcsparse Ruby bindings.

%prep
%setup -qc
mv %{name}-*/* .
%patch0 -p1

%build
libtool --tag=CC --mode=compile %{__cc} %{rpmcppflags} %{rpmcflags} -fPIC -shared -c rcsparse.c
libtool --tag=CC --mode=link %{__cc} %{rpmldflags} %{rpmcflags} -shared -o librcsparse.la -rpath %{_libdir} rcsparse.lo

%if %{with python}
libtool --tag=CC --mode=compile %{__cc} %{rpmcppflags} %{rpmcflags} -I%{py_incdir} -shared -c py-rcsparse.c
libtool --tag=CC --mode=link %{__cc} %{rpmldflags} %{rpmcflags} -avoid-version -module -shared -o rcsparse.la -rpath %{py_sitedir} py-rcsparse.lo librcsparse.la
%endif

%if %{with ruby}
%{__ruby} extconf.rb
%{__make} -j1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{py_sitedir},%{_includedir}/%{name}}
libtool --mode=install install -p -c librcsparse.la $RPM_BUILD_ROOT%{_libdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/librcsparse.a
cp -p *.h $RPM_BUILD_ROOT%{_includedir}/%{name}

%if %{with python}
libtool --mode=install install -p -c rcsparse.la $RPM_BUILD_ROOT%{py_sitedir}
rm -f $RPM_BUILD_ROOT%{py_sitedir}/rcsparse.la
rm -f $RPM_BUILD_ROOT%{py_sitedir}/rcsparse.a
%endif

%if %{with ruby}
%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT
%attr(755,root,root) %{_libdir}/librcsparse.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librcsparse.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librcsparse.so
%{_libdir}/librcsparse.la
%{_includedir}/%{name}

%if %{with python}
%files -n python-rcsparse
%defattr(644,root,root,755)
%doc testmodule.py
%attr(755,root,root) %{py_sitedir}/rcsparse.so
%endif

%if %{with ruby}
%files -n ruby-rcsparse
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_sitearchdir}/rcsfile.so
%endif
