# Wake Forest Document Assistant

A secure, branded RAG (Retrieval Augmented Generation) application for querying Google Drive documents using AI. Built with Streamlit, Claude AI, and Supabase.

![Wake Forest University](assets/WFU_Univ_Shield_Black.png)

## Features

- 🔒 **Secure Authentication** - Password-protected with bcrypt hashing
- 🎨 **Wake Forest Branding** - Official colors and logo
- 📚 **Multi-Format Support** - PDFs, DOCX, XLSX, TXT, Google Docs, Sheets, and more
- 🔍 **Semantic Search** - Vector-based search using OpenAI embeddings
- 🤖 **Claude AI** - Intelligent responses powered by Claude Sonnet 4
- 📂 **Recursive Scanning** - Automatically processes nested folders
- 💾 **Supabase Storage** - Secure, scalable vector database
- 📱 **Responsive UI** - Clean, professional interface

## Security Features

✅ **Password Protection** - Streamlit Authenticator with bcrypt hashing  
✅ **Environment Variables** - No credentials in code  
✅ **Service Account** - Controlled Google Drive access  
✅ **Encrypted Data** - Supabase TLS/SSL encryption  
✅ **Row Level Security** - Isolated database access  
✅ **Session Management** - Secure logout capability  

**Your data never leaves your control** - Everything stays in your Supabase instance and Google Drive.

## Prerequisites

Before setting up, you'll need:

1. **Python 3.9+** installed
2. **Google Cloud Service Account** with Drive API access
3. **Supabase Account** (free tier works)
4. **Anthropic API Key** (for Claude)
5. **OpenAI API Key** (for embeddings)

## Installation

### 1. Clone or Download This Repository

```bash
# If using git
git clone <your-repo-url>
cd wfu-rag-app

# Or simply extract the ZIP file
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Google Drive Setup

#### Create Service Account:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Drive API**
4. Go to **IAM & Admin** → **Service Accounts**
5. Click **Create Service Account**
6. Give it a name (e.g., "WFU RAG App")
7. Click **Create and Continue**
8. Grant role: **Basic** → **Viewer** (or custom role with Drive read access)
9. Click **Done**
10. Click on the service account you just created
11. Go to **Keys** tab
12. Click **Add Key** → **Create New Key**
13. Choose **JSON** format
14. Download the JSON file
15. Rename it to `service-account.json` and place it in the project root

#### Share Your Google Drive Folder:

1. Open the Google Drive folder you want to index
2. Click **Share**
3. Add the service account email (found in the JSON file, looks like: `xxx@xxx.iam.gserviceaccount.com`)
4. Give it **Viewer** access
5. Copy the folder ID from the URL (it's the string after `/folders/`)

### 2. Supabase Setup

#### Create Project:

1. Go to [Supabase](https://supabase.com/)
2. Create a new project (free tier is fine)
3. Wait for it to initialize (~2 minutes)

#### Enable pgvector:

1. Go to **SQL Editor** in your Supabase dashboard
2. Run this SQL to enable pgvector:

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

#### Get API Keys:

1. Go to **Settings** → **API**
2. Copy your **Project URL** (looks like: `https://xxxxx.supabase.co`)
3. Copy your **service_role secret** key (under "Project API keys")

### 3. API Keys

#### Anthropic (Claude):

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Go to **API Keys**
4. Create a new key
5. Copy it (you won't see it again!)

#### OpenAI:

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to **API Keys**
4. Create a new secret key
5. Copy it

### 4. Environment Variables

1. Copy the example file:

```bash
cp .env.example .env
```

2. Edit `.env` and fill in your values:

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxxxx
GOOGLE_SERVICE_ACCOUNT_FILE=./service-account.json
```

### 5. Authentication Setup

The default credentials are:
- **Username:** `admin`
- **Password:** `wfu_admin_2025`

**⚠️ IMPORTANT: Change this password immediately!**

To change the password:

1. Install bcrypt:
```bash
pip install bcrypt
```

2. Generate a new password hash:
```python
import bcrypt
password = "your_new_secure_password"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))
```

3. Edit `config.yaml` and replace the password hash

4. Also change the `cookie.key` to a random string for security

## Running the Application

### Local Development

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### First Time Use

1. Log in with username: `admin` and password: `wfu_admin_2025`
2. **Change your password** (see Authentication Setup above)
3. Click **Index Documents** in the sidebar
4. Enter your Google Drive folder ID
5. Click **Index Documents** and wait for processing
6. Start asking questions!

## Deployment

### Option 1: Streamlit Cloud (Easiest)

1. Push your code to GitHub (make sure `.env` and `service-account.json` are NOT committed!)
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click **New app**
4. Select your repository
5. Set main file: `app.py`
6. Click **Advanced settings**
7. Add all your environment variables from `.env`
8. For the service account, paste the JSON content into `GOOGLE_SERVICE_ACCOUNT_FILE`
9. Deploy!

**For private deployment:**
- Use Streamlit Cloud's private app feature (requires paid plan)
- Or restrict access via the authentication system

### Option 2: Docker (Self-Hosted)

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t wfu-rag-app .
docker run -p 8501:8501 --env-file .env wfu-rag-app
```

