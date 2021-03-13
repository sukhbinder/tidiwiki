import pathlib
from setuptools import find_packages, setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="tidiwiki",
    version="0.1",
    packages=find_packages(),
    license="Private",
    description="Write tidiwiki files from Marvin Journal.pdf or Calibre Markdown files",
    long_description=README,
    long_description_content_type="text/markdown",
    author="sukhbinder",
    author_email="sukh2010@yahoo.com",
    url = 'https://github.com/sukhbinder/tidiwiki',
    keywords = ["tidiwiki", "TiddlyWiki", "convertor", "pdf", "Marvin", "Calibre"],
    entry_points={
        'console_scripts': ['to_wiki = tidiwiki.write_tidiwiki:main', ],
    },
    install_requires=["PyPDF2"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],

)
