# gjrich | Dec 2024
# Palmer Penguins dashboard practice
# Primarily used for practice with github issues / merging

# make sure to install requirements.txt into your virtual environment




# Import necessary libraries
import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

from shinywidgets import render_altair
import altair as alt


# Load data set into penguins data frame
df = palmerpenguins.load_penguins()

ui.page_opts(title="Penguins dashboard", fillable=True)


with ui.sidebar(title="Filter controls"):
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
    ui.h6("Links")
    ui.a(
        "GitHub Source",
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
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )
            
            # Configure the chart specifically for web deployment
            return chart.configure_view(
                continuousWidth=400,
                continuousHeight=300
            ).interactive()

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


#ui.include_css(app_dir / "styles.css")


# Reactive.calc function to update on the fly and apply the latest filters
# See this for more info:
# https://shiny.posit.co/py/api/express/reactive.calc.html

@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
