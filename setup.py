from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages': [],
    'excludes': [],
    'include_files':['chromedriver.exe', 'french_company.db','foreign_company.db',
                     'pieces/charlesSebastian.ttf', 'pieces/john.jpg',],
    'includes':['tkinter', 'sqlite3', 'requests', 'json', 'webbrowser', 'pickle', 'selenium', 'pygame', 'datetime',
                'site_ste', 'site_FI', 'site_adm', 'outils', 'documentation', 'rh']
}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, target_name = 'hyperliens.exe', icon='logo.ico')
]

setup(name='hyperliens',
      version = '6.0',
      description = 'internet links and others',
      options = {'build_exe': build_options},
      executables = executables)
