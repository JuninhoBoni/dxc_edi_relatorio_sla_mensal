# python compile.py build
# python compile.py bdist_msi
from cx_Freeze import setup, Executable


version = '1.0'
program_name = 'dxc_edi_email'
long_description = 'EDI API EMAIL RELATORIO'
keywords = long_description

executables = [Executable(f"{program_name}.py", base=None, icon=f"{program_name}.ico")]
files = ['imgs', f'{program_name}.json']
options = {
    'build_exe': {
        "include_files": files,
    },
}
f'{program_name}.ico'
setup(
     name=f'{program_name}'
    ,options=options
    ,version=version
    ,author='Daniel Alves Dias Junior'
    ,description=f'{program_name}'
    ,author_email = 'daniel.alvesdias@dxc.com'
    ,maintainer = 'maintainer'
    ,maintainer_email = 'maintainer_email'
    ,url = 'dxc.com'
    ,license = 'DXC'
    ,long_description = long_description
    ,keywords = keywords
    ,platforms = 'Windows'
    ,classifiers = 'classifiers'
    ,download_url = 'download_url'
    ,provides = 'provides'
    ,requires = 'Windows'
    ,obsoletes = 'obsoletes'
    ,executables=executables
)
