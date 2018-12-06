from setuptools import setup


def readme():
    with open('README.md') as file:
        return file.read()


setup(
    name='ppb-vector',
    version='0.4.0rc1',
    packages=['ppb_vector'],
    url='http://github.com/pathunstrom/ppb-vector',
    license='',
    author='Piper Thunstrom',
    author_email='pathunstrom@gmail.com',
    description='A basic game development Vector2 class.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=True,
)
