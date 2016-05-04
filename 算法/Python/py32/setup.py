from distutils.core import setup, Extension

MOD = 'ParkingAlgorithm'
setup(name=MOD, ext_modules=[Extension(MOD, sources=['ParkingAlgorithm.c'])])