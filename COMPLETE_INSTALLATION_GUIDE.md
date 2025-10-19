# Wake Forest RAG Application - Complete Installation Guide

## 📥 Files You'll Need to Download

Download all these files from Claude and organize them as shown below:

### Main Files (put in project root):
1. `app.py` - Main application
2. `config.yaml` - Authentication config
3. `requirements.txt` - Dependencies
4. `.env.example` - Environment template
5. `.gitignore` - Git ignore rules
6. `Dockerfile` - Docker config
7. `docker-compose.yml` - Docker Compose config
8. `README.md` - Full documentation
9. `QUICKSTART.md` - Quick start guide
10. `DEPLOYMENT.md` - Deployment guide
11. `PROJECT_SUMMARY.md` - Project overview
12. `CHECKLIST.md` - Setup checklist
13. `generate_password.py` - Password utility
14. `verify_setup.py` - Setup checker

### Utils Files (create `utils/` folder and put these inside):
15. `utils___init__.py` → rename to `__init__.py`
16. `utils_drive_handler.py` → rename to `drive_handler.py`
17. `utils_supabase_store.py` → rename to `supabase_store.py`
18. `utils_rag_engine.py` → rename to `rag_engine.py`

### Assets (create `assets/` folder and put this inside):
19. `WFU_Univ_Shield_Black.png`

## 📁 Final Folder Structure

After organizing files, your project should look like this:

```
wfu-rag-app/
├── app.py
├── config.yaml
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
├── QUICKSTART.md
├── DEPLOYMENT.md
├── PROJECT_SUMMARY.md
├── CHECKLIST.md
├── generate_password.py
├── verify_setup.py
├── .env                          # You'll create this
├── service-account.json          # You'll get this from Google
├── assets/
│   └── WFU_Univ_Shield_Black.png
└── utils/
    ├── __init__.py
    ├── drive_handler.py
    ├── supabase_store.py
    └── rag_engine.py
```

## 🚀 Quick Start (After Downloading Files)

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your API Keys

You'll need accounts and API keys from:

**Anthropic (for Claude):**
- Go to: https://console.anthropic.com/
- Create account → API Keys → Create Key
- Copy the key (starts with `sk-ant-`)

**OpenAI (for embeddings):**
- Go to: https://platform.openai.com/
- Create account → API Keys → Create Secret Key
- Copy the key (starts with `sk-`)

**Supabase (for database):**
1. Go to: https://supabase.com/
2. Create new project (free tier is fine)
3. Wait ~2 minutes for initialization
4. Go to Settings → API
5. Copy your Project URL (e.g., `https://xxxxx.supabase.co`)
6. Copy your `service_role` secret key
7. **Important:** Run this SQL in SQL Editor:

```sql
-- Enable pgvector extension
create extension if not exists vector;

-- Create documents table
create table documents (
  id text primary key,
  content text not null,
  embedding vector(1536),
  file_id text not null,
  file_name text not null,
  file_url text,
  chunk_id integer not null,
  mime_type text,
  modified_time text,
  created_at timestamp with time zone default timezone('utc'::text, now())
);

-- Create index for vector similarity search
create index on documents using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

-- Create function for vector similarity search
create or replace function match_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int
)
returns table (
  id text,
  content text,
  file_id text,
  file_name text,
  file_url text,
  chunk_id integer,
  mime_type text,
  modified_time text,
  similarity float
)
language sql stable
as $$
  select
    id,
    content,
    file_id,
    file_name,
    file_url,
    chunk_id,
    mime_type,
    modified_time,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where 1 - (documents.embedding <=> query_embedding) > match_threshold
  order by documents.embedding <=> query_embedding
  limit match_count;
$$;
```

**Google Drive (service account):**
1. Go to: https://console.cloud.google.com/
2. Create new project (or select existing)
3. Enable "Google Drive API"
4. Go to: IAM & Admin → Service Accounts
5. Create Service Account
6. Download JSON key file
7. Rename to `service-account.json`
8. Place in project root folder
9. **Share your Google Drive folder with the service account email** (found in JSON file)
10. Copy your folder ID from the Drive URL

### 3. Create .env File

```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxxxx
GOOGLE_SERVICE_ACCOUNT_FILE=./service-account.json
```

### 4. Verify Setup

```bash
python verify_setup.py
```

This will check if everything is configured correctly.

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 6. Login and Test

**Default credentials:**
- Username: `admin`
- Password: `wfu_admin_2025`

**⚠️ IMMEDIATELY change this password:**
```bash
python generate_password.py
# Follow prompts to generate new hash
# Update config.yaml with new hash
```

### 7. Index Your Documents

1. In the sidebar, click "Index Documents"
2. Enter your Google Drive folder ID
3. Click "Index Documents"
4. Wait for processing
5. Start asking questions!

## 🔧 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Service account file not found"
- Make sure `service-account.json` is in the project root
- Check the path in `.env` is `./service-account.json`

### "Permission denied" on Google Drive
- Share your Drive folder with the service account email
- Give it "Viewer" access
- Email is in the service-account.json file

### "Supabase connection error"
- Verify URL and key in `.env`
- Make sure you ran the SQL setup script
- Check your Supabase project is active

### Can't login
- Default is `admin` / `wfu_admin_2025`
- Check `config.yaml` for user configuration

## 💰 Cost Estimate

**Free tier (testing):**
- Supabase: Free (500MB)
- Anthropic: ~$10-20/month (pay-as-you-go)
- OpenAI: ~$1-5/month (one-time indexing)
- **Total: ~$10-25/month**

**Production:**
- Supabase Pro: $25/month
- Anthropic: $30-50/month (based on usage)
- OpenAI: $5-10/month (updates)
- **Total: ~$60-85/month**

## 🌐 Deployment Options

### Streamlit Cloud (Easiest)
1. Push code to GitHub
2. Go to streamlit.io/cloud
3. Connect GitHub repo
4. Add environment variables
5. Deploy!

### Docker (VPS hosting)
```bash
docker-compose up -d
```

### See DEPLOYMENT.md for full deployment guides

## 📚 Documentation

- **README.md** - Comprehensive guide
- **QUICKSTART.md** - Fast setup
- **DEPLOYMENT.md** - Hosting options
- **CHECKLIST.md** - Step-by-step verification
- **PROJECT_SUMMARY.md** - Overview

## 🔒 Security Checklist

- [ ] Changed default password
- [ ] Updated cookie key in config.yaml
- [ ] .env not committed to git
- [ ] service-account.json not committed to git
- [ ] Using HTTPS in production

## 🎯 What This App Does

1. **Connects to Google Drive** - Scans folders recursively
2. **Extracts text** - From PDFs, DOCX, XLSX, TXT, Google Docs, Sheets
3. **Creates embeddings** - Using OpenAI for semantic search
4. **Stores in Supabase** - Secure vector database
5. **Answers questions** - Using Claude AI with source citations

## 📞 Support

If you get stuck:
1. Run `python verify_setup.py`
2. Check the troubleshooting section above
3. Review README.md for detailed help
4. Verify all API keys are correct

## ✅ Quick Verification

After setup, test these:
- [ ] App starts without errors
- [ ] Can login
- [ ] Can index documents
- [ ] Can ask questions
- [ ] Get responses with citations

## 🎓 Wake Forest Branding

The app includes:
- Old Gold (#9E7E38) and Black color scheme
- Official WFU shield logo
- Professional, academic design
- "Pro Humanitate" spirit

---

**You're all set!** Follow the steps above and you'll have a working RAG application in 15-20 minutes.

For detailed documentation, see README.md after downloading all files.
