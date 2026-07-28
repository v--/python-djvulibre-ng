py = import('python').find_installation(pure: false)

py.extension_module('ddjvuapi',
    'ddjvuapi.cpp',
    install: true,
    dependencies: [dependency('pybind11'), dependency('ddjvuapi')],
    subdir: 'djvulibre'
)

py.extension_module('miniexp',
    'miniexp.cpp',
    install: true,
    dependencies: [dependency('pybind11'), dependency('ddjvuapi')],
    subdir: 'djvulibre'
)
