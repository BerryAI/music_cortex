from setuptools import setup, find_packages

setup(name='OpenMRS',
      version='0.0.1',
      description='Open source music recommendation.',
      packages=find_packages('.'),
      include_package_data=True,
      #data_files=[('OpenMRS/data', ['OpenMRS/data/acai_game_user_ratings.json'])],
      zip_safe=False)
