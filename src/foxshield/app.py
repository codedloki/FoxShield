import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="FoxShield",
    page_icon="🦊",
    layout="wide"
)

# 2. Native Logo Placement (This forces logo to the VERY TOP of sidebar)
st.logo(
    image="https://img.icons8.com/color/96/fox.png",
    size="large",          # Sidebar मध्ये logo मोठा आणि स्पष्ट दिसेल
    icon_image="🦊"        # Sidebar बंद (collapsed) असताना फक्त Fox emoji दिसेल
)

# 3. Define your pages using st.Page
home_page = st.Page(
    page="pages/1_home.py",
    title="Home",
    icon="🏠",
    default=True,  # Sets the initial page
)

scanner_page = st.Page(
    page="pages/2_scan.py",
    title="Scan",
    icon="🔍"
)

about_page = st.Page(
    page="pages/3_about.py",
    title="About",
    icon="ℹ️"
)

# 4. Pass the page list to st.navigation
pg = st.navigation([home_page, scanner_page, about_page])

# 5. Run the navigation routing
pg.run()
