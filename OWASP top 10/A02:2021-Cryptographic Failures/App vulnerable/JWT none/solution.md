## 1. Generating a Strong Secret Key
A key like "secret" is weak because it can be easily guessed in a brute-force attack. A strong key should be long and have high entropy (randomness). The best way to create one in Python is with the built-in secrets module.

You can generate a strong key from your terminal with this one-line command:

```Bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```
Example Output:

```
a3b8f2c1d6e5a4f7b8c3d9e2a1b7f6c5d4e3b2a1f0c9d8e7b6a5f4c3d2e1b0a9
```
This command generates a 256-bit key, which is the standard for secure applications like this.

## 2. Storing the Key Securely (Using Environment Variables)
Hardcoding the key in your code is a major security risk because it gets saved into your version control history (like Git) and is visible to anyone who can see the code. The industry standard is to use environment variables.

Step A: Install python-dotenv
This helper library makes it easy to load environment variables from a file for local development.

```Bash
pip install python-dotenv
```
Step B: Create a .env File
In the same directory as your Python script, create a file named .env and place your newly generated strong key inside it.

.env file:

```
SECRET_KEY="a3b8f2c1d6e5a4f7b8c3d9e2a1b7f6c5d4e3b2a1f0c9d8e7b6a5f4c3d2e1b0a9"
```

CRITICAL: You must add the .env file to your .gitignore file to ensure you never commit your secrets to a public repository.

.gitignore file:

```
.env
```

Step C: Update the Python Script
Now, modify your application to load the key from the environment instead of having it hardcoded.