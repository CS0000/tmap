import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 5):
    sys.exit("tmap can only be used with Python 3. You are currently "
             "running Python %d." % sys.version_info.major)


setup(name='tmap',
      version='1.1.3',
      description='A topological data analysis framework implementing the TDA Mapper algorithm for population-scale microbiome data analysis ',
      author='Haokui Zhou, Tianhua Liao',
      author_email='zhouhaokui@hotmail.com',
      license='GNU',
      url='https://github.com/GPZ-Bioinfo/tmap',
      packages=find_packages(),
      package_data={'': ['test_data/*.csv',
                         'test_data/*.tsv',
                         'example/*'],
                    },
      scripts=['tmap/api/envfit_analysis.py',
               'tmap/api/Network_generator.py',
               'tmap/api/SAFE_analysis.py',
               'tmap/api/SAFE_visualization.py',
               'tmap/api/quick_vis.py'],
      extras_require={'alldeps': ('numpy')},
      install_requires=['scikit-bio',
                        'statsmodels>=0.9.0',
                        'tqdm',
                        'scikit-learn>=0.19.1',
                        'matplotlib>=2.2.2',
                        'networkx>=2.1',
                        'pandas>=0.23.0',
                        'scipy',
                        'matplotlib!=3.0.0rc2',
                        'umap-learn',
                        'rpy2',
                        'plotly',
                        ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
          "Topic :: Scientific/Engineering :: Bio-Informatics",
      ],
      zip_safe=False,
      )
