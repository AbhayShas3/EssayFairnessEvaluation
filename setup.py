import subprocess
import sys

def check_and_install(package_name, import_name=None):
    """Check if package is installed, install if not"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✓ {package_name} is installed")
        return True
    except ImportError:
        print(f"✗ {package_name} not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "-q"])
        print(f"✓ {package_name} installed")
        return True

print("Setting up environment...\n")

# Check required packages
packages = [
    ("transformers", "transformers"),
    ("torch", "torch"),
    ("scipy", "scipy"),
    ("pandas", "pandas"),
    ("numpy", "numpy"),
]

for package, import_name in packages:
    check_and_install(package, import_name)

print("\n All packages ready!")
print("\nNext steps:")
print("1. Edit step1_extract_essays.py and update dataset_path (line 80)")
print("2. Run: python3 step1_extract_essays.py")