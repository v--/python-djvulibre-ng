project(
    'djvulibre',
    'cpp',
    version: run_command(['python', '-c', 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])'], check: true).stdout().strip(),
    meson_version: '>=1.2.0',
    default_options: [
        'cpp_std=c++11',
    ],
)

subdir('src/djvulibre')
