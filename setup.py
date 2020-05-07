from setuptools import setup, find_packages, find_namespace_packages

setup(name='pyri',
      version='0.1.0',
      author='Jens Laufer',
      author_email='jenslaufer@gmail.com',
      install_requires=[
                        ],
      packages=find_namespace_packages(where='src'),
      package_dir={'': 'src'},
      include_package_data=True
      # package_data={'rltrader': ['rltrader/*.yml']}
      # data_files=[('', ['src/rltrader/logging.yml'])]
      )