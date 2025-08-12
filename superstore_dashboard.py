import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import io
from datetime import datetime
import calendar

# Page setup
st.set_page_config(
    page_title="📦 Superstore Analytics Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Styling
st.markdown("""
    <style>
        .big-font {
            font-size:28px !important;
        }
        .metric {
            font-size: 22px;
            font-weight: bold;
            color: #444;
        }
        .metric-label {
            font-size: 14px;
            color: #666;
        }
        .metric-positive {
            color: #1cc88a !important;
        }
        .metric-negative {
            color: #e74a3b !important;
        }
        .section-header {
            font-size:24px;
            margin-top:20px;
            border-bottom:2px solid #f0f0f0;
            padding-bottom:5px;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .stSelectbox > div > div {
            border-radius: 8px !important;
        }
        .stSlider > div > div {
            border-radius: 8px !important;
        }
        .stDateInput > div > div {
            border-radius: 8px !important;
        }
        .stRadio > div {
            flex-direction: row !important;
            gap: 15px !important;
        }
        .stRadio > div > label {
            margin-bottom: 0 !important;
        }
        .hover-card {
            transition: all 0.3s ease;
            border-radius: 10px;
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 4px solid #4e73df;
        }
        .hover-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .tab-content {
            padding: 15px 0;
        }
        .dataframe {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# Title with animated header
st.markdown("""
<style>
    /* Remove default Streamlit padding */
    .stApp {
        padding-top: 0rem;
        padding-right: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
    }
    
    /* Full-width header container */
    .full-width-header {
        margin: 0 -1rem;  /* Counteract Streamlit's padding */
        padding: 15px 0;
        background: linear-gradient(90deg, #4e73df 0%, #224abe 100%);
        color: white;
        border-radius: 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Center content within header */
    .header-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .big-font {
        font-size: 2.5rem !important;
        margin: 0;
        text-align: center;
    }
</style>

<div class="full-width-header">
    <div class="header-content">
        <h1 class='big-font'>📊 Superstore Analytics Pro Dashboard</h1>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:gray; margin-top:10px;'>Advanced insights with interactive visualizations and predictive analytics</p>", unsafe_allow_html=True)
st.markdown("---")
# Load and process data
@st.cache_data
def load_data():
    df = pd.read_csv("Sample - Superstore.csv", encoding="latin-1")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    df['Order Month'] = df['Order Date'].dt.month
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Day of Week'] = df['Order Date'].dt.dayofweek
    df['Order Quarter'] = df['Order Date'].dt.quarter
    df['Processing Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100
    return df

data = load_data()

# Sidebar with enhanced filters
with st.sidebar:
    st.image("market-analysis.png", width=100)
    st.title("🔍 Data Filters")
    
    # Date range filter
    min_date = data['Order Date'].min().date()
    max_date = data['Order Date'].max().date()
    date_range = st.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Convert to datetime
    if len(date_range) == 2:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered_data = data[(data['Order Date'] >= start_date) & (data['Order Date'] <= end_date)]
    else:
        filtered_data = data
    
    # Multi-select filters
    regions = st.multiselect(
        "Select Regions",
        options=data['Region'].unique(),
        default=data['Region'].unique()
    )
    
    categories = st.multiselect(
        "Select Categories",
        options=data['Category'].unique(),
        default=data['Category'].unique()
    )
    
    segments = st.multiselect(
        "Select Customer Segments",
        options=data['Segment'].unique(),
        default=data['Segment'].unique()
    )
    
    # Apply filters
    filtered_data = filtered_data[
        (filtered_data['Region'].isin(regions)) &
        (filtered_data['Category'].isin(categories)) &
        (filtered_data['Segment'].isin(segments))
    ]
    
    # Add download button
    st.markdown("---")
    st.markdown("### 📤 Export Data")
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name=f"superstore_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv'
    )

# Enhanced KPI cards
st.markdown("<div class='section-header'>📊 Performance Overview</div>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
# Add CSS styling at the beginning of your script
st.markdown("""
<style>
.hover-card {
    width: 220px;          /* Fixed width */
    height: 140px;         /* Fixed height */
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin: 10px;
    border: 1px solid #e0e0e0;
}
.hover-card:hover {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}
.metric-label {
    font-size: 16px;
    color: #555;
    margin-bottom: 8px;
    text-align: center;
    font-weight: 500;
}
.metric {
    font-size: 28px;
    font-weight: 700;
    color: #2c3e50;
    text-align: center;
    margin: 0;
}
.metric-positive {
    color: #27ae60;
}
.metric-negative {
    color: #e74c3c;
}
</style>
""", unsafe_allow_html=True)

# KPI 1 - Total Sales (Blue-themed)
with kpi1:
    st.markdown("""
    <div class="hover-card" style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);">
        <p class="metric-label">Total Sales</p>
        <p class="metric">${:,.0f}</p>
    </div>
    """.format(filtered_data["Sales"].sum()), unsafe_allow_html=True)

# KPI 2 - Total Profit (Green/Red based on value)
with kpi2:
    profit = filtered_data["Profit"].sum()
    profit_class = "metric-positive" if profit >= 0 else "metric-negative"
    card_color = "background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);" if profit >=0 else "background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);"
    
    st.markdown(f"""
    <div class="hover-card" style="{card_color}">
        <p class="metric-label">Total Profit</p>
        <p class="metric {profit_class}">${profit:,.0f}</p>
    </div>
    """, unsafe_allow_html=True)

# KPI 3 - Total Orders (Purple-themed)
with kpi3:
    st.markdown("""
    <div class="hover-card" style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);">
        <p class="metric-label">Total Orders</p>
        <p class="metric">{:,}</p>
    </div>
    """.format(filtered_data["Order ID"].nunique()), unsafe_allow_html=True)

# KPI 4 - Avg. Profit Margin (Teal-themed)
with kpi4:
    avg_profit_margin = filtered_data["Profit Margin"].mean()
    margin_class = "metric-positive" if avg_profit_margin >= 0 else "metric-negative"
    
    st.markdown(f"""
    <div class="hover-card" style="background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);">
        <p class="metric-label">Avg. Profit Margin</p>
        <p class="metric {margin_class}">{avg_profit_margin:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

# Tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "📦 Products", "👥 Customers", "🗺️ Geography"])

with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # Time series analysis
    st.markdown("<div class='section-header'>🕒 Time Series Analysis</div>", unsafe_allow_html=True)
    
    # Granularity selector
    time_granularity = st.radio(
        "Select Time Granularity",
        ["Daily", "Weekly", "Monthly", "Quarterly"],
        horizontal=True
    )
    
    # Prepare time series data based on granularity
    if time_granularity == "Daily":
        ts_data = filtered_data.groupby("Order Date").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        x_col = "Order Date"
    elif time_granularity == "Weekly":
        ts_data = filtered_data.copy()
        ts_data["Week"] = ts_data["Order Date"].dt.to_period("W").dt.start_time
        ts_data = ts_data.groupby("Week").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        x_col = "Week"
    elif time_granularity == "Monthly":
        ts_data = filtered_data.copy()
        ts_data["Month"] = ts_data["Order Date"].dt.to_period("M").dt.start_time
        ts_data = ts_data.groupby("Month").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        x_col = "Month"
    else:  # Quarterly
        ts_data = filtered_data.copy()
        ts_data["Quarter"] = ts_data["Order Date"].dt.to_period("Q").dt.start_time
        ts_data = ts_data.groupby("Quarter").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        x_col = "Quarter"
    
    # Create dual-axis chart
    fig = go.Figure()
    
    # Add Sales trace
    fig.add_trace(
        go.Scatter(
            x=ts_data[x_col],
            y=ts_data["Sales"],
            name="Sales",
            line=dict(color="#4e73df", width=2),
            yaxis="y1"
        )
    )
    
    # Add Profit trace
    fig.add_trace(
        go.Scatter(
            x=ts_data[x_col],
            y=ts_data["Profit"],
            name="Profit",
            line=dict(color="#1cc88a", width=2),
            yaxis="y2"
        )
    )
    
    # Update layout for dual y-axes
    fig.update_layout(
        title=f"Sales & Profit Trend ({time_granularity})",
        xaxis_title="Date",
        yaxis=dict(
            title="Sales ($)",
            title_font=dict(color="#4e73df"),
            tickfont=dict(color="#4e73df")
        ),
        yaxis2=dict(
            title="Profit ($)",
            title_font=dict(color="#1cc88a"),
            tickfont=dict(color="#1cc88a"),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekday analysis
    st.markdown("<div class='section-header'>📅 Day of Week Analysis</div>", unsafe_allow_html=True)
    
    weekday_data = filtered_data.copy()
    weekday_data["Day of Week"] = weekday_data["Order Date"].dt.day_name()
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_data["Day of Week"] = pd.Categorical(weekday_data["Day of Week"], categories=weekday_order, ordered=True)
    weekday_data = weekday_data.groupby("Day of Week").agg({"Sales": "sum", "Profit": "sum", "Order ID": "nunique"}).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            weekday_data,
            x="Day of Week",
            y="Sales",
            title="Sales by Day of Week",
            color="Sales",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            weekday_data,
            x="Day of Week",
            y="Profit",
            title="Profit by Day of Week",
            color="Profit",
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # Product category analysis
    st.markdown("<div class='section-header'>📦 Product Category Analysis</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        sales_cat = filtered_data.groupby("Category")["Sales"].sum().reset_index()
        fig = px.pie(
            sales_cat,
            names="Category",
            values="Sales",
            title="Sales Distribution by Category",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        profit_cat = filtered_data.groupby("Category")["Profit"].sum().reset_index()
        fig = px.pie(
            profit_cat,
            names="Category",
            values="Profit",
            title="Profit Distribution by Category",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Sub-category analysis with treemap
    st.markdown("<div class='section-header'>📚 Sub-Category Performance</div>", unsafe_allow_html=True)
    
    treemap_data = filtered_data.groupby(["Category", "Sub-Category"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Profit Margin": "mean"
    }).reset_index()
    
    view_option = st.radio(
        "View Sub-Categories by:",
        ["Sales", "Profit", "Profit Margin"],
        horizontal=True
    )
    
    if view_option == "Sales":
        fig = px.treemap(
            treemap_data,
            path=["Category", "Sub-Category"],
            values="Sales",
            color="Sales",
            color_continuous_scale="Blues",
            title="Sub-Category Sales (Size: Sales, Color: Sales)"
        )
    elif view_option == "Profit":
        fig = px.treemap(
            treemap_data,
            path=["Category", "Sub-Category"],
            values="Sales",
            color="Profit",
            color_continuous_scale="RdYlGn",
            title="Sub-Category Performance (Size: Sales, Color: Profit)"
        )
    else:
        fig = px.treemap(
            treemap_data,
            path=["Category", "Sub-Category"],
            values="Sales",
            color="Profit Margin",
            color_continuous_scale="RdYlGn",
            title="Sub-Category Performance (Size: Sales, Color: Profit Margin)"
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top/Bottom products
    st.markdown("<div class='section-header'>🏆 Top/Bottom Performing Products</div>", unsafe_allow_html=True)
    
    product_data = filtered_data.groupby("Product Name").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Order ID": "nunique"
    }).reset_index()
    
    top_bottom_col1, top_bottom_col2 = st.columns(2)
    
    with top_bottom_col1:
        num_products = st.slider("Number of products to show:", 5, 20, 10)
        sort_by = st.selectbox("Sort products by:", ["Sales", "Profit", "Quantity", "Order ID"])
        
        top_products = product_data.sort_values(by=sort_by, ascending=False).head(num_products)
        fig = px.bar(
            top_products,
            x="Product Name",
            y=sort_by,
            title=f"Top {num_products} Products by {sort_by}",
            color=sort_by,
            color_continuous_scale="Teal"
        )
        fig.update_layout(xaxis_title="Product", yaxis_title=sort_by, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with top_bottom_col2:
        bottom_products = product_data.sort_values(by=sort_by, ascending=True).head(num_products)
        fig = px.bar(
            bottom_products,
            x="Product Name",
            y=sort_by,
            title=f"Bottom {num_products} Products by {sort_by}",
            color=sort_by,
            color_continuous_scale="Peach"
        )
        fig.update_layout(xaxis_title="Product", yaxis_title=sort_by, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # Customer segment analysis
    st.markdown("<div class='section-header'>👥 Customer Segment Analysis</div>", unsafe_allow_html=True)
    
    seg_data = filtered_data.groupby("Segment").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Customer ID": "nunique",
        "Order ID": "nunique"
    }).reset_index()
    
    seg_data["Avg. Order Value"] = seg_data["Sales"] / seg_data["Order ID"]
    seg_data["Profit per Customer"] = seg_data["Profit"] / seg_data["Customer ID"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            seg_data,
            x="Segment",
            y=["Sales", "Profit"],
            barmode="group",
            title="Sales & Profit by Segment",
            color_discrete_sequence=["#4e73df", "#1cc88a"]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            seg_data,
            x="Segment",
            y="Avg. Order Value",
            title="Average Order Value by Segment",
            color="Avg. Order Value",
            color_continuous_scale="Purples"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Customer ranking
    st.markdown("<div class='section-header'>🏅 Top Customers</div>", unsafe_allow_html=True)
    
    customer_data = filtered_data.groupby(["Customer ID", "Customer Name"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique",
        "Profit Margin": "mean"
    }).reset_index()
    
    customer_data["Avg. Order Value"] = customer_data["Sales"] / customer_data["Order ID"]
    
    num_customers = st.slider("Number of customers to show:", 5, 20, 10, key="customer_slider")
    sort_customers_by = st.selectbox("Sort customers by:", ["Sales", "Profit", "Order ID", "Avg. Order Value"])
    
    top_customers = customer_data.sort_values(by=sort_customers_by, ascending=False).head(num_customers)
    
    fig = go.Figure(data=[
        go.Bar(name='Sales', x=top_customers['Customer Name'], y=top_customers['Sales'], marker_color='#4e73df'),
        go.Bar(name='Profit', x=top_customers['Customer Name'], y=top_customers['Profit'], marker_color='#1cc88a')
    ])
    
    fig.update_layout(
        barmode='group',
        title=f'Top {num_customers} Customers by {sort_customers_by}',
        xaxis_tickangle=-45,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # Geographic analysis
    st.markdown("<div class='section-header'>🗺️ Geographic Performance</div>", unsafe_allow_html=True)
    
    geo_data = filtered_data.groupby(["Region", "State"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique"
    }).reset_index()
    
    # Choropleth map
    st.markdown("#### 🌎 Sales by State")
    
    fig = px.choropleth(
        geo_data,
        locations="State",
        locationmode="USA-states",
        color="Sales",
        scope="usa",
        color_continuous_scale="Blues",
        hover_name="State",
        hover_data=["Sales", "Profit", "Order ID"],
        title="Sales Distribution by State"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Region analysis
    st.markdown("<div class='section-header'>📍 Regional Performance</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            geo_data.groupby("Region")["Sales"].sum().reset_index(),
            x="Region",
            y="Sales",
            title="Total Sales by Region",
            color="Sales",
            color_continuous_scale="Purples"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            geo_data.groupby("Region")["Profit"].sum().reset_index(),
            x="Region",
            y="Profit",
            title="Total Profit by Region",
            color="Profit",
            color_continuous_scale="RdYlGn"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # City-level analysis
    st.markdown("<div class='section-header'>🏙️ City Performance</div>", unsafe_allow_html=True)
    
    city_data = filtered_data.groupby(["Region", "State", "City"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique"
    }).reset_index()
    
    num_cities = st.slider("Number of cities to show:", 5, 20, 10, key="city_slider")
    sort_cities_by = st.selectbox("Sort cities by:", ["Sales", "Profit", "Order ID"])
    
    top_cities = city_data.sort_values(by=sort_cities_by, ascending=False).head(num_cities)
    
    fig = px.bar(
        top_cities,
        x="City",
        y=sort_cities_by,
        color="Region",
        title=f"Top {num_cities} Cities by {sort_cities_by}",
        hover_data=["State", "Sales", "Profit"]
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Shipping analysis in an expander
with st.expander("🚚 Shipping Performance Analysis", expanded=False):
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    ship_data = filtered_data.copy()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Shipping mode distribution
        ship_mode_dist = ship_data["Ship Mode"].value_counts().reset_index()
        fig = px.pie(
            ship_mode_dist,
            names="Ship Mode",
            values="count",
            title="Shipping Mode Distribution",
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Processing time by ship mode
        processing_time = ship_data.groupby("Ship Mode")["Processing Time"].mean().reset_index()
        fig = px.bar(
            processing_time,
            x="Ship Mode",
            y="Processing Time",
            title="Average Processing Time by Shipping Mode (Days)",
            color="Processing Time",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Shipping mode performance
    ship_perf = ship_data.groupby("Ship Mode").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique",
        "Profit Margin": "mean"
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=ship_perf["Ship Mode"],
        y=ship_perf["Sales"],
        name="Sales",
        marker_color="#4e73df"
    ))
    
    fig.add_trace(go.Bar(
        x=ship_perf["Ship Mode"],
        y=ship_perf["Profit"],
        name="Profit",
        marker_color="#1cc88a"
    ))
    
    fig.update_layout(
        barmode="group",
        title="Sales & Profit by Shipping Mode",
        xaxis_title="Shipping Mode",
        yaxis_title="Amount ($)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Profitability analysis in an expander
with st.expander("💰 Advanced Profitability Analysis", expanded=False):
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # Profit margin distribution
    st.markdown("#### 📊 Profit Margin Distribution")
    
    fig = px.histogram(
        filtered_data,
        x="Profit Margin",
        nbins=50,
        title="Distribution of Profit Margins",
        color_discrete_sequence=["#1cc88a"]
    )
    
    fig.add_vline(
        x=0,
        line_dash="dash",
        line_color="red",
        annotation_text="Break-even",
        annotation_position="top right"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Profitability by product
    st.markdown("#### 📦 Product Profitability Analysis")
    
    profitability_data = filtered_data.groupby("Product Name").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Profit Margin": "mean",
        "Quantity": "sum"
    }).reset_index()
    
    profitability_data["Profit per Unit"] = profitability_data["Profit"] / profitability_data["Quantity"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            profitability_data,
            x="Sales",
            y="Profit",
            color="Profit Margin",
            size="Quantity",
            hover_name="Product Name",
            title="Sales vs. Profit Bubble Chart",
            color_continuous_scale="RdYlGn",
            labels={
                "Sales": "Total Sales ($)",
                "Profit": "Total Profit ($)",
                "Profit Margin": "Avg. Profit Margin (%)",
                "Quantity": "Units Sold"
            }
        )
        
        # Add reference lines
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.add_vline(x=0, line_dash="dash", line_color="red")
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            profitability_data,
            x="Quantity",
            y="Profit per Unit",
            color="Profit Margin",
            size="Sales",
            hover_name="Product Name",
            title="Volume vs. Unit Profit",
            color_continuous_scale="RdYlGn",
            labels={
                "Quantity": "Units Sold",
                "Profit per Unit": "Profit per Unit ($)",
                "Profit Margin": "Avg. Profit Margin (%)",
                "Sales": "Total Sales ($)"
            }
        )
        
        # Add reference line
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Raw data explorer with enhanced features
with st.expander("🔍 Advanced Data Explorer", expanded=False):
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # Data preview with filters
    st.markdown("#### 🗃️ Filtered Data Preview")
    
    # Let users select columns to display
    all_columns = filtered_data.columns.tolist()
    default_cols = ["Order Date", "Customer Name", "Category", "Sub-Category", "Sales", "Profit", "Quantity"]
    selected_cols = st.multiselect("Select columns to display:", all_columns, default=default_cols)
    
    if selected_cols:
        st.dataframe(filtered_data[selected_cols], use_container_width=True)
    else:
        st.warning("Please select at least one column to display.")
    
    # Data statistics
    st.markdown("#### 📈 Descriptive Statistics")
    st.dataframe(filtered_data.describe(), use_container_width=True)
    
    # Correlation matrix
    st.markdown("#### 🔗 Correlation Matrix")
    
    numeric_cols = filtered_data.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 1:
        corr_matrix = filtered_data[numeric_cols].corr()
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            color_continuous_scale="RdYlGn",
            zmin=-1,
            zmax=1,
            title="Correlation Between Numeric Variables"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Not enough numeric columns to calculate correlations.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with more information
st.markdown("---")
st.markdown("""
    <div style='text-align:center; color:gray; padding:20px;'>
        <p>✨ <strong>Superstore Analytics Pro Dashboard</strong> ✨</p>
        <p>Built with Streamlit, Plotly, and Pandas | © 2025 Retail Analytics Inc.</p>
        <p style='font-size:12px;'>Last updated: {}</p>
    </div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)