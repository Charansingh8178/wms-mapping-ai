# 🏬 Warehouse Management System (WMS) MVP

This project is a **Warehouse Management MVP** built as part of the CSTE International assignment. It streamlines SKU-to-MSKU mapping from sales data, handles combo SKUs, syncs mapped data to Airtable, and provides a no-code dashboard to filter insights and run AI-powered queries on top of the warehouse data.


## Features

- 📁 Upload sales data and SKU/MSKU/Combo mapping files via Streamlit UI.
- 🔁 Automatically map sales SKUs to master SKUs using uploaded CSVs.
- 🎯 Detect and mark unmapped SKUs and combo SKUs.
- 🔄 Sync mapped output directly to Airtable.
- 📊 Visual dashboard using Airtable Interface Designer.
- 🤖 AI-powered natural language querying over inventory and mapped output (via OpenAI).

---
## 🔧 Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: Pandas, custom logic (SKU mapper)
- **Database**: Airtable (with relational links)
- **AI Layer**: OpenAI (ChatGPT API)
- **Dev Tools**: Python, dotenv, pyairtable, streamlit

---
## 🔁 What It Does

1. Uploads **sales data**, **SKU → MSKU mapping**, and **Combo SKU breakdowns**.
2. Maps each SKU to an MSKU using:
   - Direct match
   - Combo SKU decomposition
3. Outputs the mapped result with quantity, order ID, and mapping status.
4. Uploads results to **Airtable** (Mapped Output table).
5. Airtable **dashboard** shows:
   - Filters by mapped/unmapped SKUs
   - Visual summary via chart
6. AI Assistant accepts **natural language queries** (e.g., "Which SKUs were not mapped yesterday?") using OpenAI GPT.

---

## 🧠 AI Tools Used

- **OpenAI API** for AI-powered natural language to SQL/Airtable filtering
- Custom Python logic to pre-parse Airtable records into GPT-readable format

---

## ▶️ How to Use

Add the API keys in your .env file :
1. Airtable API Key :-  https://airtable.com/create/tokens
2. OpenAI API Key:-  https://platform.openai.com/account/api-keys
3. Base ID of Airtable:
      1. Go to your Airtable base
      2. Click the "Help" icon (question mark) at top right → "API documentation"
      3. It will take you to a link like:

4. **Run the app**
   ```bash'''
   streamlit run app.py
