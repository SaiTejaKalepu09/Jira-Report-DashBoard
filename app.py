import streamlit as st
import pandas as pd

from utils.processor import split_status
from utils.charts import create_burndown_chart
from utils.excel_export import create_styled_excel

st.set_page_config(
    page_title="Jira Dashboard",
    layout="wide"
)

# =====================================================
# Session State
# =====================================================

if "report_ready" not in st.session_state:
    st.session_state.report_ready = False

st.title("Jira Automation Dashboard")
st.markdown("### Upload Jira CSV Files")

# =====================================================
# Upload Section
# =====================================================

col1, col2 = st.columns(2)

with col1:
    dev_csv = st.file_uploader(
        "Upload Current Dev Stories CSV",
        type=["csv"]
    )

with col2:
    defects_csv = st.file_uploader(
        "Upload Open US Defects CSV",
        type=["csv"]
    )

button_col1, button_col2, button_col3= st.columns(3)

with button_col1:
    generate_btn = st.button(
        "🚀 Generate Report",
        type="primary",
        use_container_width=True
    )

with button_col2:
    requirements_placeholder = st.empty()

with button_col3:
    other_placeholder = st.empty()

# =====================================================
# Generate Report
# =====================================================

if generate_btn:

    if dev_csv is None or defects_csv is None:
        st.error("Please upload both CSV files.")
        st.stop()

    dev_df = pd.read_csv(dev_csv)
    defects_df = pd.read_csv(defects_csv)

    burn_down_fig = create_burndown_chart(dev_df)

    chart_png = None
    try:
        chart_png = burn_down_fig.to_image(format="png")
    except Exception as e:
        pass

    requirements_df, other_df = split_status(defects_df)

    if not requirements_df.empty:

        display_columns = [
            col for col in [
                "Issue key",
                "Summary",
                "Status"
            ]
            if col in requirements_df.columns
        ]

        requirements_display_df = (
            requirements_df[display_columns]
        )

        requirements_excel = create_styled_excel(
            requirements_display_df,
            "Requirements"
        )

    else:

        requirements_display_df = pd.DataFrame()
        requirements_excel = None

    other_df = other_df.drop(
        columns=["Issue id"],
        errors="ignore"
    )

    other_excel = create_styled_excel(
        other_df,
        "Other_Statuses"
    )

    # Save everything

    st.session_state.dev_df = dev_df
    st.session_state.defects_df = defects_df

    st.session_state.burn_down_fig = burn_down_fig
    st.session_state.chart_png = chart_png

    st.session_state.requirements_display_df = requirements_display_df
    st.session_state.other_df = other_df

    st.session_state.requirements_excel = requirements_excel
    st.session_state.other_excel = other_excel

    st.session_state.report_ready = True

# =====================================================
# Dashboard Display
# =====================================================

if st.session_state.report_ready:

    dev_df = st.session_state.dev_df
    defects_df = st.session_state.defects_df

    burn_down_fig = st.session_state.burn_down_fig

    requirements_display_df = (
        st.session_state.requirements_display_df
    )

    other_df = st.session_state.other_df

    st.success("Files uploaded successfully!")

    # =====================================================
    # Download Buttons
    # =====================================================

    if st.session_state.requirements_excel is not None:

        requirements_placeholder.download_button(
            label="📥 Requirements",
            data=st.session_state.requirements_excel,
            file_name="requirements.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            on_click="ignore"
        )

    other_placeholder.download_button(
        label="📥 Other Statuses",
        data=st.session_state.other_excel,
        file_name="other_statuses.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        on_click="ignore"
    )
    for _ in range(4):
        st.write("")
    st.markdown("---")
    # Push chart below first fold
    for _ in range(4):
        st.write("")

    # =====================================================
    # Burn Down Chart
    # =====================================================

    st.subheader("📈 Burn Down Chart")

    st.plotly_chart(
        burn_down_fig,
        use_container_width=False,
        config={
            "displayModeBar": "hover"
        }
    )

    st.markdown("---")

    # =====================================================
    # Requirements
    # =====================================================

    st.subheader("📋 Requirements")

    if not requirements_display_df.empty:

        st.metric(
            "Total Requirement Stories",
            len(requirements_display_df)
        )

        st.dataframe(
            requirements_display_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No Requirement records found.")

    st.markdown("---")

    # =====================================================
    # Other Statuses
    # =====================================================

    st.subheader("🛠 Development / Other Statuses")

    st.metric(
        "Total Non-Requirement Stories",
        len(other_df)
    )

    st.dataframe(
        other_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # =====================================================
    # Raw Data
    # =====================================================

    with st.expander("Current Dev Stories Data"):

        st.dataframe(
            dev_df,
            use_container_width=True
        )

    with st.expander("Open US Defects Data"):

        st.dataframe(
            defects_df,
            use_container_width=True
        )