
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
     name='for_DQE_2_ht_HS',
     version='0.1',
     scripts=['classes'],
     author="Hanna Soika",
     author_email="deepak.kumar.iet@gmail.com",
     description="Monitor folders for files and read fb2",
     url="https://github.com/HS9981/for_DQE_2_ht_HS.git",
     packages=setuptools.find_packages()
 )