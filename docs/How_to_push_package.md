```
#!/bin/bash

# Tag the version
git tag <whatever version>

# Remove old builds
rm dist/*

# Build it
python3 setup.py sdist bdist_wheel

# Send it to test environment
python3 -m twine upload -u $API_USER -p $API_TOKEN --repository-url https://test.pypi.org/legacy/ dist/*
# u: __token__
# p: API key in the keyvault

# Install the pkg
# pip install -i https://test.pypi.org/simple/ sensorizer
```
