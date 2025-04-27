from setuptools import setup, find_packages

setup(
    name="eduassist",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6",
        "pydantic==2.4.2",
        "pydantic-settings==2.0.3",
        "supabase==1.0.3",
        "python-dotenv==1.0.0",
        "pytest==7.4.3",
        "pytest-asyncio==0.21.1",
        "httpx==0.25.1",
        "pytest-cov==4.1.0",
    ],
) 