### Option 3: Traditional Hosting

Deploy to any VPS (AWS EC2, DigitalOcean, etc.):

```bash
# Install dependencies
pip install -r requirements.txt

# Run with nohup for background execution
nohup streamlit run app.py --server.port 8501 &

# Or use systemd service for production
```

## Usage Guide

### Indexing Documents

1. **Obtain Folder ID**: 
   - Open your Google Drive folder
   - Copy the ID from URL: `https://drive.google.com/drive/folders/YOUR_FOLDER_ID`

2. **Index**:
   - Click "Index Documents" in sidebar
   - Paste folder ID
   - Click "Index Documents"
   - Wait for processing (progress bar shows status)

3. **What Gets Indexed**:
   - All files in the folder
   - All files in nested subfolders (recursive)
   - Supported types: PDF, DOCX, XLSX, CSV, TXT, Google Docs, Sheets, Slides

### Querying Documents

Simply type your question in the chat interface. Examples:

- "What are the key findings in the Q3 report?"
- "Summarize the project timeline from the planning docs"
- "What budget was allocated for marketing?"
- "Find information about the new hiring policy"

The system will:
1. Search relevant documents using semantic similarity
2. Generate a response using Claude AI
3. Cite source documents
4. Show clickable links to original files

### Tips for Best Results

- ✅ Be specific in your questions
- ✅ Ask one question at a time
- ✅ Include context if the question is ambiguous
- ✅ Check the sources to verify information
- ❌ Don't ask questions unrelated to your documents
- ❌ Don't expect the AI to know information not in your files

## Cost Estimates

### Free Tier (Testing/Small Scale)
- **Supabase**: Free (500MB database)
- **Anthropic Claude**: Pay-as-you-go (~$0.01-0.03/query)
- **OpenAI Embeddings**: ~$0.10 per 1M tokens (one-time indexing)
- **Google Cloud**: Free (Drive API calls)
- **Streamlit Cloud**: Free (public apps)

**Estimated**: $10-30/month for moderate usage

### Production Scale
- **Supabase Pro**: $25/month
- **Anthropic**: Based on usage
- **OpenAI**: Based on usage
- **Streamlit Cloud Private**: $20+/month

**Estimated**: $50-100/month for heavy usage

## Troubleshooting

### "Service account file not found"
- Ensure `service-account.json` is in the project root
- Check the path in `.env` file

### "Permission denied" on Google Drive
- Make sure you shared the folder with the service account email
- The service account needs at least Viewer access

### "Supabase connection error"
- Verify your `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`
- Check if you ran the SQL setup scripts

### "No relevant documents found"
- Make sure documents are indexed (check sidebar status)
- Try rephrasing your question
- Verify files were successfully processed during indexing

### Indexing fails or skips files
- Check file permissions in Google Drive
- Some file types may not be supported
- Large files may timeout (increase processing if needed)

## Security Best Practices

1. **Change default password immediately**
2. **Use strong, unique passwords**
3. **Keep `.env` and `service-account.json` private**
4. **Never commit secrets to version control**
5. **Use environment-specific configs for production**
6. **Regularly rotate API keys**
7. **Enable Supabase Row Level Security policies**
8. **Use HTTPS in production**
9. **Limit service account permissions**
10. **Monitor API usage for anomalies**

## Updating Documents

To refresh your document index:
1. Click "Index Documents" again
2. Enter the same folder ID
3. New/modified files will be reprocessed
4. Old documents are automatically updated

## Customization

### Branding

Edit `app.py` to customize:
- Colors (search for `--wfu-gold` and `--wfu-black`)
- Logo (replace file in `assets/`)
- Title and headers
- Footer text

### RAG Parameters

Edit `utils/rag_engine.py`:
- `top_k`: Number of documents to retrieve (default: 5)
- `max_tokens`: Claude response length (default: 4096)

Edit `utils/supabase_store.py`:
- `chunk_size`: Document chunk size (default: 1000)
- `chunk_overlap`: Overlap between chunks (default: 200)

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review logs: `streamlit run app.py --server.enableXsrfProtection false`
3. Verify all API keys are valid
4. Check Supabase logs in dashboard

## License

This application is built for Wake Forest University. Modify and use according to your institutional policies.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Claude AI](https://www.anthropic.com/)
- Vector storage by [Supabase](https://supabase.com/)
- Embeddings by [OpenAI](https://openai.com/)

---

**Wake Forest University** | Pro Humanitate
