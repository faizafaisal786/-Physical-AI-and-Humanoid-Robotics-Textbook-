# Hugging Face Space Deployment Guide - Complete Setup

## 🔑 Step 1: Environment Variables (Secrets) Setup

### Required Secret: COHERE_API_KEY Only

Aapke chatbot ko **sirf ek API key** ki zaroorat hai:

| Secret Name | Required | Description |
|------------|----------|-------------|
| `COHERE_API_KEY` | ✅ Yes | Cohere API key for LLM responses and embeddings |

**Note**: Current code mein:
- ❌ OpenAI nahi use hota (Cohere use hota hai)
- ❌ Qdrant nahi use hota (ChromaDB use hota hai, local storage)
- ❌ Neon DB nahi use hota

### Setup Steps:

1. **Hugging Face Space ke Settings mein jao:**
   - Space page: https://huggingface.co/spaces/faiza-faisal/Physical-Ai-Humanoid-Textbook
   - **Settings** tab par click karo

2. **Repository Secrets section:**
   - Settings page par scroll karo
   - **"Repository secrets"** section dhundho

3. **COHERE_API_KEY add karo:**
   - **"New secret"** / **"Add secret"** button par click karo
   - **Name**: `COHERE_API_KEY` (exactly yeh name)
   - **Value**: Apni Cohere API key paste karo
   - **"Add secret"** / **"Save"** button par click karo

4. **API Key kaise milegi:**
   - Cohere website: https://cohere.com/
   - Dashboard: https://dashboard.cohere.com/
   - API Keys section: https://dashboard.cohere.com/api-keys
   - Create API key → Copy karo

---

## 📦 Step 2: Data Initialization - IMPORTANT!

Hugging Face Spaces par `setup_db.py` script directly run nahi kar sakte kyunki:
- Disk space limited hai
- Build time limited hai
- Documents processing time-consuming hai

### Solution: Pre-build Database Locally & Commit

**Recommended Approach**: Database ko locally build karo aur Git mein commit karo.

#### Step 2.1: Locally Database Build Karo

```bash
# 1. Local machine par .env file mein API key set karo
# .env file mein add karo:
COHERE_API_KEY=your_actual_cohere_api_key

# 2. Database build karo
python setup_db.py --docs-dir ./docs

# 3. Verify karo
ls -la chroma_db/
# Ya Windows par:
dir chroma_db
```

#### Step 2.2: Database Files ko Git Mein Add Karo

**IMPORTANT**: `.gitignore` file check karo - agar `chroma_db/` ignore ho raha hai, to usko temporarily remove karo ya allow karo.

```bash
# Check .gitignore
cat .gitignore
# Ya Windows par:
type .gitignore

# Agar chroma_db/ ignore ho raha hai, to .gitignore se remove karo
# (temporary - deployment ke liye)
```

```bash
# Database files add karo
git add chroma_db/
git commit -m "Add pre-built vector database"
git push -u origin master:main
```

#### Step 2.3: app.py Update Karo

Current code mein agar database nahi milta to automatically setup try karta hai, lekin HF Spaces par yeh reliable nahi hai. Better approach:

```python
# app.py mein initialize_pipeline() function ko update karo
# Agar database nahi milta, to error show karo (setup locally message)
```

---

## 🔄 Alternative Solution: Runtime Database Creation (For Small Data)

Agar aapka data chota hai (< 50 documents), to runtime creation bhi work kar sakta hai:

### Option A: Modify app.py for HF Spaces

```python
@st.cache_resource
def initialize_pipeline():
    """Initialize RAG pipeline"""
    try:
        import os
        
        # Check if database exists
        if not os.path.exists("./chroma_db") or not os.listdir("./chroma_db"):
            st.warning("⚠️ Database not found. Creating it now (this may take a few minutes)...")
            
            # Only create if documents exist
            if os.path.exists("./docs") and os.listdir("./docs"):
                from setup_db import setup_database
                success = setup_database(docs_directory="./docs", force_rebuild=False)
                if not success:
                    st.error("Failed to create database. Please contact admin.")
                    return None, "Database creation failed"
            else:
                st.error("No documents found in ./docs directory")
                return None, "No documents available"
        
        # Initialize pipeline
        pipeline = RAGPipeline(
            model_name="command-r-plus-08-2024",
            temperature=0.7,
            max_tokens=500,
            retrieval_k=5
        )
        return pipeline, None
        
    except Exception as e:
        return None, str(e)
```

**Note**: Yeh approach sirf chote datasets ke liye recommended hai. Timeout issues ho sakte hain.

---

## 📁 Recommended File Structure for Deployment

