import os
import sys
import subprocess

def run_tests():
    # Set environment variables
    os.environ["PYTHONPATH"] = os.getcwd()
    os.environ["TESTING"] = "True"
    
    # Run pytest with coverage
    result = subprocess.run(
        ["pytest", "tests/", "-v", "--cov=app", "--cov-report=term-missing"],
        env=os.environ
    )
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests()) 