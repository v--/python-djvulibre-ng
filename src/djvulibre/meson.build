py = import('python').find_installation(pure: false)
cpp = meson.get_compiler('cpp')

pybind11_dep = dependency('pybind11')

if build_machine.system() == 'windows'
    # We should make these automatically discoverable after we figure out 64-bit builds
    libdjvu_dep = cpp.find_library('libdjvulibre', dirs: ['C:\Program Files (x86)\DjVuLibre'])
    libdjvu_incdir = include_directories('C:\Program Files (x86)\DjVuLibre\include')
else
    libdjvu_dep = dependency('ddjvuapi')
    libdjvu_incdir = include_directories()
endif

py.extension_module('ddjvuapi',
    'ddjvuapi.cpp',
    install: true,
    dependencies: [pybind11_dep, libdjvu_dep],
    include_directories: [libdjvu_incdir],
    subdir: 'djvulibre'
)

py.extension_module('miniexp',
    'miniexp.cpp',
    install: true,
    dependencies: [pybind11_dep, libdjvu_dep],
    include_directories: [libdjvu_incdir],
    subdir: 'djvulibre'
)

py.install_sources(
    '__init__.py', 'test_ddjvuapi.py', 'test_miniexp.py',
    subdir: 'djvulibre'
)
