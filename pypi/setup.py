from setuptools import setup, find_packages

setup(
    name='apiverve-mcp',
    version='1.0.1',
    description='APIVerve MCP Server - Access 306+ APIs through the Model Context Protocol',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    project_urls={
        'Documentation': 'https://docs.apiverve.com',
        'Source': 'https://github.com/apiverve/mcp-server',
        'Tracker': 'https://github.com/apiverve/mcp-server/issues',
    },
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'apiverve-mcp=apiverve_mcp.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
    keywords='mcp mcp-server model-context-protocol apiverve api claude chatgpt ai llm',
)
