import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unix-socket-server",
    version="0.0.1",
    author="Erfan Shekari",
    author_email="erfan.dp.co@gmail.com",
    description="A single-threaded server for serving in-memory files via Unix sockets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/erfanshekari/unix-socket-server",
    project_urls={
        "Bug Tracker": "https://github.com/erfanshekari/unix-socket-server",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    python_requires=">=3.0",
    packages=["unix_socket_server"],
    include_package_data=True,
    install_requires=[],
)