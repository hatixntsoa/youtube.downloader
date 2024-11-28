from setuptools import setup, find_packages

setup(
    name='pytube-tool',
    version='0.1.2',
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
    install_requires=[
        'python-dotenv==1.0.1',
        'yt_dlp==2024.11.18',
        'moviepy==2.0.0.dev2',
        'setuptools==63.2.0',
        'inquirer==3.4.0'
    ],
    entry_points={
        'console_scripts': [
            'pytube=pytube.main:main',
        ],
    },
)