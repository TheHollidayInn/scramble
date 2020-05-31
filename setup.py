import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='scrambler',  
     version='0.1',
     scripts=['scramble/scrambler_test.py'] ,
     author="Tony Lambropoulos",
     package_data = {
    'scramble': ['16.png'],
     },
     install_requires=['numpy', 'opencv-python'],
     author_email="tonyl7126@gmail.com",
     description="A Docker and AWS utility package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/tony7126/scrambler",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
