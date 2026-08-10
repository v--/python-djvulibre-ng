py = import('python').find_installation(pure: false)
cpp = meson.get_compiler('cpp')

pybind11_dep = dependency('pybind11')

if build_machine.system() == 'windows'
    djvulibre_version = run_command(
        ['python', '-c', 'from helpers.windows_config import get_djvulibre_version; print(get_djvulibre_version())'],
        env: {'PYTHONPATH': join_paths(meson.project_source_root(), 'src')},
        check: true
    ).stdout().strip()

    djvulibre_subproj = subproject('djvulibre')
    libdjvu_inc = djvulibre_subproj.get_variable('djvulibre_inc')

    djvulibre_bin_subproj = subproject(
        'djvulibre-bin',
        default_options: {
            'djvulibre_version': djvulibre_version,
            'cpu_family': build_machine.cpu_family()
        }
    )

    libdjvu_dep = djvulibre_bin_subproj.get_variable('libdjvu_dep')
else
    libdjvu_dep = dependency('ddjvuapi')
    libdjvu_inc = include_directories()
endif

py.extension_module('ddjvuapi',
    'ddjvuapi.cpp',
    install: true,
    dependencies: [pybind11_dep, libdjvu_dep],
    include_directories: [libdjvu_inc],
    subdir: 'djvulibre'
)

py.extension_module('miniexp',
    'miniexp.cpp',
    install: true,
    dependencies: [pybind11_dep, libdjvu_dep],
    include_directories: [libdjvu_inc],
    subdir: 'djvulibre'
)

py.install_sources(
    '__init__.py', 'test_ddjvuapi.py', 'test_miniexp.py',
    subdir: 'djvulibre'
)
