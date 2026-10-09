import pandas as pd
import plotly.graph_objects as go


def create_burndown_chart(df):

    chart_df = df.copy()

    chart_df["Due date"] = pd.to_datetime(
        chart_df["Due date"],
        errors="coerce"
    )

    chart_df = chart_df.dropna(
        subset=["Due date"]
    )

    picked_df = (
        chart_df.groupby("Due date")
        .size()
        .reset_index(name="Stories Picked")
        .sort_values("Due date")
    )

    total_stories = picked_df[
        "Stories Picked"
    ].sum()

    picked_df["Stories Left"] = (
        total_stories
        - picked_df["Stories Picked"].cumsum()
        + picked_df["Stories Picked"]
    )

    picked_df["Display Date"] = (
        picked_df["Due date"]
        .dt.strftime("%d-%b")
    )

    fig = go.Figure()

    # Plan for Dev Completion (Bars)

    fig.add_trace(
        go.Bar(
            x=picked_df["Display Date"],
            y=picked_df["Stories Picked"],
            name="Plan for Dev Completion",
            marker_color="#C05020",
            text=picked_df["Stories Picked"],
            textposition="outside",
            width=0.18
        )
    )

    # Pending Story (Line)

    fig.add_trace(
        go.Scatter(
            x=picked_df["Display Date"],
            y=picked_df["Stories Left"],
            name="Pending Story",
            mode="lines+markers+text",
            text=picked_df["Stories Left"],
            textposition="top center",
            line=dict(
                color="#1F4E79",
                width=3
            ),
            marker=dict(
                size=8
            )
        )
    )

    fig.update_layout(

        title=dict(
            text="Burn Down Chart",
            x=0.5,
            xanchor="center",
            font=dict(
                size=24,
                color="black"
            )
        ),

        paper_bgcolor="white",
        plot_bgcolor="white",

        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),

        height=420,

        bargap=0.7,

        margin=dict(
            l=40,
            r=40,
            t=60,
            b=60
        ),

        legend=dict(
            orientation="h",
            y=-0.15,
            x=0.25,
            font=dict(
                color="black",
                size=12
            )
        ),

        xaxis=dict(
            title="",
            showgrid=False,
            tickfont=dict(
                size=11,
                color="black"
            )
        ),

        yaxis=dict(
            title="",
            rangemode="tozero",
            gridcolor="#D9D9D9",
            tickfont=dict(
                color="black"
            )
        )
    )

    return fig