#!/usr/bin/env python

from abc import abstractmethod

try:
    from pip._internal import main as pipmain
except ImportError:
    from pip import main as pipmain

class DownloadingError(Exception):
    '''Error during downloading the package'''

class InstallationError(Exception):
    '''Error during installing the package'''

class UnInstallationError(Exception):
    '''Error during uninstalling the package'''

class PackageManager(object):
    @abstractmethod
    def download(self, package_name, version=None):
        pass

    @abstractmethod
    def install(self, package_name, version=None):
        pass

    @abstractmethod
    def uninstall(self, package_name):
        pass

class PipManager(PackageManager):
    def _run_pip_command(self, command, *args):
            pipmain([command] + list(args))

    def _install_package(self, package_name, version=None, download_only=False):
        requested_package = '{}=={}'.format(package_name, version) if version is not None else package_name
        if not download_only:
            if self._run_pip_command('install', requested_package) == 1:
                raise InstallationError()
        else:
            if self._run_pip_command('download', requested_package) == 1:
                raise DownloadingError()

    def download(self, package_name, version=None):
        self._install_package(package_name, download_only=True)

    def install(self, package_name, version=None):
        self._install_package(package_name, download_only=False)

    def uninstall(self, package_name):
        if pipmain('uninstall', package_name) == 1:
            raise UnInstallationError()

if __name__ == '__main__':
    pip_manager = PipManager()
    pip_manager.install('pip')
