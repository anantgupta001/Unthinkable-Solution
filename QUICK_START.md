# ⚡ Quick Start Guide

Get your Knowledge Base Search Engine running in 5 minutes!

## 🚀 Super Quick Start (Copy-Paste These Commands)

### macOS/Linux
```bash
# 1. Navigate to project
cd hue-hue-hue-master

# 2. Run setup (first time only)
chmod +x setup.sh run.sh
./setup.sh

# 3. Add your documents
# Put .txt or .pdf files in: backend/app/docs/

# 4. Start the server
./run.sh

# 5. Open browser
# Open frontend/index.html in your browser
# Start searching! 🔍
```

### Windows
```cmd
# 1. Navigate to project
cd hue-hue-hue-master

# 2. Run setup (first time only)
setup.bat

# 3. Add your documents
# Put .txt or .pdf files in: backend\app\docs\

# 4. Start the server
run.bat

# 5. Open browser
# Open frontend\index.html in your browser
# Start searching! 🔍
```

---

## 📋 Common Commands Cheat Sheet

| Task | Command |
|------|---------|
| **First-time setup** | `./setup.sh` or `setup.bat` |
| **Start server** | `./run.sh` or `run.bat` |
| **Stop server** | Press `Ctrl + C` |
| **Check if running** | Visit http://127.0.0.1:8000 |
| **View API docs** | Visit http://127.0.0.1:8000/docs |
| **Add documents** | Copy files to `backend/app/docs/` |
| **Reload documents** | Restart server |
| **View logs** | Check terminal/console output |

---

## 🔍 Using the Search Engine

### Via Web UI (Recommended)
1. Open `frontend/index.html` in browser
2. Type your question
3. Click "Search" or press Enter
4. View answer and sources

### Via API (curl)
```bash
# GET request
curl "http://127.0.0.1:8000/query/?query=What%20is%20HTTP"

# POST request
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain normalization", "top_k": 3}'
```

### Via API (Python)
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/search",
    json={"query": "What is a primary key?", "top_k": 3}
)

data = response.json()
print(data['answer'])
```

---

## 📂 Where to Put Files

```
backend/app/docs/          ← PUT YOUR DOCUMENTS HERE
├── your_notes.txt         ✅ Text files
├── lecture.pdf            ✅ PDF files
├── study_guide.txt        ✅ More text
└── research_paper.pdf     ✅ More PDFs
```

**Supported formats:**
- ✅ `.txt` - Plain text files
- ✅ `.pdf` - PDF documents (text-based)

**Not supported (yet):**
- ❌ `.docx` - Word documents
- ❌ `.pptx` - PowerPoint
- ❌ Image-based PDFs (scanned documents)

---

## 🐛 Troubleshooting in 30 Seconds

### Problem: "No documents loaded"
**Fix:** Add `.txt` or `.pdf` files to `backend/app/docs/`

### Problem: "Connection refused"
**Fix:** Make sure server is running with `./run.sh`

### Problem: "Module not found"
**Fix:** Run `./setup.sh` first

### Problem: "Port 8000 already in use"
**Fix:** 
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9  # macOS/Linux
# or restart your computer
```

### Problem: PDF not extracting text
**Fix:** Some PDFs are images. Convert to text first using online OCR tools.

---

## 📊 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.8+ | 3.11+ |
| RAM | 2GB | 4GB+ |
| Disk Space | 1GB | 2GB+ |
| CPU | 2 cores | 4+ cores |
| OS | Any | macOS/Linux/Windows 10+ |

---

## ⏱️ Installation Time Estimates

| Step | Time |
|------|------|
| Download dependencies | 2-3 min |
| Install packages | 1-2 min |
| Setup environment | 30 sec |
| **Total first run** | **3-5 min** |
| Subsequent starts | **5-10 sec** |

---

## 🎯 Sample Queries to Try

Once running, try these queries:

1. **"What is HTTP?"** 
   - Tests basic retrieval

2. **"Explain the difference between primary and foreign keys"**
   - Tests comparison understanding

3. **"What are ACID properties in DBMS?"**
   - Tests multi-concept retrieval

4. **"How does normalization reduce redundancy?"**
   - Tests reasoning

5. **"Give me an example of a JOIN query"**
   - Tests code example retrieval

---

## 📖 Documentation Map

Need more help? Check these docs:

| File | Purpose | When to Read |
|------|---------|--------------|
| **README.md** | Complete guide | First time setup |
| **QUICK_START.md** | This file | Quick reference |
| **DEMO_GUIDE.md** | Video guide | Making demo video |
| **TESTING.md** | Test procedures | Verifying it works |
| **PROJECT_SUMMARY.md** | Overview | Understanding the project |

---

## 🆘 Still Stuck?

1. **Read the error message** - It usually tells you what's wrong
2. **Check README.md** - Section: "Troubleshooting"
3. **Check TESTING.md** - Run the tests
4. **Verify Python version** - Run `python3 --version`
5. **Reinstall** - Delete `venv/` folder and run `./setup.sh` again

---

## 🎓 Next Steps After Setup

### Beginner
- [ ] Add your study notes to `docs/`
- [ ] Try the sample queries above
- [ ] Explore the web UI

### Intermediate
- [ ] Test the API with curl/Postman
- [ ] Read the source code in `backend/app/`
- [ ] Experiment with different chunk sizes

### Advanced
- [ ] Integrate a real LLM (GPT-4, Claude)
- [ ] Add new features from the roadmap
- [ ] Deploy to cloud (Heroku, AWS, GCP)

---

## 💡 Pro Tips

1. **Organize your docs** - Use clear filenames
2. **Start small** - Test with 2-3 docs first
3. **Check logs** - Server output shows what's happening
4. **Restart after adding docs** - Server loads docs at startup
5. **Keep docs focused** - Better results with topic-specific docs

---

## 🔗 Quick Links

- API Root: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/
- Stats: http://127.0.0.1:8000/stats
- Frontend: Open `frontend/index.html`

---

## 📞 Emergency Commands

```bash
# Kill all Python processes (use carefully!)
pkill python

# Remove everything and start fresh
rm -rf venv/
./setup.sh

# Check if port 8000 is free
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

---

**Remember:** The first run takes 3-5 minutes. After that, it's instant! 🚀

---

Made with ❤️ for easy deployment and demos

