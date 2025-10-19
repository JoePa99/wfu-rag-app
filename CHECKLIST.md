# Setup Checklist ✓

Use this checklist to ensure everything is properly configured before running the app.

## 📋 Pre-Setup Requirements

### API Keys & Accounts
- [ ] Anthropic account created
- [ ] Anthropic API key obtained
- [ ] OpenAI account created
- [ ] OpenAI API key obtained
- [ ] Supabase account created
- [ ] Supabase project created
- [ ] Google Cloud project created

## 🔧 Step-by-Step Setup

### Phase 1: Google Drive Access
- [ ] Created Google Cloud project
- [ ] Enabled Google Drive API
- [ ] Created service account
- [ ] Downloaded service account JSON file
- [ ] Renamed to `service-account.json`
- [ ] Placed in project root directory
- [ ] Shared Google Drive folder with service account email
- [ ] Copied folder ID from Drive URL

### Phase 2: Supabase Configuration
- [ ] Created Supabase project
- [ ] Waited for initialization (~2 minutes)
- [ ] Opened SQL Editor
- [ ] Ran the SQL script (from README.md) to:
  - [ ] Enable pgvector extension
  - [ ] Create documents table
  - [ ] Create vector index
  - [ ] Create match_documents function
- [ ] Copied Project URL
- [ ] Copied service_role secret key

### Phase 3: Environment Setup
- [ ] Installed Python 3.9+
- [ ] Created virtual environment: `python -m venv venv`
- [ ] Activated virtual environment
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Copied `.env.example` to `.env`
- [ ] Filled in all values in `.env`:
  - [ ] ANTHROPIC_API_KEY
  - [ ] OPENAI_API_KEY
  - [ ] SUPABASE_URL
  - [ ] SUPABASE_SERVICE_KEY
  - [ ] GOOGLE_SERVICE_ACCOUNT_FILE

### Phase 4: Security Configuration
- [ ] Ran `python generate_password.py`
- [ ] Generated new password hash
- [ ] Updated `config.yaml` with new password
- [ ] Changed cookie key in `config.yaml`
- [ ] Verified `.gitignore` includes sensitive files

### Phase 5: Verification
- [ ] Ran `python verify_setup.py`
- [ ] All checks passed ✅
- [ ] Logo file present in assets/
- [ ] All required files present

## 🚀 First Run

### Starting the Application
- [ ] Opened terminal in project directory
- [ ] Activated virtual environment
- [ ] Ran `streamlit run app.py`
- [ ] App opened in browser
- [ ] No error messages

### First Login
- [ ] Logged in with admin/wfu_admin_2025
- [ ] Login successful
- [ ] App interface loaded correctly
- [ ] Wake Forest logo displayed
- [ ] Branding looks correct

### Indexing Test
- [ ] Clicked "Index Documents" in sidebar
- [ ] Entered Google Drive folder ID
- [ ] Clicked "Index Documents"
- [ ] Progress bar appeared
- [ ] Files were processed
- [ ] Success message appeared
- [ ] Status changed to "Documents Indexed"

### Query Test
- [ ] Typed test question in chat
- [ ] Response generated
- [ ] Sources shown
- [ ] Links to files work
- [ ] Citations accurate

## 🔒 Security Checklist

### Post-Setup Security
- [ ] Changed default admin password
- [ ] Updated cookie key
- [ ] Verified .env not in git
- [ ] Verified service-account.json not in git
- [ ] Tested logout functionality
- [ ] Confirmed session persistence works

## 📦 Deployment Checklist

### Before Deploying
- [ ] Tested locally completely
- [ ] All features working
- [ ] No console errors
- [ ] Performance acceptable
- [ ] Read DEPLOYMENT.md
- [ ] Chosen deployment method
- [ ] Prepared deployment credentials

### After Deploying
- [ ] Application accessible at URL
- [ ] HTTPS enabled (if public)
- [ ] Login works
- [ ] Can index documents
- [ ] Can query documents
- [ ] Performance acceptable
- [ ] Monitoring setup
- [ ] Backup strategy in place

## 📊 Testing Scenarios

### Functional Tests
- [ ] Login with correct credentials works
- [ ] Login with wrong credentials fails appropriately
- [ ] Logout works
- [ ] Can index small folder (< 10 files)
- [ ] Can index large folder (> 50 files)
- [ ] Can query indexed documents
- [ ] Sources link back to correct files
- [ ] Can clear conversation
- [ ] Can re-index after adding files

### File Type Tests
- [ ] PDF files indexed correctly
- [ ] DOCX files indexed correctly
- [ ] XLSX files indexed correctly
- [ ] TXT files indexed correctly
- [ ] CSV files indexed correctly
- [ ] Google Docs indexed correctly
- [ ] Google Sheets indexed correctly

### Error Handling Tests
- [ ] Invalid folder ID handled gracefully
- [ ] Network errors handled
- [ ] Invalid API key error messages clear
- [ ] Empty folder handled correctly
- [ ] Unsupported file types skipped appropriately

## 💡 Troubleshooting Guide

### If Something Doesn't Work:

1. **Run verification script:**
   ```bash
   python verify_setup.py
   ```

2. **Check logs:**
   - Look at terminal output
   - Check for error messages
   - Verify all imports work

3. **Verify credentials:**
   - All API keys valid
   - Service account has permissions
   - Folder shared correctly

4. **Review documentation:**
   - README.md for detailed setup
   - QUICKSTART.md for fast reference
   - DEPLOYMENT.md for hosting options

## ✅ Final Verification

Before considering setup complete:

- [ ] Everything above checked off
- [ ] Application runs without errors
- [ ] Can successfully index documents
- [ ] Can successfully query documents
- [ ] Security measures in place
- [ ] Ready for production use

---

## 🎉 You're Ready!

Once all items are checked, your Wake Forest RAG application is ready to use!

### Next Steps:
1. Index your production document folder
2. Share with intended users
3. Monitor usage and performance
4. Provide feedback for improvements

### Support:
- See README.md for comprehensive documentation
- Check DEPLOYMENT.md for hosting options
- Use verify_setup.py for troubleshooting

**Pro Humanitate** 🎓
