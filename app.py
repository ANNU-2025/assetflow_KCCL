import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from datetime import datetime

# ==========================================
# 1. DATABASE CONFIGURATION & INITIALIZATION
# ==========================================
url = "https://emdjnndnsdebhbzebrsg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtZGpubmRuc2RlYmhiemVicnNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODExNzU4NDYsImV4cCI6MjA5Njc1MTg0Nn0.ypy3k30Nbp2caJaNXpwxbrnUzrOLrhwTJ1FZwW5L8Fc"
supabase: Client = create_client(url, key)

st.set_page_config(page_title="AssetFlow KCCL Template", layout="wide")

# --- LOGO PROVISION FOR ALL PAGES ---
def add_logo():
    if os.path.exists("assets/logo.png"):
        st.sidebar.image("assets/logo.png", width=150)
    else:
        # CORRECTED: unsafe_allow_html used here
        st.sidebar.markdown("<h2 style='text-align: center; color: #00D2FF;'>📦 AssetFlow</h2>", unsafe_allow_html=True)

add_logo()

# ==========================================
# 2. LOGIN MECHANISM (TEMPLATE SESSION-BASED)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.subheader("🔑 System Secure Login")
    with st.form("Login Form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_login = st.form_submit_button("Login")
        
        if submit_login:
            if username == "admin" and password == "kccl@2026":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Username or Password!")
    st.stop()

# Logout provision in sidebar
if st.sidebar.button("🔓 Logout"):
    st.session_state['logged_in'] = False
    st.rerun()

st.sidebar.markdown("---")
page = st.sidebar.radio("📌 Navigation Menu", ["Dashboard", "Transaction", "Reports"])

# Helper function to convert dataframes safely to CSV bytes
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# ==========================================
# 3. DASHBOARD PAGE
# ==========================================
if page == "Dashboard":
    st.header("📈 Inventory Dashboard Summary")
    
    try:
        p_res = supabase.table('tpl_inv_products').select('*').execute()
        tx_res = supabase.table('tpl_inv_transactions').select('*').execute()
        
        df_p = pd.DataFrame(p_res.data)
        df_t = pd.DataFrame(tx_res.data)
    except Exception as e:
        st.error(f"Database query processing failed: {e}")
        df_p, df_t = pd.DataFrame(), pd.DataFrame()

    if not df_p.empty:
        st.subheader("📦 Product Inventory Cards")
        cols = st.columns(4)
        
        product_summaries = []
        
        for idx, row in df_p.iterrows():
            p_id = row['id']
            p_name = row['product_name']
            i_code = row['item_code']
            u_type = row['default_unit']
            
            if not df_t.empty and 'product_id' in df_t.columns:
                p_tx = df_t[df_t['product_id'] == p_id]
                
                uploaded = pd.to_numeric(p_tx[p_tx['action_type'] == 'UPLOAD']['quantity']).sum()
                returned = pd.to_numeric(p_tx[p_tx['action_type'] == 'RETURN']['quantity']).sum()
                issued = pd.to_numeric(p_tx[p_tx['action_type'] == 'ISSUE']['quantity']).sum()
                
                in_stock = (uploaded + returned) - issued
                total_added = row['total_added_to_system'] if 'total_added_to_system' in row else uploaded
            else:
                in_stock = 0.0
                total_added = 0

            product_summaries.append({
                "Product Name": p_name,
                "Item Code": i_code,
                "In Stock Quantity": f"{in_stock:.3f} {u_type}",
                "Total System Entry": total_added
            })

            # Display individual cards loop
            with cols[idx % 4]:
                # CORRECTED: unsafe_allow_html used here as well
                st.markdown(
                    f"""
                    <div style="border: 2px solid #4A4A4A; padding: 15px; border-radius: 10px; background-color: #1E1E1E; margin-bottom: 15px;">
                        <h4 style='color: #00D2FF; margin: 0;'>{p_name}</h4>
                        <small style='color: #888;'>Code: {i_code}</small>
                        <h2 style='margin: 10px 0; color: #FFF;'>{in_stock:.3f} <span style='font-size: 16px;'>{u_type}</span></h2>
                        <div style='border-top: 1px solid #333; padding-top: 5px;'>
                            <span style='font-size: 11px; color: #AAA;'>Total Count (Added): <b>{total_added}</b></span>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        
        df_summary_download = pd.DataFrame(product_summaries)

        st.markdown("---")
        st.subheader("📥 Master Download Dashboard Operations")
        
        dl_col1, dl_col2, dl_col3 = st.columns(3)
        
        with dl_col1:
            st.markdown("##### 1. Master Dump Log")
            if not df_t.empty:
                st.download_button(
                    label="📥 Download Full Dump CSV",
                    data=convert_df_to_csv(df_t),
                    file_name=f"full_inventory_dump_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="dl_full_dump"
                )
            else:
                st.caption("No transaction logs recorded to dump yet.")
                
        with dl_col2:
            st.markdown("##### 2. Product Summary Logs")
            if not df_summary_download.empty:
                st.download_button(
                    label="📥 Download Product Summary",
                    data=convert_df_to_csv(df_summary_download),
                    file_name="product_stock_summary.csv",
                    mime="text/csv",
                    key="dl_prod_summary"
                )
                
        with dl_col3:
            st.markdown("##### 3. Card Click Issued Details")
            target_p = st.selectbox("Choose Card Product Line", df_p['product_name'].unique())
            if target_p and not df_t.empty:
                target_id = df_p[df_p['product_name'] == target_p]['id'].values[0]
                df_card_issued = df_t[(df_t['product_id'] == target_id) & (df_t['action_type'] == 'ISSUE')]
                
                if not df_card_issued.empty:
                    st.download_button(
                        label=f"📥 Download {target_p} Issued Data",
                        data=convert_df_to_csv(df_card_issued),
                        file_name=f"{target_p.lower().replace(' ', '_')}_issued_details.csv",
                        mime="text/csv"
                    )
                else:
                    st.caption("No issue entries recorded for this item line.")
    else:
        st.info("Your custom table 'tpl_inv_products' is currently empty. Please populate it in Supabase.")

# ==========================================
# 4. TRANSACTION PAGE
# ==========================================
elif page == "Transaction":
    st.header("🔄 Stock Transaction Registry Pipeline")
    
    try:
        p_res = supabase.table('tpl_inv_products').select('id', 'product_name', 'item_code').execute()
        raw_p_list = p_res.data
    except:
        raw_p_list = []

    if raw_p_list:
        p_map = {item['product_name']: item for item in raw_p_list}
        col_form1, col_form2 = st.columns(2)
        
        with col_form1:
            selected_product_name = st.selectbox("Select Product List (Dynamic Master Dropdown)", list(p_map.keys()))
            target_product = p_map[selected_product_name]
            
            st.text_input("Item Code Identifier", value=target_product['item_code'], disabled=True)
            serial_number = st.text_area("Serial Number Registry (Separate entries with commas)")
            
            unit = st.selectbox("Unit Classification System", ["PCS", "LTR", "ML", "MTR", "DRUM", "BOX"])
            quantity = st.number_input("Transaction Quantity Input Value", min_value=0.000, step=0.001, format="%.3f")
            
        with col_form2:
            issued_to = st.text_input("Issued To Destination Person/Vendor Name")
            invoice_no = st.text_input("Invoice Tracking Number / DC No")
            action_type = st.selectbox("Action Execution Method", ["ISSUE", "RETURN", "UPLOAD"])
            st.markdown("<br><br>", unsafe_with_html=True)
            submit_tx = st.button("⚡ Execute & Commit Transaction to Database", use_container_width=True)

        if submit_tx:
            if quantity <= 0:
                st.error("Transaction failed: Quantity must be greater than zero.")
            else:
                execution_time = datetime.now().isoformat()
                
                tx_payload = {
                    "product_id": target_product['id'],
                    "item_code": target_product['item_code'],
                    "serial_number": serial_number,
                    "quantity": quantity,
                    "unit": unit,
                    "issued_to": issued_to,
                    "invoice_no": invoice_no,
                    "action_type": action_type,
                    "created_at": execution_time
                }
                
                try:
                    supabase.table('tpl_inv_transactions').insert(tx_payload).execute()
                    st.success(f"Successfully tracked: {action_type} action locked at {execution_time}!")
                except Exception as ex:
                    st.error(f"Failed to post ledger configuration setup: {ex}")
    else:
        st.warning("No Master Product mappings detected. Please confirm database setup records exist in 'tpl_inv_products'.")

# ==========================================
# 5. REPORTS PAGE (ADVANCED AUTO-FILTERS)
# ==========================================
elif page == "Reports":
    st.header("📊 Advanced Analytics & Multi-Filter Ledger Reports")
    
    try:
        tx_res = supabase.table('tpl_inv_transactions').select('*').execute()
        df_master_report = pd.DataFrame(tx_res.data)
        
        p_res = supabase.table('tpl_inv_products').select('id', 'product_name').execute()
        df_product_map = pd.DataFrame(p_res.data)
    except:
        df_master_report = pd.DataFrame()
        df_product_map = pd.DataFrame()

    if not df_master_report.empty:
        if not df_product_map.empty:
            df_master_report = pd.merge(df_master_report, df_product_map, left_on="product_id", right_on="id", how="left")
        
        st.markdown("### 🔍 Real-time Auto Filter Options")
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        filter_col4, filter_col5 = st.columns(2)
        
        with filter_col1:
            chosen_action = st.multiselect("Filter by Action Status", df_master_report['action_type'].unique())
        with filter_col2:
            chosen_item = st.multiselect("Filter by Product Line Name", df_master_report['product_name'].unique() if 'product_name' in df_master_report.columns else df_master_report['item_code'].unique())
        with filter_col3:
            chosen_recipient = st.multiselect("Filter by Recipient Name (Issued To)", df_master_report['issued_to'].dropna().unique())
        with filter_col4:
            chosen_invoice = st.multiselect("Filter by Invoice Tracking Code", df_master_report['invoice_no'].dropna().unique())
        with filter_col5:
            st.caption("Date parsing framework auto active")
            
        df_filtered = df_master_report.copy()
        
        if chosen_action:
            df_filtered = df_filtered[df_filtered['action_type'].isin(chosen_action)]
        if chosen_item:
            if 'product_name' in df_filtered.columns:
                df_filtered = df_filtered[df_filtered['product_name'].isin(chosen_item)]
            else:
                df_filtered = df_filtered[df_filtered['item_code'].isin(chosen_item)]
        if chosen_recipient:
            df_filtered = df_filtered[df_filtered['issued_to'].isin(chosen_recipient)]
        if chosen_invoice:
            df_filtered = df_filtered[df_filtered['invoice_no'].isin(chosen_invoice)]
            
        st.markdown("---")
        st.dataframe(df_filtered, use_container_width=True)
        
        st.download_button(
            label="📥 Export Current Filtered View to CSV Ledger File",
            data=convert_df_to_csv(df_filtered),
            file_name="filtered_inventory_report.csv",
            mime="text/csv",
            key="dl_filtered_report"
        )
    else:
        st.info("Ledger analytics parameters are blank. Try appending transactions mapping profiles first.")
