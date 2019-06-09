#Importing the required packages
import geopandas as gpd
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet, Select
from bokeh.plotting import figure, show, output_file
from bokeh.tile_providers import get_provider, Vendors #bokeh version 1.1
#from bokeh.tile_providers import CARTODBPOSITRON #bokeh version 1.0
from bokeh.io import curdoc
from bokeh.layouts import column, row
import math
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:ruking29@localhost:5432/se4g')
bike = pd.read_sql_table('bike',engine)



# #FIRST GRAPH


d = pd.to_datetime(bike['time']).dt.date
bike['time'] = d
bike.rename(columns={'time':'date'}, inplace=True)


stat_names = list(bike)
del stat_names[1]
options=[]

for i in stat_names:
    string = 'Station %s' %i
    options.append(string)

days = []
for i in range(1,32):
    days.append(str(i))
    
months = []
for i in range(1,13):
    months.append(str(i))


curr_date = pd.to_datetime('1-1-2010')

hours = list(range(0,24))
data = ColumnDataSource({'x' : hours, 'y': list(bike[bike["date"] == curr_date.date()]['1'])})

#Create the Line plot 
p = figure(title='Daily # of bikes in the station ', title_location='above', x_axis_label = 'Time(hours)', y_axis_label = '# of bikes', x_range=(1, 24))
p.vbar(x='x', top='y', source=data, width=0.6, color='red')
#p.circle(x = 'x', y = 'y', source=data, color = 'black', size = 10, alpha = 0.8)
p.title.text_color = 'black'
p.title.text_font_size = '15pt'

#Create Select Widget
select_widget_1 = Select(options = options, value = options[1], 
                title = 'Select a station')
select_widget_2 = Select(options =["January", "February", "March", "April", "May", "June", "July", "August","September", "October", "November", "December"], value = months[0], title = 'Select a month')
select_widget_3 = Select(options = days, value = days[0], title = 'Select a day')

def callback(attr, old, new):
    column2plot = select_widget_1.value
    day2plot = select_widget_3.value
    month2plot = select_widget_2.value
    date2plot = pd.to_datetime('2010-'+str(month2plot)+'-'+str(day2plot))
    if len(column2plot) == 9:
        data.data = {'x' : hours, 'y': list(bike[bike["date"] == date2plot.date()][str(column2plot[-1])])}
    elif len(column2plot) == 10:
        data.data = {'x' : hours, 'y': list(bike[bike["date"] == date2plot.date()][str(column2plot[-2]+column2plot[-1])])}
    p.vbar(x='x', top='y', source = data, width=0.6, color='red') 

#Update Select Widget to each interaction
select_widget_1.on_change('value', callback)
select_widget_2.on_change('value', callback)
select_widget_3.on_change('value', callback)








layout = column(row(column(select_widget_1, select_widget_2, select_widget_3), p))
#Output the plot
output_file("graph.html")
show(layout)
curdoc().add_root(layout)#Importing the required packages
