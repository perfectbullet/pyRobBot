import os
import re

from setuptools import find_packages, setup


extra_require = { }


def main():
    setup(
        name="pyrobbot",
        version='pyrobbot',
        author="zhoujing",
        author_email="121531845" "@" "qq.com",
        description="Chat with GPT LLMs over voice, text or both.",
        long_description=open("README.md", "r", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        keywords=["Chat", "GPT", "LLMs", "zhoujing", "ChatGPT", "pyrobbot", "voice", "text"],
        license="Apache 2.0 License",
        url="git@github.com:perfectbullet/pyRobBot.git",
        package_dir={"": "pyrobbot"},
        packages=find_packages("pyrobbot"),
        python_requires=">=3.8.0",
        entry_points={"console_scripts": ["pyrobbot = pyrobbot.__main__:main"]},
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
        ],
    )


if __name__ == "__main__":
    main()
