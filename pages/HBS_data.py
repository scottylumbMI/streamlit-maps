

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
        color="region_harvested_description",
        labels={"total_volume_scaled": "Harvest Volume", "year": "Year"},
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data for selected filters.")

# --- Show summary numbers ---
st.subheader("Summary")
st.write(f"Total rows: {len(df_filtered)}")
st.write(f"Total harvest volume: {df_filtered['total_volume_scaled'].sum():,.0f}")









# import streamlit as st
# import leafmap.foliumap as leafmap
# import os
# from sqlalchemy import create_engine
# from sqlalchemy import text
# import pandas as pd
# import geopandas as gpd
# import plotly.express as px





# st.title("HBS data")

# col_chart ,col_map = st.columns([3, 1])
# options = list(leafmap.basemaps.keys())
# index = options.index("OpenTopoMap")

# gdf_path_regions = r"C:\Users\Scotty Lumb\code\python\streamlit-maps\data\nr_regions.shp"

# # Load the HBS parquet
# parquet_path = r"C:\Users\Scotty Lumb\code\python\streamlit-maps\data\hbs_history.parquet"
# if os.path.exists(parquet_path):
#     df_hbs = pd.read_parquet(parquet_path)
# else:
#     st.error(f"Parquet file not found at {parquet_path}")
#     st.stop()
    
# # Example: unique values for dropdowns
# lst_scale_sites = df_hbs["scale_site"].unique().tolist()
# lst_spp_codes = df_hbs["species_code"].unique().tolist()
# lst_products = df_hbs["product_code"].unique().tolist() 
# lst_regions = df_hbs["region_harvested_description"].unique().tolist()
# lst_mgmt_unit_types = df_hbs["mgmt_unit_type_description"].unique().tolist()
# lst_mgmt_unit_ids = df_hbs["mgmt_unit_id"].unique().tolist()



# # --- Filter form ---
# with st.form("filter_form"):
#     selected_scale_sites = st.multiselect("Select scale sites", lst_scale_sites)
#     selected_spp_codes = st.multiselect("Select species codes", lst_spp_codes)
#     selected_products = st.multiselect("Select product codes", lst_products)
#     selected_regions = st.multiselect("Select regions", lst_regions, default=lst_regions[:1])
#     selected_mgmt_unit_types = st.multiselect("Select management unit types", lst_mgmt_unit_types)
#     selected_mgmt_unit_ids = st.multiselect("Select management unit IDs", lst_mgmt_unit_ids)
    
#     submitted = st.form_submit_button("Apply Filters")

# # Ensure `submitted` is defined even if form hasn't been submitted yet
# if 'submitted' not in locals():
#     submitted = False

# # --- Filter data if submitted, otherwise show all ---
# df_filtered = df_hbs.copy()
# if submitted:
#     mask = pd.Series(True, index=df_filtered.index)
#     mask &= df_filtered["region_harvested_description"].isin(selected_regions)
#     if selected_scale_sites:
#         mask &= df_filtered["scale_site"].isin(selected_scale_sites)
#     if selected_spp_codes:
#         mask &= df_filtered["species_code"].isin(selected_spp_codes)
#     if selected_products:
#         mask &= df_filtered["product_code"].isin(selected_products)
#     if selected_mgmt_unit_types:
#         mask &= df_filtered["mgmt_unit_type_description"].isin(selected_mgmt_unit_types)
#     if selected_mgmt_unit_ids:
#         mask &= df_filtered["mgmt_unit_id"].isin(selected_mgmt_unit_ids)
#     df_filtered = df_filtered[mask]

# # --- Always render chart ---
# with col_chart:
#     fig = px.bar(
#         df_filtered,
#         x="year",
#         y="total_volume_scaled",
#         color="region_harvested_description",
#         title="Harvest Volume",
#         labels={"total_volume_scaled": "Harvest Volume", "year": "Year"}
#     )
#     st.plotly_chart(fig, use_container_width=True)

# # --- Always render map ---
# with col_map:
#     m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
#     if os.path.exists(gdf_path_regions):
#         gdf_regions = gpd.read_file(gdf_path_regions)
#         if submitted:
#             gdf_regions_filtered = gdf_regions[gdf_regions["rgn_name"].isin(selected_regions)]
#             m.add_gdf(gdf_regions_filtered, layer_name="Selected Regions")
#         else:
#             m.add_gdf(gdf_regions, layer_name="Regions")
#     m.add_basemap(st.selectbox("Select a basemap:", options, index))
#     m.to_streamlit(height=300, return_selected=True)



# # --- Filter form ---
# with st.form("filter_form"):
#     selected_scale_sites = st.multiselect("Select scale sites", lst_scale_sites)
#     selected_spp_codes = st.multiselect("Select species codes", lst_spp_codes)
#     selected_products = st.multiselect("Select product codes", lst_products)
#     selected_regions = st.multiselect("Select regions", lst_regions, default=lst_regions[:1])
#     selected_mgmt_unit_types = st.multiselect("Select management unit types", lst_mgmt_unit_types)
#     selected_mgmt_unit_ids = st.multiselect("Select management unit IDs", lst_mgmt_unit_ids)
    
#     submitted = st.form_submit_button("Apply Filters")

# # --- Filter data if submitted, otherwise show all ---
# df_filtered = df_hbs.copy()
# if submitted:
#     mask = pd.Series(True, index=df_filtered.index)
#     mask &= df_filtered["region_harvested_description"].isin(selected_regions)
#     if selected_scale_sites:
#         mask &= df_filtered["scale_site"].isin(selected_scale_sites)
#     if selected_spp_codes:
#         mask &= df_filtered["species_code"].isin(selected_spp_codes)
#     if selected_products:
#         mask &= df_filtered["product_code"].isin(selected_products)
#     if selected_mgmt_unit_types:
#         mask &= df_filtered["mgmt_unit_type_description"].isin(selected_mgmt_unit_types)
#     if selected_mgmt_unit_ids:
#         mask &= df_filtered["mgmt_unit_id"].isin(selected_mgmt_unit_ids)
#     df_filtered = df_filtered[mask]

# # --- Always render chart and map ---
# with col_chart:
#     fig = px.bar(
#         df_filtered,
#         x="year",
#         y="total_volume_scaled",
#         color="region_harvested_description",
#         title="Harvest Volume",
#         labels={"total_volume_scaled": "Harvest Volume", "year": "Year"}
#     )
#     st.plotly_chart(fig, use_container_width=True)

# # with col_map:
#     # m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
#     # if os.path.exists(gdf_path_regions):
#     #     gdf_regions = gpd.read_file(gdf_path_regions)
#     #     if submitted:
#     #         gdf_regions_filtered = gdf_regions[gdf_regions["rgn_name"].isin(selected_regions)]
#     #         m.add_gdf(gdf_regions_filtered, layer_name="Selected Regions")
#     #     else:
#     #         m.add_gdf(gdf_regions, layer_name="Regions")
#     # m.add_basemap(st.selectbox("Select a basemap:", options, index))
#     # m.to_streamlit(height=300, return_selected=True)
