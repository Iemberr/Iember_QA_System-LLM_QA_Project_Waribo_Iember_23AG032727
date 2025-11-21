# Iember QA System

A Question & Answering system powered by Hugging Face's Mistral-7B-Instruct model, featuring both CLI and Web GUI interfaces.

## 📁 Project Structure

```
Iember_QA_System/
├── LLM_QA_CLI.py                    # Command-line interface
├── app.py                            # Flask web application
├── requirements.txt                  # Python dependencies
├── example.env                       # Environment variables template
├── LLM_QA_hosted_webGUI_link.txt    # Deployment info
├── templates/
│   └── index.html                    # Web GUI template
└── static/
    └── style.css                     # Styling
```

## 🚀 Setup Instructions

### 1. Get Hugging Face API Token

1. Create a free account at [Hugging Face](https://huggingface.co/)
2. Go to Settings → Access Tokens
3. Create a new token with "Read" permissions
4. Copy the token

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
HUGGINGFACE_API_TOKEN=hf_your_actual_token_here
```

Replace `hf_your_actual_token_here` with your actual Hugging Face token.

**Alternative (temporary):**
```powershell
# Windows PowerShell
$env:HUGGINGFACE_API_TOKEN="hf_your_token_here"
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 💻 Running the Application

### CLI Application

```powershell
python LLM_QA_CLI.py
```

Example:
```
Your Question: What is machine learning?
Processed Question: what is machine learning?
Querying LLM API...

💡 Answer:
Machine learning is a subset of artificial intelligence...
```

### Web GUI Application

```powershell
python app.py
```

Then open your browser to: `http://localhost:5000`

## 🌐 Deployment Options

### Option 1: Render.com (Recommended)

1. Push your project to GitHub
2. Create a new Web Service on [Render.com](https://render.com)
3. Connect your GitHub repository
4. Set environment variable: `HUGGINGFACE_API_TOKEN`
5. Deploy!

**Build Command:** `pip install -r requirements.txt`  
**Start Command:** `gunicorn app:app`

### Option 2: PythonAnywhere

1. Upload files via Files tab
2. Create a new Web App (Flask)
3. Set WSGI configuration to point to `app.py`
4. Add `HUGGINGFACE_API_TOKEN` in environment variables
5. Reload the web app

### Option 3: Streamlit Cloud

1. Convert to Streamlit (optional)
2. Push to GitHub
3. Deploy via [streamlit.io/cloud](https://streamlit.io/cloud)

## 🧪 Testing

Ask questions like:
- "What is artificial intelligence?"
- "Explain photosynthesis"
- "What are the benefits of exercise?"
- "How does the internet work?"

## 📝 Features

✅ Natural language preprocessing (lowercasing, tokenization, punctuation removal)  
✅ Integration with Hugging Face Mistral-7B-Instruct model  
✅ Clean, responsive web interface  
✅ Command-line interface for quick queries  
✅ Error handling and loading states  

## 🔧 Troubleshooting

**Issue:** `Import "flask" could not be resolved`  
**Solution:** Install dependencies: `pip install -r requirements.txt`

**Issue:** `HUGGINGFACE_API_TOKEN environment variable not set`  
**Solution:** Set the environment variable as shown in Setup Instructions

**Issue:** Model loading takes time  
**Solution:** First API call may take 20-30 seconds as the model loads. Subsequent calls are faster.

## 📄 License

MIT License - Feel free to use and modify for educational purposes.

## 👨‍💻 Author

Created by Iember

