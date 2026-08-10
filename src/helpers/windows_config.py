"""Module for development-time hacks for Windows."""
import configparser
import pathlib

from mesonbuild.envconfig import detect_cpu_family


ROOT = pathlib.Path(__file__).parent.parent.parent


def get_djvulibre_version() -> str:
    config = configparser.ConfigParser()
    config.read(ROOT / 'subprojects' / 'djvulibre.wrap')
    return config['wrap-git']['revision'][len('release.'):]


def get_dll_path() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent.parent.parent /
        'subprojects' /
        'djvulibre-bin' /
        'windows' /
        detect_cpu_family({}) /
        get_djvulibre_version()
    )
