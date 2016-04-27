from setuptools import setup, find_packages


required = [
    "MozillaPulse",
]

setup(
    name='pulse_replay',
    version='0.1.0.dev0',
    packages=find_packages(),
    install_requires=required,
    author='Armen Zambrano G.',
    author_email='armenzg@mozilla.com',
    license='MPL',
    url='https://github.com/armenzg/pulse_replay',
)
