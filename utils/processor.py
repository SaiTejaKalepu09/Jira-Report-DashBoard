import pandas as pd


def split_status(df):

    requirements_df = df[
        df["Status"].str.strip().eq("Requirements")
    ].copy()

    other_df = df[
        ~df["Status"].str.strip().eq("Requirements")
    ].copy()

    # Sort by Due Date (Oldest -> Newest)
    # Null dates at the end

    if "Due date" in other_df.columns:

        other_df["Due date"] = pd.to_datetime(
            other_df["Due date"],
            errors="coerce"
        )

        other_df = other_df.sort_values(
            by="Due date",
            ascending=True,
            na_position="last"
        )

        # Format date for display

        other_df["Due date"] = (
            other_df["Due date"]
            .dt.strftime("%d-%b-%Y")
        )

        # Convert NaT back to blank

        other_df["Due date"] = (
            other_df["Due date"]
            .fillna("")
        )

    return requirements_df, other_df