# gjrich | Dec 2024
# Palmer Penguins dashboard practice
# Primarily used for practice with github issues / merging

# make sure to install /requirements.txt into your virtual environment
# disregard /app/requirements.txt - included for github.io altair functionality 

# Import necessary libraries
from faicons import icon_svg


from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

from shinywidgets import render_altair
import altair as alt

# Future proofing too
import seaborn as sns
from pathlib import Path



# Load data set into penguins data frame
df = palmerpenguins.load_penguins()

ui.page_opts(title="Penguin Time", fillable=True)


with ui.sidebar(title="Flipper Filters"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    
    # Pick the related Species
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    
    # Provides links to all of the related collateral
    ui.h6("Collateral")
    ui.a(
        "GitHub",
        href="https://github.com/gjrich/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://gjrich.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/gjrich/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "Source Repo + Extra Info",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Generate the desired graphs
# This formatting ensures space is evenly distributed and has no scrollbars regardless of zoom 

with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Penguin Head Count"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average Bill Length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average Bill Depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill Length & Depth - Altair")

# Swapped for Altair scatter plot
        @render_altair
        def length_depth():
            return (alt.Chart(filtered_df())
                .mark_circle()
                .encode(
                    x=alt.X('bill_length_mm:Q', title='Bill Length (mm)'),
                    y=alt.Y('bill_depth_mm:Q', title='Bill Depth (mm)'),
                    color=alt.Color('species:N', title='Species'),
                    tooltip=['species', 'bill_length_mm', 'bill_depth_mm']
                )
                .interactive()
            )


    # Table of all data / searchable
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# Including option for later css options
#ui.include_css(app_dir / "styles.css")


# Reactive.calc function to update on the fly and apply the latest filters
# See this for more info:
# https://shiny.posit.co/py/api/express/reactive.calc.html

@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df