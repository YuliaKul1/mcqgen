from setuptools import find_packages, setup

setup(
    name='mcgenerator',
    version='0.0.1',
    author='Yulia',
    author_email='ulechek.kul@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()

)