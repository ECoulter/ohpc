#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%include %{_sourcedir}/OHPC_macros

%define pname spack

Name:		%{pname}%{PROJ_DELIM}
Version:	0.11.2
Release:	1%{?dist}
Summary:	HPC software package management

Group:		%{PROJ_NAME}/dev-tools
License:	LGPL
URL:		https://github.com/LLNL/spack
Source0:	https://github.com/LLNL/%{pname}/archive/v%{version}.tar.gz

BuildArch: noarch
BuildRequires:	rsync
BuildRequires:	python
Requires:	python >= 2.6
Requires: bash
Requires: curl
Requires: coreutils
Requires: subversion
Requires: hg
Requires: patch
%if 0%{?suse_version}
Requires: python-mock
%else
Requires: python2-mock
%endif

%global install_path %{OHPC_ADMIN}/%{pname}/%version
%global spack_install_path %{OHPC_PUB}/%{pname}/%version
%global spack_modules_path %{OHPC_PUB}/%{pname}-%version-modules

%ifarch x86_64
%if 0%{?centos_version} 
%global spack_arch_name linux-centos7-x86_64
%endif
%if 0%{?rhel_version}
%global spack_arch_name linux-rhel7-x86_64
%endif
%if 0%{?sles_version} 
%global spack_arch_name linux-sles12-x86_64
%endif
%endif


#No need to check for aarch, since spack isn't built for it?
%ifarch x86 
#Now, if on cent/rhel/sles/???

%endif


# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%description
Spack is a package management tool designed to support multiple versions and configurations of software on a wide variety of platforms and environments. It was designed for large supercomputing centers, where many users and application teams share common installations of software on clusters with exotic architectures, using libraries that do not have a standard ABI. Spack is non-destructive: installing a new version does not break existing installations, so many configurations can coexist on the same system.

Most importantly, Spack is simple. It offers a simple spec syntax so that users can specify versions and configuration options concisely. Spack is also simple for package authors: package files are written in pure Python, and specs allow package authors to write a single build script for many different builds of the same package.


%prep
%setup -q -n %{pname}-%{version}

%install
mkdir -p %{buildroot}%{install_path}
mkdir -p %{buildroot}%{spack_install_path}
mkdir -p %{buildroot}%{spack_modules_path}
rsync -av --exclude=.gitignore {etc,bin,lib,var,share,templates} %{buildroot}%{install_path}

sed -i "s@    tcl:.*@    tcl: %{spack_modules_path}/@" %{buildroot}%{install_path}/etc/spack/defaults/config.yaml
sed -i "s@  install_tree:.*@  install_tree: %{spack_install_path}@" %{buildroot}%{install_path}/etc/spack/defaults/config.yaml

# OpenHPC user module file
%{__mkdir} -p %{buildroot}/%{OHPC_PUB}/modulefiles/spack-apps
%{__cat} << EOF > %{buildroot}/%{OHPC_PUB}/modulefiles/spack-user/%{version}
#%Module1.0#####################################################################

module-whatis "Name: Spack"
module-whatis "Version: %{version}"
module-whatis "Category: System/Configuration"
module-whatis "Description: Spack package access for users"
module-whatis "URL: https://github.com/LLNL/spack/"

set     version             %{version}
set     SPACK_ROOT          %{install_path}

prepend-path   PATH         %{install_path}/bin
prepend-path   MODULEPATH   %{spack_modules_path}/%{spack_arch_name}

EOF
# OpenHPC admin module file
%{__mkdir} -p %{buildroot}/%{OHPC_ADMIN}/modulefiles/spack
%{__cat} << EOF > %{buildroot}/%{OHPC_ADMIN}/modulefiles/spack/%{version}
#%Module1.0#####################################################################

module-whatis "Name: Spack"
module-whatis "Version: %{version}"
module-whatis "Category: System/Configuration"
module-whatis "Description: Spack package management"
module-whatis "URL: https://github.com/LLNL/spack/"

set     version             %{version}
set     SPACK_ROOT          %{install_path}

prepend-path   PATH         %{install_path}/bin
prepend-path   MODULEPATH   %{install_path}/modules

EOF

%{__mkdir} -p %{buildroot}/%{_docdir}

%files
%{OHPC_HOME}
%doc LICENSE README.md
