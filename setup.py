from setuptools import setup, find_packages

setup(
    name='pytube-tool',
    version='0.1.3',
    description='A CLI tool to download YouTube Videos by giving an URL',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hatix Ntsoa',
    author_email='hatixntsoa@gmail.com',
    url='https://github.com/h471x/youtube_downloader',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pytube=pytube.main:main',
        ],
    },
)