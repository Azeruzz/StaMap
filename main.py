from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from pyecharts.charts import Map
from pyecharts import options as opts

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def create_china_map():
    df = pd.read_excel("data.xlsx")
    df = df.dropna()
    data_list = list(zip(df['省份'], df['数值']))

    china_map = (
        Map(init_opts=opts.InitOpts(width="1200px", height="900px", renderer="svg"))
        .add(
            "",
            data_list,
            "china",
            is_map_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False)
        )
        .set_global_opts(

            tooltip_opts=opts.TooltipOpts(is_show=False),
            legend_opts=opts.LegendOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,
                pieces=[
                    {"min": 200, "label": "≥200", "color": "#800026"},
                    {"min": 151, "max": 200, "label": "151-200", "color": "#BD0026"},
                    {"min": 101, "max": 150, "label": "101-150", "color": "#E31A1C"},
                    {"min": 51, "max": 100, "label": "51-100", "color": "#FC4E2A"},
                    {"min": 10, "max": 50, "label": "10-50", "color": "#FD8D3C"},
                    {"min": 1, "max": 9, "label": "<10", "color": "#FEB24C"},
                    {"max": 0, "label": "null", "color": "#000000"}
                ],
                textstyle_opts=opts.TextStyleOpts(
                    font_size=18,
                    font_family="Times New Roman"
                ),
                item_width=30,
                item_height=20,
                orient="horizontal", 
                pos_bottom="20px",
                pos_left="center"
            ),

        graphic_opts=[
                opts.GraphicGroup(
                    graphic_item=opts.GraphicItem(left="center", bottom=10),
                    children=[
                        opts.GraphicText(
                            graphic_item=opts.GraphicItem(left="center", bottom=30)
                        ),
                        opts.GraphicText(
                            graphic_item=opts.GraphicItem(left="center", bottom=10)
                        )
                    ]
                )
            ]
        )
    )

    return china_map.render_embed()

@app.get("/", response_class=HTMLResponse)
async def show_map(request: Request):
    chart_html = create_china_map()
    return templates.TemplateResponse("map.html", {"request": request, "chart": chart_html})
