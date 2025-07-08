from setuptools import setup

setup(
    name='SSfSBT',
    version='0.1',
    description='Simple Scripts for Simple Bioinformatics Tasks',
    author='SimonHegele',
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'polars',
        'seaborn',
        ],
    package_dir={"": "."},
    entry_points={
            "console_scripts": [
                "fa2fq=fa2fq:main",
                "sample=sequence_sample:main",
                "lengths=sequence_lengths:main",
                "kallisto2nanosim=kallisto2nanosim:main",
                "busco_merge=busco_merge:main",
                "unambiguous_codes=unambiguous_codes:main",
                "rnaQUASTcompare=rnaQUASTcompare:main"
            ],
        },
)
