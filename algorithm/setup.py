from distutils.core import setup, Extension

MOD = 'Parking'
setup(name=MOD, ext_modules=[Extension(MOD, sources=['Parking.c'])])