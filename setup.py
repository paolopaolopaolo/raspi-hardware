from setuptools import setup
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
setup(
    name = "rpi_hardware",
    version = "0.0.1",
    author = "Dean Mercado",
    author_email = "dean@yeti.co",
    description = ("Python Class for interacting with GPIO pins on Raspberry Pi"),
    license = "BSD",
    keywords = "RPi",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['rpi_hardware', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)