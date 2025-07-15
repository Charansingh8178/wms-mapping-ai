import streamlit as st
import pandas as pd
from sku_mapper import SKUMappingEngine
from pyairtable import Api
from dotenv import load_dotenv
import os
from openai import OpenAI
import openai
# --- Load environment variables ---
load_dotenv()
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TABLE_NAME = "Mapped Output"
SKU_TABLE_NAME = "SKU Mapping"

# --- Airtable client ---
api = Api(AIRTABLE_API_KEY)
mapped_output_table = api.table(AIRTABLE_BASE_ID, TABLE_NAME)
sku_table = api.table(AIRTABLE_BASE_ID, SKU_TABLE_NAME)

# --- OpenAI client ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Streamlit UI ---
st.title("📦 Warehouse Sales Mapper & AI Dashboard")

# Upload CSVs
sales_file = st.file_uploader("📄 Upload Sales CSV", type=["csv"])
sku_to_msku_file = st.file_uploader("🔁 Upload SKU → MSKU Mapping", type=["csv"])
combo_file = st.file_uploader("🧃 Upload Combo SKU Mapping", type=["csv"])

if sales_file and sku_to_msku_file and combo_file:
    # Load data
    sales_df = pd.read_csv(sales_file)
    sku_df = pd.read_csv(sku_to_msku_file)
    combo_df = pd.read_csv(combo_file)

    sku_df.to_csv("temp_sku.csv", index=False)
    combo_df.to_csv("temp_combo.csv", index=False)

    # Mapping engine
    engine = SKUMappingEngine("temp_sku.csv", "temp_combo.csv")
    mapped_df = engine.map_sales_data(sales_df)

    st.subheader("🧾 Mapped Output")
    st.dataframe(mapped_df)
    mapped_df.to_csv("mapped_output.csv", index=False)

    # Upload to Airtable
    if st.button("🔄 Upload to Airtable"):
        with st.spinner("Uploading to Airtable..."):
            success = 0
            for _, row in mapped_df.iterrows():
                msku = str(row.get("MSKU", "")).strip()
                linked_id = None

                if msku:
                    search_results = sku_table.all(formula=f"{{msku}} = '{msku}'")
                    if search_results:
                        linked_id = search_results[0]['id']

                try:
                    mapped_output_table.create({
                        "OrderID": str(row.get("OrderID", "")),
                        "SKU": str(row.get("SKU", "")),
                        "MSKU": [linked_id] if linked_id else [],
                        "Mapped_Qty": int(row.get("Mapped_Qty", 0)),
                        "Status": str(row.get("Status", ""))
                    })
                    success += 1
                except Exception as e:
                    st.error(f"❌ Error uploading: {e}")
            st.success(f"✅ Uploaded {success} records to Airtable.")

# --- AI Query ---
st.markdown("---")


st.subheader("🤖 Ask a Question About the Data")

user_query = st.text_input("Enter your question:", placeholder="e.g., Show me all unmapped orders")

if st.button("Ask AI") and user_query and not mapped_df.empty:
    with st.spinner("Analyzing with AI..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data assistant. Convert user questions into pandas DataFrame filter strings using these columns: OrderID, SKU, MSKU, Mapped_Qty, Status."
                    },
                    {
                        "role": "user",
                        "content": f"My data looks like this:\n{mapped_df.head(3).to_string()}\n\nNow filter it with:\n{user_query}"
                    }
                ],
                temperature=0.2
            )

            filter_code = response.choices[0].message.content.strip()
            st.code(filter_code, language='python')

            try:
                filtered_df = mapped_df.query(filter_code)
                st.success("✅ Filter applied")
                st.dataframe(filtered_df)
            except Exception as fe:
                st.error(f"❌ Failed to apply filter: {fe}")

        except Exception as e:
            st.error(f"⚠️ AI Query Error: {e}")
