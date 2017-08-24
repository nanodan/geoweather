import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

def temperature_plot(
    x,y,counts,stdev=None,real_y=None,realmax=None,realmin=None,
    plot_label='Measured Temperature',compare_label="Air Temperature",
    cmap_label='# of Distinct Hardware IDs',max_label='Daily Max (Air)',
    min_label='Daily Min (Air)',xlabel='Hour',
    ylabel_left='Temperature ($^\circ$C)',
    ylabel_right='Temperature ($^\circ$F)',title='',switch_y=False,xlim=[0,23],
    stdev_label='Standard Deviation'
    ):
    """Generate a temperature plot comparing real vs. measured with bounds
    
    x, y, and counts are required, all other keyword arguments are optional.
    
    Example usage:
        y = np.array(df['Temperature'])
        real_y = np.array(df_real['Temperature'])
        x = np.array(df['Hour'])
        stdev = np.array(df['Stdev'])
        realmax = 30
        realmin = 15
        counts = np.array(df['DistinctIds'])
        temperature_plot(
            x=x,y=y,counts=counts,stdev=stdev,real_y=real_y,
            realmax=realmax,realmin=realmin
            )
    """
    
    # Default is celcius left axis, and fahrenheit on right: switch_y swaps this
    if switch_y:
        temp = ylabel_right
        ylabel_right = ylabel_left
        ylabel_left = temp
        
    if stdev is not None:
        ydevup = y + stdev
        ydevdown = y - stdev
    if realmax is not None and realmin is not None:
        realmax_list = realmax*np.ones(len(x))
        realmin_list = realmin*np.ones(len(x))
    
    fig, ax = plt.subplots(ncols=1,figsize=(30,5))
    
    try:
        # If including stdev, plot upper and lower bounds
        ax.plot(x,ydevup,'g--',linewidth=1,zorder=3,label=stdev_label)
        ax.plot(x,ydevdown,'g--',linewidth=1,zorder=3)
    except NameError:
        pass
    
    # Add a scatterplot of the count values (may be optional in future release)
    sc = ax.scatter(x,y,s=300,c=counts,cmap='plasma',zorder=3,label=cmap_label)
    
    # Plot the measured temperature data
    ax.plot(x,y,'k',zorder=1,label=plot_label)
    
    # If comparing to "real" data, add a dashed comparison and bounds
    if real_y is not None:
        ax.plot(x,real_y,'k--',zorder=1,label=compare_label)
    try:
        ax.plot(x,realmax_list,'r',zorder=1,alpha=0.5,label=max_label)
        ax.plot(x,realmin_list,'b',zorder=1,alpha=0.5,label=min_label)
    except NameError:
        pass
    
    # Figure labels and properties
    ax.set_xlabel(xlabel,fontsize=14)
    axlab = ax.set_ylabel(ylabel_left,fontsize=14)
    ax.set_title(title,fontsize=16,fontweight='bold')
    cb = fig.colorbar(sc)
    cb.set_label(cmap_label)
    ax.set_xlim(xlim)
    loc = plticker.MultipleLocator(base=1.0)
    ax.xaxis.set_major_locator(loc)
    ax2 = ax.twinx()
    setax2 = ax2.set_ylim(ax.get_ylim())
    ax2.grid(None)
    
    # Do the celcius to fahrenheit conversion (future release will alow F input)
    if not switch_y:
        adjust_second_ax = ax2.set_ylim([ax.get_ylim()[0]/0.5556+32,ax.get_ylim()[1]/0.5556+32])
    else:
        adjust_second_ax = ax2.set_ylim([(ax.get_ylim()[0]-32)*0.5556,(ax.get_ylim()[1]-32)*0.5556])
    
    ax2lab = ax2.set_ylabel(ylabel_right)
    
    # Add legend
    lg = ax.legend(loc='best',bbox_to_anchor=(1.235,0.95))
    
def geohash_to_polygon(df=None,mag_col_name=None,fileout_json=None,fileout_csv=None):
  if df is not None and mag_col_name is not None and fileout_json is not None and fileout_csv is not None:
    polygons_out = {'type':'FeatureCollection','features':[]}
    for index, row in df.iterrows():
      sw_lon = row['sw_lon']
      sw_lat = row['sw_lat']
      se_lat = row['se_lat']
      se_lon = row['se_lon']
      ne_lat = row['ne_lat']
      ne_lon = row['ne_lon']
      nw_lat = row['nw_lat']
      nw_lon = row['nw_lon']
      poly_points = [[sw_lon,sw_lat],[se_lon,se_lat],[ne_lon,ne_lat],[nw_lon,nw_lat]]
      feature = {'type':'Feature',
                 'properties':{'Temperature': row['AvgTemp']},
                 'id':index,
                 'geometry':{'type':'Polygon',
                             'coordinates':[poly_points]}}
      polygons_out['features'].append(feature)


    geojson = json.dumps(polygons_out)
    f = open(fileout_json,'w')
    f.write(geojson)
    f.close()

    magnitudes = pd.DataFrame(df[mag_col_name])
    magnitudes.to_csv(fileout_csv,index_label='id')
  else:
    return 'Error: Must pass all parameters to function'