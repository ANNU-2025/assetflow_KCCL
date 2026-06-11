import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from datetime import datetime

# --- LOGO PROVISION FOR ALL PAGES ---
def add_logo():
    # assets/logo.png thakle load hobe, naholay direct text dekhabe
    if os.path.exists("assets/logo.png"):
        st.sidebar.image("assets/logo.png", width=150)
    else:
        st.sidebar.title("📦 MY INVENTORY")

# --- SUPABASE CONNECTION ---
# Render-e deploy korle dynamic pull korbe env variable theke
url = "https://emdjnndnsdebhbzebrsg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtZGpubmRuc2RlYmhiemVicnNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODExNzU4NDYsImV4cCI6MjA5Njc1MTg0Nn0.ypy3k30Nbp2caJaNXpwxbrnUzrOLrhwTJ1FZwW5L8Fc"
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Inventory Management Template", layout="wide")
add_logo()

# --- NAVIGATION ---
page = st.sidebar.radio("Navigation", ["Dashboard", "Transaction", "Reports"])

# ==========================================
# 1. DASHBOARD PAGE
# ==========================================
if page == "Dashboard":
    st.header("📈 Inventory Dashboard")
    
    # Supabase theke uncommon table query pull
    try:
        products_res = supabase.table('tpl_inv_products').select('*').execute()
        summary_res = supabase.table('tpl_inv_stock_summary').select('*').execute()
        tx_res = supabase.table('tpl_inv_transactions').select('*').execute()
        
        df_p = pd.DataFrame(products_res.data)
        df_s = pd.DataFrame(summary_res.data)
        df_t = pd.DataFrame(tx_res.data)
    except Exception as e:
        st.error(f"Database error: {e}")
        df_p, df_s, df_t = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    if not df_s.empty and not df_p.empty:
        # Merge product name for visualization
        df_dash = pd.merge(df_s, df_p, on="product_id")
        
        # PRODUCT WISE CARDS LOOP
        cols = st.columns(4)
        for idx, row in df_dash.iterrows():
            with cols[idx % 4]:
                st.metric(
                    label=f"📦 {row['product_name']} ({row['item_code']})",
                    value=f"{row['in_stock_qty']} {row['default_unit']}",
                    delta=f"Total Added: {row['total_system_qty']}",
                    delta_color="off"
                )
    else:
        st.info("No product data available in your uncommon tables yet.")

    st.markdown("---")
    st.subheader("📥 Download Section")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not df_t.empty:
            csv_dump = df_t.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Full Dump", data=csv_dump, file_name="full_dump.csv", mime="text/csv")
            
    with col2:
        if not df_s.empty:
            csv_sum = df_s.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Product Summary", data=csv_sum, file_name="product_summary.csv", mime="text/csv")
            
    with col3:
        selected_card = st.selectbox("Select Product for Issued Details", df_p['product_name'].unique() if not df_p.empty else [])
        if selected_card and not df_t.empty:
            # Filter issued details for click response
            p_id = df_p[df_p['product_name'] == selected_card]['id'].values[0]
            df_issued = df_t[(df_t['product_id'] == p_id) & (df_t['action_type'] == 'ISSUE')]
            csv_issued = df_issued.to_csv(index=False).encode('utf-8')
            st.download_button(f"📥 Download {selected_card} Issued Logs", data=csv_issued, file_name=f"{selected_card}_issued.csv", mime="text/csv")

# ==========================================
# 2. TRANSACTION PAGE
# ==========================================
elif page == "Transaction":
    st.header("🔄 New Transaction Entry")
    
    # Dynamic Dropdown load from Master table
    try:
        p_res = supabase.table('tpl_inv_products').select('id', 'product_name', 'item_code').execute()
        products_list = p_res.data
    except:
        products_list = []
        
    if products_list:
        p_options = {p['product_name']: p for p in products_list}
        selected_p_name = st.selectbox("Product List (Dropdown)", list(p_options.keys()))
        
        selected_p = p_options[selected_p_name]
        item_code = st.text_input("Item Code", value=selected_p['item_code'], disabled=True)
        
        serial_no = st.text_input("Serial Number (For bulk, separate with comma)")
        
        # Unit and Stock fractional logic (.5 ML validation handle)
        unit = st.selectbox("Unit", ["PCS", "LTR", "ML", "MTR"])
        quantity = st.number_input("Quantity", min_value=0.000, step=0.100, format="%.3f")
        
        issued_to = st.text_input("Issued To")
        invoice_no = st.text_input("Invoice No")
        action = st.selectbox("Action", ["ISSUE", "RETURN", "UPLOAD"])
        
        if st.button("Submit Transaction"):
            # Automatic Capture of current Date and Time
            timestamp = datetime.now().isoformat()
            
            tx_data = {
                "product_id": selected_p['id'],
                "item_code": selected_p['item_code'],
                "serial_number": serial_no,
                "quantity": quantity,
                "unit": unit,
                "issued_to": issued_to,
                "invoice_no": invoice_no,
                "action_type": action,
                "created_at": timestamp
            }
            
            # Insert logic into Supabase
            try:
                supabase.table('tpl_inv_transactions').insert(tx_data).execute()
                st.success(f"Transaction recorded successfully at {timestamp}!")
            except Exception as e:
                st.error(f"Error saving transaction: {e}")
    else:
        st.warning("Please add products to 'tpl_inv_products' table first.")

# ==========================================
# 3. REPORTS PAGE (AUTO FILTERS & DOWNLOAD)
# ==========================================
elif page == "Reports":
    st.header("📊 Advanced Auto-Filter Reports")
    
    try:
        tx_res = supabase.table('tpl_inv_transactions').select('*').execute()
        df_rep = pd.DataFrame(tx_res.data)
    except:
        df_rep = pd.DataFrame()
        
    if not df_rep.empty:
        # Layout design for auto-filters
        f_col1, f_col2, f_col3 = st.columns(3)
        
        with f_col1:
            filter_action = st.multiselect("Action Filter", df_rep['action_type'].unique())
        with f_col2:
            filter_item = st.multiselect("Item Code Filter", df_rep['item_code'].unique())
        with f_col3:
            filter_invoice = st.multiselect("Invoice Filter", df_rep['invoice_no'].dropna().unique())
            
        # Apply Pandas Filters dynamically
        df_filtered = df_rep.copy()
        if filter_action:
            df_filtered = df_filtered[df_filtered['action_type'].isin(filter_action)]
        if filter_item:
            df_filtered = df_filtered[df_filtered['item_code'].isin(filter_item)]
        if filter_invoice:
            df_filtered = df_filtered[df_filtered['invoice_no'].isin(filter_invoice)]
            
        st.dataframe(df_filtered, use_container_width=True)
        
        # Download Filtered Report
        csv_rep = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Filtered Report", data=csv_rep, file_name="filtered_report.csv", mime="text/csv")
    else:
        st.info("No transaction reports available.")
