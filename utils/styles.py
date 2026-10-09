def style_table(df):

    return (
        df.style
        .set_properties(
            **{
                "border": "1px solid black",
                "text-align": "left",
                "font-size": "12px",
                "background-color": "#4F81BD",
                "color": "white"
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#1F4E79"),
                        ("color", "white"),
                        ("border", "1px solid black"),
                        ("font-weight", "bold"),
                        ("text-align", "center"),
                        ("font-size", "13px")
                    ]
                },
                {
                    "selector": "td",
                    "props": [
                        ("background-color", "#4F81BD"),
                        ("color", "white"),
                        ("border", "1px solid black")
                    ]
                }
            ]
        )
    )