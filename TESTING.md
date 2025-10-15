# 🧪 Testing Guide

This guide helps you test your Knowledge Base Search Engine to ensure everything works correctly.

## Quick Test Checklist

### 1. Installation Test

```bash
# Run setup
./setup.sh  # or setup.bat on Windows

# Expected output:
✅ Python version check
✅ Virtual environment created
✅ Dependencies installed
✅ Documents folder created
```

### 2. Document Loading Test

```bash
# Activate environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start server
cd backend
uvicorn app.main:app --reload
```

**Expected console output:**
```
[Info] Loading documents from /path/to/docs...
[Info] Loaded text file: cn.txt
[Info] Created 2 chunks from cn.txt
[Info] Loaded text file: dbms.txt
[Info] Created 45 chunks from dbms.txt
[Info] Loaded PDF file: document.pdf
[Info] Created 12 chunks from document.pdf
[Info] Total documents loaded: 59
[Info] FAISS index created with 59 vectors
```

✅ **Pass if:** All documents load without errors

❌ **Fail if:** 
- "No documents loaded"
- PDF extraction errors
- Memory errors

### 3. API Endpoints Test

#### Test 1: Health Check

```bash
curl http://127.0.0.1:8000/
```

**Expected response:**
```json
{
  "message": "Knowledge Base Search Engine API",
  "status": "running",
  "docs_loaded": 59
}
```

✅ Pass if: Status is "running" and docs_loaded > 0

---

#### Test 2: Stats Endpoint

```bash
curl http://127.0.0.1:8000/stats
```

**Expected response:**
```json
{
  "total_documents": 59,
  "index_size": 59,
  "embedding_dimension": 384,
  "model": "all-MiniLM-L6-v2"
}
```

✅ Pass if: All values are correct

---

#### Test 3: GET Query

```bash
curl "http://127.0.0.1:8000/query/?query=What%20is%20a%20primary%20key"
```

**Expected response:**
```json
{
  "query": "What is a primary key",
  "answer": "Based on the available documents:\n\nA Primary Key...",
  "sources": [
    {
      "file": "dbms.txt",
      "chunk": 9,
      "similarity": 0.89
    }
  ],
  "num_docs_searched": 59
}
```

✅ Pass if:
- Answer is not empty
- Sources are provided
- Similarity > 0.5

---

#### Test 4: POST Query

```bash
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain normalization", "top_k": 3}'
```

**Expected response:**
```json
{
  "query": "Explain normalization",
  "answer": "Based on the available documents:\n\nNormalization is...",
  "sources": [...],
  "num_docs_searched": 59
}
```

✅ Pass if: Same as GET query test

---

#### Test 5: Error Handling

**Empty query:**
```bash
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": ""}'
```

**Expected response:**
```json
{
  "detail": "Query is required"
}
```

✅ Pass if: Error message is returned

---

### 4. Frontend Test

1. Open `frontend/index.html` in browser
2. Check UI loads correctly
3. Test each feature:

**Test Case 1: Empty Query**
- Input: (leave empty)
- Click "Search"
- Expected: "⚠️ Please enter a query."

**Test Case 2: Valid Query**
- Input: "What is HTTP?"
- Click "Search"
- Expected: 
  - Loading indicator appears
  - Answer displays
  - Sources shown
  - Similarity scores visible

**Test Case 3: Backend Down**
- Stop backend server
- Try to search
- Expected: Error message with helpful instructions

**Test Case 4: Complex Query**
- Input: "Explain the difference between primary and foreign keys with examples"
- Expected: Comprehensive answer from multiple sources

