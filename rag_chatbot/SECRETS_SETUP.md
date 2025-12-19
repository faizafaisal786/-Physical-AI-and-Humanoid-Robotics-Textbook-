# 🔐 Secrets Setup Guide - Hugging Face Space

## Required Secret: COHERE_API_KEY Only

### ❌ Important Clarification

**Current code uses:**
- ✅ **Cohere API** (for LLM and embeddings)
- ✅ **ChromaDB** (local file-based storage)

**Current code does NOT use:**
- ❌ OpenAI API
- ❌ Qdrant API
- ❌ Neon DB

---

## ✅ Step-by-Step Setup

### Step 1: Get Cohere API Key

1. Go to Cohere website: https://cohere.com/
2. Sign up / Login
3. Navigate to Dashboard: https://dashboard.cohere.com/
4. Go to API Keys section: https://dashboard.cohere.com/api-keys
5. Click "Create API Key" or use existing key
6. Copy the API key (keep it secure!)

### Step 2: Add Secret to Hugging Face Space

1. **Go to Space Settings:**
   - Navigate to: https://huggingface.co/spaces/faiza-faisal/Physical-Ai-Humanoid-Textbook/settings
   - Or: Space page → "Settings" tab

2. **Find Repository Secrets Section:**
   - Scroll down on Settings page
   - Look for "Repository secrets" section

3. **Add New Secret:**
   - Click "New secret" or "Add secret" button
   - **Name field**: Type exactly: `COHERE_API_KEY`
     - ⚠️ Case-sensitive
     - ⚠️ Must match exactly (no spaces, correct spelling)
   - **Value field**: Paste your Cohere API key
   - Click "Add secret" or "Save"

4. **Verify:**
   - Secret should appear in the list
   - Name: `COHERE_API_KEY`
   - Status: Active/Visible

### Step 3: Restart Space (Important!)

After adding secret:
1. Go to Settings
2. Look for "Restart this Space" button/option
3. Click to restart
4. Wait for rebuild (2-5 minutes)

---

## ✅ Verification

### Method 1: Check in App

1. Go to Space → "App" tab
2. Wait for app to load
3. In sidebar, expand "ℹ️ System Info"
4. Look for: "Cohere API Key: ✅"
   - ✅ = Secret properly set
   - ❌ = Secret not found

### Method 2: Check Logs

1. Go to Space → "Logs" tab
2. Look for errors:
   - ❌ "COHERE_API_KEY not found" → Secret not set
   - ✅ No such error → Secret working

### Method 3: Test Functionality

1. Ask a test question: "What is ROS2?"
2. If answer appears → Secret working correctly
3. If error about API key → Secret not set properly

---

## ❌ Common Mistakes

### Mistake 1: Wrong Secret Name

**Wrong:**
- `cohere_api_key` (lowercase)
- `Cohere_Api_Key` (mixed case)
- `COHERE-API-KEY` (hyphens)
- `OPENAI_API_KEY` (wrong service)

**Correct:**
- `COHERE_API_KEY` (exactly this)

### Mistake 2: Forgot to Restart

- Secret add karne ke baad Space restart karna zaroori hai
- Restart ke bina secret load nahi hoga

### Mistake 3: Invalid API Key

- Ensure API key is valid and active
- Check Cohere dashboard to verify key status
- Make sure key has required permissions

### Mistake 4: Added to Wrong Space

- Verify you're adding secret to correct Space
- Check Space name: `faiza-faisal/Physical-Ai-Humanoid-Textbook`

---

## 📋 Summary Table

| Secret Name | Required | Service | Purpose |
|------------|----------|---------|---------|
| `COHERE_API_KEY` | ✅ Yes | Cohere | LLM responses + embeddings |

| Not Needed | Reason |
|------------|--------|
| `OPENAI_API_KEY` | Code uses Cohere, not OpenAI |
| `QDRANT_API_KEY` | Code uses ChromaDB (local), not Qdrant |
| `NEON_DB_*` | No Neon DB connection in code |

---

## 🔄 Future Migration (If Needed)

If you want to switch services in the future:

### Switch to OpenAI:
1. Update code to use OpenAI instead of Cohere
2. Add secret: `OPENAI_API_KEY`
3. Update `requirements.txt`

### Switch to Qdrant Cloud:
1. Update `vector_store.py` to use Qdrant
2. Add secrets: `QDRANT_API_KEY`, `QDRANT_URL`
3. Update `requirements.txt` with `qdrant-client`

**Current Setup**: Cohere + ChromaDB (no changes needed)

---

## 📞 Need Help?

**Issues with Secret:**
1. Verify secret name is exactly `COHERE_API_KEY`
2. Check Space was restarted after adding secret
3. Verify API key is valid in Cohere dashboard

**Issues with API:**
1. Check Cohere dashboard for API usage/quota
2. Verify API key has required permissions
3. Check Space logs for detailed error messages

**Resources:**
- Cohere Dashboard: https://dashboard.cohere.com/
- Cohere API Docs: https://docs.cohere.com/
- HF Spaces Secrets: https://huggingface.co/docs/hub/spaces-overview#managing-secrets


