import streamlit as st
import os
import pandas as pd
import plotly.express as px

st.title("HBS Data")

# Load the HBS parquet
parquet_path = r"C:\Users\Scotty Lumb\code\python\streamlit-maps\data\hbs_history.parquet"
if os.path.exists(parquet_path):
    df_hbs = pd.read_parquet(parquet_path)
else:
    st.error(f"Parquet file not found at {parquet_path}")
    st.stop()

# --- Example unique values for filters ---
lst_scale_sites = df_hbs["scale_site"].unique().tolist()
lst_spp_codes = df_hbs["species_code"].unique().tolist()
lst_products = df_hbs["product_code"].unique().tolist() 
lst_regions = df_hbs["region_harvested_description"].unique().tolist()
lst_mgmt_unit_types = df_hbs["mgmt_unit_type_description"].unique().tolist()
lst_mgmt_unit_ids = df_hbs["mgmt_unit_id"].unique().tolist()

# --- Filter form ---
with st.form("filter_form"):
    selected_scale_sites = st.multiselect("Select scale sites", lst_scale_sites)
    selected_spp_codes = st.multiselect("Select species codes", lst_spp_codes)
    selected_products = st.multiselect("Select product codes", lst_products)
    selected_regions = st.multiselect("Select regions", lst_regions, default=lst_regions[:1])
    selected_mgmt_unit_types = st.multiselect("Select management unit types", lst_mgmt_unit_types)
    selected_mgmt_unit_ids = st.multiselect("Select management unit IDs", lst_mgmt_unit_ids)
    
    submitted = st.form_submit_button("Apply Filters")

# --- Filter data if submitted, otherwise show all ---
df_filtered = df_hbs.copy()
if submitted:
    mask = pd.Series(True, index=df_filtered.index)
    mask &= df_filtered["region_harvested_description"].isin(selected_regions)
    if selected_scale_sites:
        mask &= df_filtered["scale_site"].isin(selected_scale_sites)
    if selected_spp_codes:
        mask &= df_filtered["species_code"].isin(selected_spp_codes)
    if selected_products:
        mask &= df_filtered["product_code"].isin(selected_products)
    if selected_mgmt_unit_types:
        mask &= df_filtered["mgmt_unit_type_description"].isin(selected_mgmt_unit_types)
    if selected_mgmt_unit_ids:
        mask &= df_filtered["mgmt_unit_id"].isin(selected_mgmt_unit_ids)
    df_filtered = df_filtered[mask]

# --- Display chart ---
st.subheader("Harvest Volume by Year")
if not df_filtered.empty:
    fig = px.bar(
        df_filtered,
        x="year",
        y="total_volume_scaled",
        color="species_code",
        labels={"total_volume_scaled": "Harvest Volume", "year": "Year"},
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data for selected filters.")

# --- Show summary numbers ---
st.subheader("Summary")
st.write(f"Total rows: {len(df_filtered)}")
st.write(f"Total harvest volume: {df_filtered['total_volume_scaled'].sum():,.0f}")

# --- Excel download ---
if not df_filtered.empty:
    excel_file = "hbs_filtered.xlsx"
    df_filtered.to_excel(excel_file, index=False)
    st.download_button(
        label="Download filtered data as Excel",
        data=open(excel_file, "rb"),
        file_name="hbs_filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- Show pandas code snippet for filtering ---
st.subheader("Pandas Code Used to Filter")
code_snippet = f"""
# Original DataFrame: df_hbs
df_filtered = df_hbs.copy()
mask = pd.Series(True, index=df_filtered.index)
mask &= df_filtered["region_harvested_description"].isin({selected_regions})
if {selected_scale_sites}:
    mask &= df_filtered["scale_site"].isin({selected_scale_sites})
if {selected_spp_codes}:
    mask &= df_filtered["species_code"].isin({selected_spp_codes})
if {selected_products}:
    mask &= df_filtered["product_code"].isin({selected_products})
if {selected_mgmt_unit_types}:
    mask &= df_filtered["mgmt_unit_type_description"].isin({selected_mgmt_unit_types})
if {selected_mgmt_unit_ids}:
    mask &= df_filtered["mgmt_unit_id"].isin({selected_mgmt_unit_ids})
df_filtered = df_filtered[mask]
"""

if selected_scale_sites:
    code_lines.append(f"mask &= df_filtered['scale_site'].isin({selected_scale_sites})")
if selected_spp_codes:
    code_lines.append(f"mask &= df_filtered['species_code'].isin({selected_spp_codes})")
if selected_products:
    code_lines.append(f"mask &= df_filtered['product_code'].isin({selected_products})")
if selected_mgmt_unit_types:
    code_lines.append(f"mask &= df_filtered['mgmt_unit_type_description'].isin({selected_mgmt_unit_types})")
if selected_mgmt_unit_ids:
    code_lines.append(f"mask &= df_filtered['mgmt_unit_id'].isin({selected_mgmt_unit_ids})")

code_lines.append("df_filtered = df_filtered[mask]")

# Join lines into a single string for Streamlit
code_snippet = "\n".join(code_lines)
st.code(code_snippet, language="python")
