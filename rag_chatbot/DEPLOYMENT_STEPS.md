# 🚀 Hugging Face Space Deployment - Step by Step

## ✅ Complete Deployment Checklist

### Step 1: Environment Variables (Secrets) Setup

**Location**: Hugging Face Space Settings → Repository Secrets

**Required Secret:**
- **Name**: `COHERE_API_KEY`
- **Value**: Your Cohere API key
- **Get Key**: https://dashboard.cohere.com/api-keys

**Steps:**
1. Go to: https://huggingface.co/spaces/faiza-faisal/Physical-Ai-Humanoid-Textbook/settings
2. Scroll to "Repository secrets" section
3. Click "New secret" / "Add secret"
4. Name: `COHERE_API_KEY`
5. Value: [Paste your Cohere API key]
6. Click "Add secret" / "Save"

**Important Notes:**
- ❌ OpenAI API key **NOT needed** (code uses Cohere)
- ❌ Qdrant API key **NOT needed** (code uses ChromaDB local storage)
- ❌ Neon DB keys **NOT needed**
- ✅ Only `COHERE_API_KEY` required

---

### Step 2: Database Pre-build (Recommended)

Hugging Face Spaces par database automatically create nahi ho sakti reliably. Pre-build karke commit karo.

#### 2.1: Locally Build Database

```bash
# 1. Ensure .env file has COHERE_API_KEY
# .env file content:
COHERE_API_KEY=your_actual_cohere_api_key_here

# 2. Build database
python setup_db.py --docs-dir ./docs

# 3. Verify build
# Check chroma_db/ folder has files:
dir chroma_db
# Should see: chroma.sqlite3 and collection folders
```

#### 2.2: Update .gitignore (Temporary)

Database files ko commit karne ke liye `.gitignore` se `chroma_db/` temporarily remove karo:

**Option A: Comment out (Recommended)**
```gitignore
# ChromaDB (temporarily enabled for deployment)
# chroma_db/
# *.db
```

**Option B: Remove line**
- `.gitignore` file open karo
- Line 19: `chroma_db/` ko remove ya comment out karo
- Line 20: `*.db` ko remove ya comment out karo

#### 2.3: Commit Database Files

```bash
# Add database to git
git add chroma_db/

# Commit
git commit -m "Add pre-built vector database for deployment"

# Push to Hugging Face Space
git push -u origin master:main
```

**Note**: Database size check karo - agar > 100MB hai to Git LFS use karo ya external database consider karo.

---

### Step 3: Verify Deployment

#### 3.1: Check Space Build

1. Space page par jao: https://huggingface.co/spaces/faiza-faisal/Physical-Ai-Humanoid-Textbook
2. "Logs" tab check karo - build errors nahi hone chahiye
3. Build complete hone ka wait karo (2-5 minutes)

#### 3.2: Test App

1. "App" tab par jao
2. Sidebar → "ℹ️ System Info" expand karo
3. Check: "Cohere API Key: ✅" dikhna chahiye
4. Test query: "What is ROS2?" type karo
5. Verify answer mil raha hai with sources

#### 3.3: Check Logs (If Issues)

1. "Logs" tab par jao
2. Errors check karo:
   - `COHERE_API_KEY not found` → Secret set nahi hua
   - `Database not found` → Database commit nahi hui
   - `Timeout` → Database too large, pre-build issue

---

## 📋 Quick Command Reference

```bash
# Local setup
python setup_db.py --docs-dir ./docs

# Check database exists
dir chroma_db  # Windows
ls -la chroma_db/  # Linux/Mac

# Git operations
git status  # Check what's staged
git add chroma_db/
git commit -m "Add pre-built database"
git push -u origin master:main

# Verify secrets (in HF Space)
# Settings → Repository secrets → COHERE_API_KEY should exist
```

---

## 🔍 Troubleshooting

### Issue: "COHERE_API_KEY not found"

**Solution:**
1. Space Settings → Repository secrets
2. Verify `COHERE_API_KEY` exists
3. Name exactly `COHERE_API_KEY` hai (case-sensitive)
4. Space restart karo after adding secret

### Issue: "Database not found" or Empty Database

**Solution:**
1. Locally verify: `dir chroma_db` - files hone chahiye
2. Check `.gitignore` - `chroma_db/` comment out karo
3. Re-commit: `git add chroma_db/` → `git commit` → `git push`
4. Space rebuild karo

### Issue: Build Timeout

**Cause:** Runtime database creation trying (too slow)

**Solution:**
- Pre-build database locally
- Commit database files
- App directly load karegi pre-built database

### Issue: Disk Space Full

**If database too large:**
1. Check database size: `du -sh chroma_db` (Linux/Mac) or check folder size (Windows)
2. If > 100MB:
   - Consider Git LFS: `git lfs track "chroma_db/**"`
   - Or reduce document count
   - Or use external database (future migration)

---

## ✅ Final Checklist

### Pre-Deployment
- [ ] `.env` file mein `COHERE_API_KEY` set ki
- [ ] `python setup_db.py` successfully run kiya
- [ ] `chroma_db/` folder mein files verify ki
- [ ] `.gitignore` se `chroma_db/` temporarily removed/commented
- [ ] `git add chroma_db/` kiya
- [ ] `git commit` kiya
- [ ] `git push` kiya

### Hugging Face Space
- [ ] Space created: https://huggingface.co/spaces/faiza-faisal/Physical-Ai-Humanoid-Textbook
- [ ] Repository secret added: `COHERE_API_KEY`
- [ ] Code pushed (with database files)
- [ ] Build successful (Logs tab check kiya)
- [ ] App running (App tab check kiya)

### Testing
- [ ] System Info mein "Cohere API Key: ✅" dikh raha hai
- [ ] Test query successfully answered
- [ ] Source documents properly showing
- [ ] No errors in logs

---

## 📚 Additional Resources

- **Detailed Guide**: See `HF_SPACE_DEPLOYMENT.md` for complete documentation
- **Cohere API**: https://dashboard.cohere.com/
- **HF Spaces Docs**: https://huggingface.co/docs/hub/spaces-overview
- **Secrets Guide**: https://huggingface.co/docs/hub/spaces-overview#managing-secrets

---

**Current Setup:**
- ✅ Cohere API (not OpenAI)
- ✅ ChromaDB local storage (not Qdrant)
- ✅ Pre-built database commit approach

**Future Options (if needed):**
- External database (Qdrant Cloud, Pinecone) for large datasets
- Git LFS for large files
- Alternative embedding models


