from setuptools import setup, find_packages
setup(name='realMonkey',
        version='1.1',
        description='realMonkey moudle',
        author='wuqiaomin,linyanyan',
        packages = find_packages('automatormonkey'),
        package_dir = {'':'automatormonkey'}, 
        package_data = {'': ['*.jar'],},
        include_package_data=True,
        scripts = ['bin/realMonkey.exe']
        )
