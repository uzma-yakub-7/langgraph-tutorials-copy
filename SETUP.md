# Running Files in VS Code

# Get Groq API Key
- Go to https://console.groq.com
- Sign up with your Google account
- Click "API Keys" on the left sidebar
- Click "Create API Key"
- Copy the key

# Create .env File
- Inside your project folder, create a file called .env
- Add this inside: GROQ_API_KEY=paste_your_key_here
- Save the file

# Install Packages
- Open VS Code
- Go to File → Add Folder to Workspace
- Select your folder
- Open VS Code terminal (Ctrl + backtick)
- Change terminal to Command Prompt
- In VS Code terminal, run: pip install langgraph langchain-groq python-dotenv . Press Enter

