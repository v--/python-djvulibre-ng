import argparse
import hashlib
import logging
import pathlib
import platform
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from urllib.error import HTTPError
from urllib.request import urlopen


@dataclass
class FileSpecifier:
    name: str
    sha256: str


@dataclass
class DjVuLibreVersionSpecifier:
    djvulibre_version: str
    arch: str
    os: str
    files: Sequence[FileSpecifier]


DJVULIBRE_VERSION_SPECS = [
    DjVuLibreVersionSpecifier(
        '3.5.30.1', 'x86_64', 'windows',
        [
            FileSpecifier('libdjvulibre.dll', '165e5c1c3e7dfb8c46edd0d03e10a63e592ea70918c818c559340ea034db24b4'),
            FileSpecifier('libjpeg.dll', '133ac0d5dd940c34320154f32181823946075aeababa200d6b3e4e7ec7debe60'),
        ],
    ),
]

BIN_URL_TEMPLATE = 'https://github.com/v--/djvulibre-bin/raw/refs/heads/master/bin/{djvulibre_version}/{os}/{arch}/{file_name}'
BIN_DIR = pathlib.Path(__file__).parent.parent / 'djvulibre' / 'bin'


logger = logging.getLogger(__name__)


def normalize_os_name(value: str) -> str:
    match value:
        case 'win32':
            return 'windows'

        case other:
            return other


def normalize_arch_name(value: str) -> str:
    match value:
        case 'AMD64':
            return 'x86_64'

        case other:
            return other


def fetch_bin() -> None:
    logging.basicConfig(format='{levelname:8} {message}', style='{')
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(
        prog='fetch-bin',
        description='Download (and verify) prebuilt libdjvulibre binary.',
    )

    parser.add_argument('--version', help='version of DjVuLibre (e.g. 3.5.30.1)', default=max(spec.djvulibre_version for spec in DJVULIBRE_VERSION_SPECS))

    # According to [1], "the most well defined field for use when declaring platform specific dependencies".
    # [1]: https://packaging.python.org/en/latest/specifications/dependency-specifiers/#defined-environment-marker-fields
    parser.add_argument('--os', help='operating system name (e.g. windows, linux)', default=sys.platform, type=normalize_os_name)
    parser.add_argument('--arch', help='target architecture (e.g. x86_64, aarch64)', default=platform.machine(), type=normalize_arch_name)
    args = parser.parse_args()

    try:
        spec = next(spec for spec in DJVULIBRE_VERSION_SPECS if spec.djvulibre_version == args.version and spec.os == args.os and spec.arch == args.arch)
    except StopIteration:
        # ruff: ignore[error-instead-of-exception]
        logger.error(f'No prebuilt binary available for DjVuLibre {args.version} on {args.os} on {args.arch}')
        raise SystemExit(1) from None

    for file_spec in spec.files:
        file_path = BIN_DIR.joinpath(file_spec.name)

        if file_path.exists():
            if hashlib.sha256(file_path.read_bytes()).hexdigest() == file_spec.sha256:
                logger.info(f'The file {file_path} has already been downloaded.')
                return
            else:
                logger.error(f"The file {file_path} already exists, but its SHA256 hash doesn't match the expected value {file_spec.sha256}.")
                raise SystemExit(1) from None

        url = BIN_URL_TEMPLATE.format(djvulibre_version=spec.djvulibre_version, os=spec.os, arch=spec.arch, file_name=file_spec.name)

        try:
            res = urlopen(url)
        except HTTPError as err:
            logger.exception(f'HTTP error while fetching {url}')
            raise SystemExit(1) from err

        result = res.read()
        logger.info(f'Successfully downloaded file from {url}.')

        if hashlib.sha256(result).hexdigest() != file_spec.sha256:
            logger.error(f"The SHA256 hash for {file_spec.name} doesn't match the expected value {file_spec.sha256}.")
            raise SystemExit(1)

        BIN_DIR.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(result)
        logger.info(f'Successfully validated hash for {file_path}.')
