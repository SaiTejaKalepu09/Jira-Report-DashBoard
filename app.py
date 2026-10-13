import streamlit as st
import pandas as pd

from utils.processor import split_status
from utils.charts import create_burndown_chart
from utils.excel_export import create_styled_excel
from utils.report_export import create_full_report


st.set_page_config(
    page_title="Jira Dashboard",
    layout="wide"
)

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

# =====================================================
# Top Buttons
# =====================================================

button_col1, button_col2 = st.columns(2)

with button_col1:

    generate_btn = st.button(
        "🚀 Generate Report",
        type="primary",
        use_container_width=True
    )

with button_col2:

    full_report_placeholder = st.empty()

# =====================================================
# Dashboard
# =====================================================

if generate_btn:

    if dev_csv is None or defects_csv is None:

        st.error(
            "Please upload both CSV files."
        )

        st.stop()

    # =====================================================
    # Read CSV Files
    # =====================================================

    dev_df = pd.read_csv(dev_csv)

    defects_df = pd.read_csv(defects_csv)

    st.success(
        "Files uploaded successfully!"
    )

    st.markdown("---")

    # =====================================================
    # Burn Down Chart
    # =====================================================

    st.subheader("Burn Down Chart")

    burn_down_fig = create_burndown_chart(
        dev_df
    )

    st.plotly_chart(
        burn_down_fig,
        use_container_width=False,
        config={
            "displayModeBar": "hover"
        }
    )

    # =====================================================
    # Generate PNG
    # =====================================================

    try:

        chart_png = burn_down_fig.to_image(
            format="png"
        )

    except Exception as e:

        st.error(
            f"PNG Generation Error:\n\n{e}"
        )

        st.stop()

    st.markdown("---")

    # =====================================================
    # Process Defects CSV
    # =====================================================

    requirements_df, other_df = split_status(
        defects_df
    )

    other_df = other_df.drop(
        columns=["Issue id"],
        errors="ignore"
    )

    desired_order = [
        "Issue key",
        "Summary",
        "Status",
        "Due date"
    ]

    existing_columns = [
        col
        for col in desired_order
        if col in other_df.columns
    ]

    other_df = other_df[
        existing_columns
    ]

    # =====================================================
    # Requirements
    # =====================================================

    st.subheader("Requirements")

    if not requirements_df.empty:

        display_columns = [

            col

            for col in [
                "Issue key",
                "Summary",
                "Status"
            ]

            if col in requirements_df.columns

        ]

        requirements_display_df = (
            requirements_df[
                display_columns
            ]
        )

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

        st.info(
            "No Requirement records found."
        )

        requirements_display_df = pd.DataFrame()

    st.markdown("---")

    # =====================================================
    # Other Statuses
    # =====================================================

    st.subheader(
        "Development / Other Statuses"
    )

    st.metric(
        "Total Non-Requirement Stories",
        len(other_df)
    )

    st.dataframe(
        other_df,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # Full Report Generation
    # =====================================================

    full_report = create_full_report(
        chart_png,
        requirements_display_df,
        other_df
    )

    full_report_placeholder.download_button(
        label="📊 Download Full Report",
        data=full_report,
        file_name="jira_daily_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    st.markdown("---")

    # =====================================================
    # Raw Data
    # =====================================================

    with st.expander(
        "Current Dev Stories Data"
    ):

        st.dataframe(
            dev_df,
            use_container_width=True
        )

    with st.expander(
        "Open US Defects Data"
    ):

        st.dataframe(
            defects_df,
            use_container_width=True
        )