import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="SchoolOps Learning",
    version="0.0.1",

    description="A CDK app for learning",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "stacks"},
    packages=setuptools.find_packages(where="stacks"),

    install_requires=[
        "aws-cdk.core==1.103.0",
        "aws-cdk.aws-ec2==1.103.0",
        "aws-cdk.aws-iam==1.103.0",
        "aws-cdk.aws-ssm==1.103.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