```
rag_chatbot/
├── app.py                    # Main Streamlit app
├── setup_db.py              # Database setup (local use only)
├── rag_pipeline.py          # RAG pipeline
├── vector_store.py          # Vector store manager
├── ingest_documents.py      # Document processing
├── requirements.txt         # Python dependencies
├── README.md               # Space metadata
├── chroma_db/              # Pre-built database (COMMITTED)
│   ├── chroma.sqlite3
│   └── [collection folders]
└── docs/                   # Source documents
    ├── introduction_to_robotics.md
    ├── ros2_guide.md
    └── ai_ml_robotics.md
```

---

## ✅ Deployment Checklist

### Pre-Deployment (Local)

- [ ] `.env` file mein `COHERE_API_KEY` set ki
- [ ] `python setup_db.py` run karke database build kiya
- [ ] Database successfully build hui (chroma_db folder check kiya)
- [ ] `.gitignore` se `chroma_db/` temporarily remove kiya (agar ignore ho raha ho)
- [ ] `git add chroma_db/` kiya
- [ ] `git commit` kiya
- [ ] `git push` kiya

### Hugging Face Space Setup

- [ ] Space create kiya: https://huggingface.co/spaces/faiza-faisal/Physical-Ai-Humanoid-Textbook
- [ ] Repository secret add kiya: `COHERE_API_KEY`
- [ ] Code push kiya (with pre-built database)
- [ ] Space build successfully hui
- [ ] App tab mein app run ho rahi hai
- [ ] System Info section mein "Cohere API Key: ✅" dikh raha hai

### Testing

- [ ] App successfully start hui
- [ ] Database load hui (no errors in logs)
- [ ] Test query: "What is ROS2?" - answer mila
- [ ] Source documents properly show ho rahe hain

---

## 🚨 Troubleshooting

### Problem: Database Not Found Error

**Solution 1**: Pre-built database commit nahi hui
```bash
# Locally check
ls -la chroma_db/
# Files honi chahiye

# Git mein check
git ls-files chroma_db/
# Agar kuch nahi dikha, to add karo
git add chroma_db/
git commit -m "Add database"
git push
```

**Solution 2**: `.gitignore` mein chroma_db/ ignore ho raha hai
- `.gitignore` file open karo
- `chroma_db/` line ko comment out karo ya remove karo
- Phir add/commit/push karo

### Problem: COHERE_API_KEY Not Found

**Check karo:**
1. Space Settings → Repository secrets → `COHERE_API_KEY` exists hai
2. Secret name exactly `COHERE_API_KEY` hai (case-sensitive)
3. Space restart kiya after adding secret

### Problem: Build Timeout

**Causes:**
- Runtime database creation (too slow)
- Large documents processing

**Solution:**
- Pre-build database locally
- Commit database files
- App directly load karegi pre-built database

### Problem: Disk Space Full

**If database too large:**
- Consider using external database (Qdrant Cloud, Pinecone)
- Or compress database files
- Or reduce document count

---

## 📊 Size Recommendations

| Data Size | Approach | Notes |
|-----------|----------|-------|
| < 10 MB | Pre-build + Commit | ✅ Recommended |
| 10-50 MB | Pre-build + Commit | ✅ OK (Git LFS consider karo) |
| 50-100 MB | External DB (Qdrant Cloud) | Consider migration |
| > 100 MB | External DB Required | Must use external storage |

---

## 🔄 Migration to External Database (Future)

Agar data bada ho jaye, to Qdrant Cloud use kar sakte hain:

1. Qdrant Cloud account banao
2. Cluster create karo
3. New secret add karo: `QDRANT_API_KEY`, `QDRANT_URL`
4. `vector_store.py` update karo to use Qdrant instead of ChromaDB
5. Update `requirements.txt` with `qdrant-client`

**Current implementation**: ChromaDB (local storage)
**Future option**: Qdrant Cloud (if needed)

---

## 📝 Quick Reference Commands

```bash
# Local setup
python setup_db.py --docs-dir ./docs

# Check database
ls -la chroma_db/

# Add to git
git add chroma_db/
git commit -m "Add pre-built database"
git push -u origin master:main

# Verify secrets (in Space)
# Settings → Repository secrets → COHERE_API_KEY

# Check app logs (in Space)
# Logs tab → Check for errors
```

---

## ✅ Final Steps Summary

1. ✅ **Secret Add Karo**: `COHERE_API_KEY` in Space Settings
2. ✅ **Database Build Karo**: Locally run `setup_db.py`
3. ✅ **Database Commit Karo**: `chroma_db/` folder ko Git mein add karo
4. ✅ **Push Karo**: Code aur database ko Space mein push karo
5. ✅ **Verify Karo**: App successfully run ho rahi hai

---

**Important Notes:**
- Current code: **Cohere API + ChromaDB** use karta hai
- **OpenAI, Qdrant, Neon DB** currently use nahi hote
- Agar future mein change chahiye, to code update karna hoga


