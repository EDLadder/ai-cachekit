from setuptools import setup, find_packages

setup(
    name='ai-cachekit',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    description='Lightweight caching library for AI/LLM API responses',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Eugen D',
    license='MIT',
    python_requires='>=3.8',
)
