# Well Log Plot
This library was created to plot well log data by bokeh. The main advantage of bokeh is linked brushing. Linked brushing connects multiple plots in such a way that when points in one plot is highlighted, then corresponding points in the other plots also get highlighted.

The way to apply this library first download the library.
Convert the well data to pandas dataframe. THe dataframe is considered to be stored in the variable df.\n

from WellLogPlot import WellPlot
from bokeh.models import ColumnDataSource, BoxSelectTool, LassoSelectTool, CDSView, IndexFilter, BooleanFilter
from bokeh.plotting import figure, show, output_file, save
from bokeh.layouts import layout

What are the different logs in each plot of the well log plot that need to be defined.
plot_1={'logs':['GR_COR','SP','BS','CALI'],
        'x_rang':[[0,150],[0,10],[6,16],[6,16]],
        'colour_list':['black','blue','green','red'],
        'unit_list':['API','mV','IN','IN'],
        'fill':None,
        'fill_logs':None,
        'fill_colour':None}
plot_2={'logs':['NPHI_COR','RHO_COR'],
        'x_rang':[[0.54,-0.06],[1.75,2.75]],
        'colour_list':['red','blue'],
        'unit_list':['V/V','gm/cc'],
        'fill':'yes',
        'fill_logs':[['NPHI_COR','RHO_COR']],
        'fill_colour':[['purple','yellow']]}

tool='lasso_select'
source=ColumnDataSource(data=dirok_3_well)
plot=WellPlot(source=source)
well_plots=plot.complete_plot(well_cpi=[plot_1,plot_2],tool=tool,y_rang=[df['DEPTH'].max(),df['DEPTH'].min()],heit=1000,n_cols=2)
show(layout([well_cpi_total],sizing_mode='fixed'))

This will give you the well log plot.
