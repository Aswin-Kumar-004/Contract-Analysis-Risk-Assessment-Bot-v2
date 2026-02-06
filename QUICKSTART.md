# Quick Start Guide

## Installation (5 minutes)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Step 1: Install Dependencies

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:**
```bash
install.bat
```

**Or manually:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 2: Set API Key

**Linux/Mac:**
```bash
export ANTHROPIC_API_KEY='your_api_key_here'
```

**Windows:**
```bash
set ANTHROPIC_API_KEY=your_api_key_here
```

**Or create a `.env` file:**
```
ANTHROPIC_API_KEY=your_api_key_here
```

### Step 3: Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## First Time Usage

### Analyze a Contract

1. Click **"Load Sample Vendor Agreement"** in the sidebar
2. Click **"🚀 Analyze Document"**
3. Wait 10-20 seconds for analysis
4. Explore the results:
   - Risk dashboard
   - Financial impact
   - Clause-by-clause breakdown
   - Comparative analysis

### Generate a Template

1. Navigate to **"📄 Template Generator"** tab
2. Select contract type (NDA, Employment, Service Agreement)
3. Fill in party names and dates
4. Click **"✨ Generate Template"**
5. Download the template

### Search Knowledge Base

1. Navigate to **"🤖 AI Clause Search (RAG)"** tab
2. Paste any clause from your contract
3. Click **"🔍 Search Knowledge Base"**
4. View similar standard clauses and their safety ratings

---

## Troubleshooting

### "API key not configured" error
- Make sure you set the `ANTHROPIC_API_KEY` environment variable
- Restart your terminal/command prompt after setting it
- Check that the key is valid at console.anthropic.com

### "spaCy model not found" error
```bash
python -m spacy download en_core_web_sm
```

### App won't start
- Check Python version: `python --version` (should be 3.8+)
- Update Streamlit: `pip install --upgrade streamlit`
- Check for port conflicts: Try `streamlit run app.py --server.port 8502`

### Import errors
```bash
pip install --upgrade -r requirements.txt
```

---

## Tips for Best Results

### Contract Upload
- **Supported formats:** PDF (text-based), DOCX, TXT
- **Best format:** Plain text with clear clause numbering
- **Avoid:** Scanned PDFs (OCR not supported yet), images

### Getting Good Analysis
- Upload complete contracts (not just excerpts)
- Contracts with clear section headers work best
- For best results, use contracts in English

### Understanding Results
- **High Risk** = Negotiate these clauses before signing
- **Medium Risk** = Review carefully, may need clarification
- **Low Risk** = Standard clauses, generally safe

---

## Demo Mode (Without API Key)

You can still use most features without an API key:
- ✅ Contract classification
- ✅ Entity extraction
- ✅ Keyword-based risk detection
- ✅ Knowledge base search
- ❌ AI summaries (requires API key)
- ❌ Detailed clause explanations (requires API key)
- ❌ Alternative clause suggestions (requires API key)

To get full functionality, sign up for an Anthropic API key (free tier available).

---

## Next Steps

1. **Try with your own contracts** - Upload a real contract to test
2. **Review the sample contract** - See all 8 risky clauses we catch
3. **Generate templates** - Create safe contracts for your business
4. **Read the full README** - Understand the architecture and capabilities

---

## Support

- **Issues:** File a GitHub issue
- **Email:** support@example.com
- **Documentation:** See README.md for detailed information

---

## License

MIT License - Free for personal and commercial use