**Test Case 5: Enter Key**
- Type query
- Press Enter (don't click button)
- Expected: Search executes

---

### 5. Performance Test

#### Test 1: Response Time

```bash
time curl -s "http://127.0.0.1:8000/query/?query=test" > /dev/null
```

✅ Pass if: Response time < 1 second for 50+ documents

---

#### Test 2: Multiple Queries

Run 10 queries in sequence:

```bash
for i in {1..10}; do
  curl -s "http://127.0.0.1:8000/query/?query=test$i" > /dev/null
  echo "Query $i completed"
done
```

✅ Pass if: All queries complete without errors

---

#### Test 3: Concurrent Requests

```bash
# Install Apache Bench (ab) if not installed
# macOS: brew install httpd
# Ubuntu: sudo apt-get install apache2-utils

ab -n 100 -c 10 "http://127.0.0.1:8000/query/?query=test"
```

✅ Pass if: 
- 0% failed requests
- Average response time < 500ms

---

### 6. Document Ingestion Test

#### Test PDF with Text

1. Add a text-based PDF to `backend/app/docs/`
2. Restart server
3. Check console output

✅ Pass if: PDF is loaded and chunked

---

#### Test Image-based PDF

1. Add an image-based (scanned) PDF
2. Restart server
3. Check console output

Expected: Warning message (this is OK - OCR not implemented)

---

#### Test Large Document

1. Add a document with 10,000+ words
2. Restart server
3. Check chunks created

✅ Pass if: Multiple chunks created (20+ chunks expected)

---

### 7. Retrieval Accuracy Test

Test with known queries:

| Query | Expected Source | Min Similarity |
|-------|----------------|----------------|
| "What is HTTP?" | cn.txt | 0.8 |
| "Define primary key" | dbms.txt | 0.85 |
| "ACID properties" | dbms.txt | 0.8 |

Run each query and verify:
✅ Correct source file
✅ Similarity above threshold
✅ Relevant answer

---

### 8. Edge Cases

#### Test 1: Very Long Query

```bash
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "'"$(yes "What is a database? " | head -100 | tr -d '\n')"'"}'
```

✅ Pass if: Handles gracefully (no crash)

---

#### Test 2: Special Characters

```bash
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What is <html> & \"special\" chars?"}'
```

✅ Pass if: Returns valid response

---

#### Test 3: Non-English Characters

```bash
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "データベース"}'
```

✅ Pass if: Handles without error (may return "no info found")

---

#### Test 4: Query Not in Docs

```bash
curl "http://127.0.0.1:8000/query/?query=quantum%20physics"
```

✅ Pass if: Returns answer (even if not highly relevant)

---

## Automated Test Script

Save as `test_api.py` in the `backend` folder:

```python
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "status" in response.json()
    print("✅ Health check passed")

def test_stats():
    print("Testing stats endpoint...")
    response = requests.get(f"{BASE_URL}/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_documents"] > 0
    print(f"✅ Stats passed - {data['total_documents']} documents loaded")

def test_query_get():
    print("Testing GET query...")
    response = requests.get(f"{BASE_URL}/query/?query=What is HTTP")
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    print("✅ GET query passed")

def test_query_post():
    print("Testing POST query...")
    response = requests.post(
        f"{BASE_URL}/search",
        json={"query": "Explain normalization", "top_k": 3}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["sources"]) <= 3
    print("✅ POST query passed")

def test_empty_query():
    print("Testing empty query...")
    response = requests.post(
        f"{BASE_URL}/search",
        json={"query": ""}
    )
    assert response.status_code == 400
    print("✅ Empty query validation passed")

def test_response_time():
    print("Testing response time...")
    start = time.time()
    response = requests.get(f"{BASE_URL}/query/?query=test")
    end = time.time()
    assert response.status_code == 200
    assert (end - start) < 2.0  # Should respond within 2 seconds
    print(f"✅ Response time: {end - start:.2f}s")

if __name__ == "__main__":
    print("🧪 Running API tests...\n")
    try:
        test_health_check()
        test_stats()
        test_query_get()
        test_query_post()
        test_empty_query()
        test_response_time()
        print("\n🎉 All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to server. Is it running?")
```

**Run tests:**
```bash
cd backend
pip install requests
python test_api.py
```

---

## Test Results Template

Document your test results:

```markdown
## Test Results - [Date]

### Environment
- OS: macOS 14.6.0
- Python: 3.11.5
- Documents: 59 chunks

### Results

| Test | Status | Notes |
|------|--------|-------|
| Installation | ✅ Pass | 2m 30s |
| Document Loading | ✅ Pass | 57 docs loaded |
| Health Check | ✅ Pass | - |
| Stats Endpoint | ✅ Pass | - |
| GET Query | ✅ Pass | 450ms avg |
| POST Query | ✅ Pass | 420ms avg |
| Error Handling | ✅ Pass | - |
| Frontend UI | ✅ Pass | All features work |
| Response Time | ✅ Pass | <500ms |
| Retrieval Accuracy | ✅ Pass | >0.8 similarity |
| Edge Cases | ✅ Pass | All handled |

### Issues Found
- None

### Overall: ✅ PASS
```

---

## Debugging Failed Tests

### Issue: Documents not loading

**Symptoms:**
- "No documents loaded" message
- Index size = 0

**Solutions:**
1. Check docs folder exists: `backend/app/docs/`
2. Verify files are `.txt` or `.pdf`
3. Check file permissions
4. Look for error messages in console

---

### Issue: Low similarity scores

**Symptoms:**
- Similarity < 0.5 for relevant queries
- Wrong sources returned

**Solutions:**
1. Check document content matches query domain
2. Try different chunk sizes
3. Verify embeddings model loaded correctly
4. Add more documents

---

### Issue: Slow response times

**Symptoms:**
- Response time > 2 seconds
- API timeouts

**Solutions:**
1. Reduce chunk size
2. Use fewer documents for testing
3. Check system resources (RAM, CPU)
4. Optimize FAISS index

---

### Issue: Frontend not connecting

**Symptoms:**
- "Error connecting to backend"
- CORS errors in console

**Solutions:**
1. Verify backend is running on port 8000
2. Check CORS settings in `main.py`
3. Try different browser
4. Check firewall settings

---

## CI/CD Testing

For GitHub Actions, create `.github/workflows/test.yml`:

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install requests pytest
      - name: Run tests
        run: |
          cd backend
          python test_api.py &
          sleep 10
          pytest
```

---

Good luck with testing! 🧪

