# Physical AI & Humanoid Robotics Textbook - Quick Start Guide

## 🚀 Ab Root Directory Se Direct Start Karein!

### Option 1: Sirf Frontend (Textbook)

```bash
npm run start
```

Ye command automatically:
- `docusaurus_textbook` folder mein jayega
- Development server start karega
- Textbook http://localhost:3000 par open hogi

### Option 2: Frontend + Backend Dono Saath Mein

```bash
npm run dev
```

Ye command simultaneously chalayega:
- Frontend (Docusaurus) - http://localhost:3000
- Backend (FastAPI) - http://localhost:8000

### Available Commands:

| Command | Kya Karta Hai |
|---------|--------------|
| `npm run start` | Frontend (textbook) start karta hai |
| `npm run build` | Production build banata hai |
| `npm run serve` | Built site serve karta hai |
| `npm run backend` | Sirf backend API start karta hai |
| `npm run dev` | Frontend + Backend dono start karta hai |
| `npm run install-frontend` | Frontend dependencies install karta hai |
| `npm run install-backend` | Backend dependencies install karta hai |
| `npm run setup` | Sab kuch install karta hai (first time) |

## 📋 First Time Setup:

Agar aap pehli baar project run kar rahe hain:

```bash
# Step 1: Sab dependencies install karein
npm run setup

# Step 2: Backend ke liye .env file banayein
cd backend
copy .env.example .env
# .env file mein apni API keys daalein

# Step 3: Database initialize karein
python init_db.py

# Step 4: Project start karein
cd ..
npm run start
```

## 🎯 Ab Kya Karen:

1. Terminal mein jayen project root directory mein
2. Likhein: `npm run start`
3. Browser mein jayen: http://localhost:3000
4. Enjoy! 🎉

## 🌟 Features:

- ✅ Root se direct `npm run start`
- ✅ Automatic navigation to docusaurus folder
- ✅ Frontend + Backend ek saath chalane ka option
- ✅ Easy setup commands
- ✅ Production build support

## 📝 Example Usage:

```bash
# Terminal mein
cd "C:\Users\HDD BANK\Desktop\all-work\-Physical-AI-and-Humanoid-Robotics-Textbook-"

# Simple start
npm run start

# Ya dono saath mein
npm run dev
```

That's it! Ab aap root directory se hi sab kuch control kar sakte hain! 🚀
