#!/bin/bash

echo "Unpacking all .zip files"
for file in $(find . -name "*.zip"); do
    unzip -o "$file" -d "$(dirname "$file")" >/dev/null
done
echo "Done unpacking."

echo "Checking for .gitignore file"
if [ ! -f .gitignore ]; then
    echo ".gitignore file not found, creating one"
    cat > .gitignore <<EOL
*.csv
.DS_Store
__pycache__/
*.pyc
EOL
else
    echo ".gitignore found."
    for pattern in "*.csv" ".DS_Store" "__pycache__/" "*.pyc"; do
        if ! grep -qxF "$pattern" .gitignore; then
            echo "Adding missing pattern: $pattern"
            echo "$pattern" >> .gitignore
        fi
    done
fi

echo "Setup complete!"