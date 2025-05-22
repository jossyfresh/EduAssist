import os
import sys
import subprocess

def run_tests():
    # Set environment variables
    os.environ["PYTHONPATH"] = os.getcwd()
    os.environ["TESTING"] = "True"
    os.environ["COVERAGE_FILE"] = os.path.join(os.getcwd(), ".coverage")
    
    # Run pytest with coverage
    result = subprocess.run(
        [
            "pytest", "tests/", "-v", "--cov=app", "--cov-report=term-missing",
            "--cov-config=.coveragerc"
        ],
        env=os.environ
    )
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())