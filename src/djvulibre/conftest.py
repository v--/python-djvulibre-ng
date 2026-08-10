import os


if os.name == 'nt':
    from helpers.windows_config import get_dll_path

    os.add_dll_directory(get_dll_path())  # type: ignore[attr-defined]
