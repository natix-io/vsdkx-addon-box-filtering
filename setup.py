from setuptools import setup, find_namespace_packages

setup(
    name='vsdkx-addon-box-filtering',
    url='https://github.com/natix-io/vsdkx-addon-box-filtering.git',
    author='Giorgi',
    author_email='gd@gegidze.com',
    namespace_packages=['vsdkx', 'vsdkx.addon'],
    packages=find_namespace_packages(include=['vsdkx*']),
    dependency_links=[
        'https://github.com/natix-io/vsdkx-core.git#egg=vsdkx-core'
    ],
    install_requires=[
        'vsdkx-core',
        'numpy>=1.18.5',
        'torch==1.9.0',
        'torchvision==0.10.0'
    ],
    version='1.0',
)
