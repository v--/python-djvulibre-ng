import os
import pathlib
import sysconfig
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


BIN_DIR = pathlib.Path(__file__).parent.parent / 'djvulibre' / 'bin'


class DjVuLibreBuildError(Exception):
    pass


class CustomBuildHook(BuildHookInterface):
    # ruff: ignore[no-self-use, unused-method-argument]
    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        if (
            (platform_tag := os.environ.get('DJVULIBRE_WHEEL_TAG')) or
            (platform_tag := sysconfig.get_platform().replace('-', '_')) == 'win_amd64'
        ):
            if not BIN_DIR.exists():
                raise DjVuLibreBuildError('Please download binaries via the fetch-bin utility.')

            build_data['pure_python'] = False
            build_data['artifacts'] = ['src/djvulibre/bin/*']
            build_data['tag'] = f'py3-none-{platform_tag}'
