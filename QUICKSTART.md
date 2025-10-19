# Quick Start Guide

## 🚀 Get Started in 5 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Setup Supabase Database
- Create a Supabase project at https://supabase.com
- Run the SQL script from README.md in your SQL Editor
- Copy your URL and service key to .env

### 4. Setup Google Drive Access
- Create a service account in Google Cloud Console
- Download the JSON file as `service-account.json`
- Share your Drive folder with the service account email
- Copy the folder ID from the Drive URL

### 5. Run the App
```bash
streamlit run app.py
```

## Default Login
- Username: `admin`
- Password: `wfu_admin_2025`

**⚠️ Change this immediately after first login!**

Run: `python generate_password.py` to create a new password hash.

## Next Steps

1. Log in to the app
2. Generate a new password (see above)
3. Update config.yaml with new password hash
4. Index your documents
5. Start asking questions!

## Need Help?

See the full README.md for detailed instructions and troubleshooting.

## File Checklist

Before running, make sure you have:
- [ ] `.env` file with all API keys
- [ ] `service-account.json` from Google Cloud
- [ ] Supabase database created and configured
- [ ] Changed default password in `config.yaml`

## Folder Structure
```
wfu-rag-app/
├── app.py                      # Main Streamlit application
├── config.yaml                 # Authentication configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create from .env.example)
├── service-account.json        # Google service account (you provide)
├── generate_password.py        # Password hash generator utility
├── assets/
│   └── WFU_Univ_Shield_Black.png
├── utils/
│   ├── __init__.py
│   ├── drive_handler.py        # Google Drive integration
│   ├── supabase_store.py       # Vector storage
│   └── rag_engine.py           # RAG query engine
├── README.md                   # Full documentation
└── QUICKSTART.md              # This file
```

## Common Issues

**"Service account file not found"**
- Make sure `service-account.json` is in the root directory

**"Permission denied" on Google Drive**
- Share your folder with the service account email

**"Supabase connection error"**
- Check your URL and service key in .env
- Make sure you ran the SQL setup

**Login doesn't work**
- Default is username: `admin`, password: `wfu_admin_2025`
- Check config.yaml for user configuration

## Support

For detailed setup instructions, see README.md
For API documentation:
- Anthropic: https://docs.anthropic.com
- OpenAI: https://platform.openai.com/docs
- Supabase: https://supabase.com/docs
- Google Drive API: https://developers.google.com/drive
