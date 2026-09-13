from setuptools import setup, find_packages

setup(
    name="ios-duo-analyzer",
    version="1.0.0",
    description="iPhone Duo iOS Project Readiness Analyzer",
    author="kliuchev",
    url="https://github.com/kliuchev/duolipa",
    py_modules=["analyze_ios_duo"],
    package_dir={"": ".agents/skills/iphone-duo-readiness/scripts"},
    entry_points={
        "console_scripts": [
            "ios-duo-analyzer=.agents.skills.iphone-duo-readiness.scripts.analyze_ios_duo:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
