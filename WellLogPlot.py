from bokeh.models import LinearAxis, Range1d, LogAxis, LogScale, LinearColorMapper, LogColorMapper, ColorBar, VArea, HArea, DataRange1d, Patches
# from bokeh.plotting import figure, show, output_file, save
from bokeh.layouts import row, gridplot, layout
from bokeh.models import ColumnDataSource, BoxSelectTool, LassoSelectTool, CDSView, IndexFilter, BooleanFilter
import bokeh.io
import bokeh.plotting

class WellLog():
    def __init__(self,well):
        self.well=well
        # well is the pandas dataframe converted from las file

    def filtered_data(self,log,minimum,maximum,sign=None):
        self.log=log
        self.minimum=minimum
        self.maximum=maximum
        self.sign=sign
        if(self.sign=='<=and<='):
            self.well_filtered=self.well[(self.well_[self.log]>=self.minimum) & (self.well[self.log]<=self.maximum)]
            return self.well_filtered # Gives the filtered dataframe
        elif(self.sign=='<and<'):
            self.well_filtered=self.well[(self.well[self.log]>self.minimum) & (self.well[self.log]<self.maximum)]
            return self.well_filtered # Gives the filtered dataframe
        elif(self.sign==None):
            return self.well  

class WellPlot():
    def __init__(self,source):
        self.source=source
    def scaled_value(self,log_value,log_value_range_min,log_value_range_max,t_value_min_range,t_value_max_range):
        self.log_value=log_value
        self.log_value_range_min=log_value_range_min
        self.log_value_range_max=log_value_range_max
        self.t_value_min_range=t_value_min_range
        self.t_value_max_range=t_value_max_range
        self.s_value=self.t_value_min_range+((self.log_value-self.log_value_range_min)*
                                             (self.t_value_max_range-self.t_value_min_range)/(self.log_value_range_max-self.log_value_range_min))
        # self.s_value=(self.n_value*(self.t_value_max_range-self.t_value_min_range))+self.log_value.min()
        # return self.s_value, self.log_value, self.t_value_min_range, self.t_value_max_range, self.n_value
        return self.s_value
        
    def overlay_plot(self,tool,logs,x_rang,y_rang,colour_list,unit_list,n_cols,heit,fill=None,fill_logs=None,fill_colour=None):
        self.tool=tool
        self.logs=logs
        self.x_rang=x_rang
        self.y_rang=y_rang
        self.colour_list=colour_list
        self.unit_list=unit_list
        self.n_cols=n_cols
        self.heit=heit
        self.fill=fill
        self.fill_logs=fill_logs
        self.fill_colour=fill_colour
        
        
        if(self.logs[0]=='RT' or self.logs[0]=='RXO'):
            self.plot=figure(tools=self.tool,x_range=tuple(self.x_rang[0]),y_range=tuple(self.y_rang),x_axis_location='above',
                             width=int(1272/self.n_cols),height=self.heit,x_axis_type='log')
        else:
            self.plot=bokeh.plotting.figure(tools=self.tool,x_range=tuple(self.x_rang[0]),y_range=tuple(self.y_rang),x_axis_location='above',
                             width=int(1272/self.n_cols),height=self.heit)
        
        self.plot.line(x=self.logs[0],y='DEPTH',source=self.source,color=self.colour_list[0],line_width=2)
        self.plot.xaxis.axis_label=self.logs[0]+'\n'+self.unit_list[0]
        self.plot.xaxis.axis_label_text_color=self.colour_list[0]
        self.plot.xaxis.major_label_text_color=self.colour_list[0]
        self.plot.xaxis.major_tick_line_color=self.colour_list[0]
        self.plot.xaxis.minor_tick_line_color=self.colour_list[0]
        self.plot.xaxis.axis_line_color=self.colour_list[0]

        self.plot.yaxis.axis_label='Depth in meter'
        self.plot.yaxis.axis_label_text_color=self.colour_list[0]
        self.plot.yaxis.major_label_text_color=self.colour_list[0]
        self.plot.yaxis.major_tick_line_color=self.colour_list[0]
        self.plot.yaxis.minor_tick_line_color=self.colour_list[0]
        self.plot.yaxis.axis_line_color=self.colour_list[0]

        

        for i in range(1,len(self.logs)):
            self.plot.extra_x_ranges[self.logs[i]]=Range1d(self.x_rang[i][0],self.x_rang[i][1])
            self.plot.line(x=self.logs[i],y='DEPTH',source=self.source,color=self.colour_list[i],x_range_name=self.logs[i],line_width=2)
            if(self.logs[i]=='RT' or self.logs[i]=='RXO'):
                self.ax=LogAxis(x_range_name=self.logs[i],axis_label=self.logs[i]+'\n'+self.unit_list[i])
            else:
                self.ax=LinearAxis(x_range_name=self.logs[i],axis_label=self.logs[i]+'\n'+self.unit_list[i])
            self.ax.axis_label_text_color=self.colour_list[i]
            self.ax.axis_line_color=self.colour_list[i]
            self.ax.major_label_text_color=self.colour_list[i]
            self.ax.major_tick_line_color=self.colour_list[i]
            self.ax.minor_tick_line_color=self.colour_list[i]
            self.plot.add_layout(self.ax,'above')
       
        if self.fill is not None:
            self.df_temp=pd.DataFrame(self.source.data)
            for self.j_1 in range(len(self.fill_logs)):
                self.scaled_log=[]
                for self.j_2 in range(len(self.fill_logs[self.j_1])):
                    if(type(self.fill_logs[self.j_1][self.j_2])!=str):
                        if(self.j_2==1):
                            self.log_value=np.array([self.fill_logs[self.j_1][1]]*len(self.df_temp[self.fill_logs[self.j_1][0]]))
                            self.log_value_range_min=self.x_rang[self.logs.index(self.fill_logs[self.j_1][0])][0]
                            self.log_value_range_max=self.x_rang[self.logs.index(self.fill_logs[self.j_1][0])][1]
                            self.t_value_min_range=self.x_rang[0][0]
                            self.t_value_max_range=self.x_rang[0][1]
                            self.scaled_log.append(self.scaled_value(log_value=self.log_value,log_value_range_min=self.log_value_range_min,
                                                                     log_value_range_max=self.log_value_range_max,t_value_min_range=self.t_value_min_range,
                                                                     t_value_max_range=self.t_value_max_range))
                        elif(self.j_2==0):
                            self.log_value=np.array([self.fill_logs[self.j_1][0]]*len(self.df_temp[self.fill_logs[self.j_1][1]]))
                            self.log_value_range_min=self.x_rang[self.logs.index(self.fill_logs[self.j_1][1])][0]
                            self.log_value_range_max=self.x_rang[self.logs.index(self.fill_logs[self.j_1][1])][1]
                            self.t_value_min_range=self.x_rang[0][0]
                            self.t_value_max_range=self.x_rang[0][1]
                            self.scaled_log.append(self.scaled_value(log_value=self.log_value,log_value_range_min=self.log_value_range_min,
                                                             log_value_range_max=self.log_value_range_max,t_value_min_range=self.t_value_min_range,
                                                             t_value_max_range=self.t_value_max_range))
                    elif(self.fill_logs[self.j_1][self.j_2]==self.logs[0]):
                        self.scaled_log.append(self.df_temp[self.logs[0]])
                    else:
                        self.log_value=self.df_temp[self.fill_logs[self.j_1][self.j_2]]
                        self.log_value_range_min=self.x_rang[self.logs.index(self.fill_logs[self.j_1][self.j_2])][0]
                        self.log_value_range_max=self.x_rang[self.logs.index(self.fill_logs[self.j_1][self.j_2])][1]
                        self.t_value_min_range=self.x_rang[0][0]
                        self.t_value_max_range=self.x_rang[0][1]
                        self.scaled_log.append(self.scaled_value(log_value=self.log_value,log_value_range_min=self.log_value_range_min,
                                                                 log_value_range_max=self.log_value_range_max,t_value_min_range=self.t_value_min_range,
                                                                 t_value_max_range=self.t_value_max_range))
                
                self.fil_1=self.scaled_log[0]<self.scaled_log[1]
                self.fil_2=self.scaled_log[0]>=self.scaled_log[1]
                self.df_temp['x1_f'],self.df_temp['x2_f'],self.df_temp['x1f'],self.df_temp['x2f']=self.scaled_log[0],\
                self.scaled_log[1],self.scaled_log[0],self.scaled_log[1]
                self.df_temp.loc[self.fil_1,'x1_f']=self.df_temp.loc[self.fil_1,'x2_f']
                self.df_temp.loc[self.fil_2,'x1f']=self.df_temp.loc[self.fil_2,'x2f']
        
                self.plot.harea(x1=self.df_temp['x1_f'],x2=self.df_temp['x2_f'],y=self.df_temp['DEPTH'],fill_color=self.fill_colour[self.j_1][0],fill_alpha=0.4)
                self.plot.harea(x1=self.df_temp['x1f'],x2=self.df_temp['x2f'],y=self.df_temp['DEPTH'],fill_color=self.fill_colour[self.j_1][1],fill_alpha=0.4)
        
        self.plot.toolbar.autohide=True
        return self.plot

    def complete_plot(self,well_cpi,tool,y_rang,heit,n_cols):
        self.well_cpi=well_cpi
        self.tool=tool
        self.y_rang=y_rang
        self.heit=heit
        self.n_cols=n_cols
        self.row=[]
        for i in range(len(self.well_cpi)):
            self.well_subplot=self.well_cpi[i]
            self.row.append(self.overlay_plot(tool=self.tool,logs=self.well_subplot['logs'],x_rang=self.well_subplot['x_rang'],y_rang=self.y_rang,
                                              colour_list=self.well_subplot['colour_list'],unit_list=self.well_subplot['unit_list'],n_cols=self.n_cols,
                                              heit=self.heit,fill=self.well_subplot['fill'],fill_logs=self.well_subplot['fill_logs'],
                                              fill_colour=self.well_subplot['fill_colour']))
        return self.row