import weio # install from https://github.com/ebranlard/weio
import matplotlib 
import matplotlib.pyplot as plt

# Font size
matplotlib.rcParams['font.size'] = 14

# Reading data and converting to a pandas DataFrame (table)
df = weio.read('../weio/tests/example_files/FASTOutBin.outb').toDataFrame()
print('Available columns:', df.columns)

# Creating figure, setting figure size, and spacing/margins
fig,ax = plt.subplots(1, 1, sharey=False, figsize=(6.4,4.8))
fig.subplots_adjust(left=0.12, right=0.95, top=0.95, bottom=0.11, hspace=0.20, wspace=0.20)

# Plotting with different styling and legend labels
ax.plot(df['Time_[s]'], df['RtAeroCp_[-]'], '-'  , color='k'          , marker='' , markersize=6, label='Cp')
ax.plot(df['Time_[s]'], df['RtAeroCt_[-]'], '--' , color=[0.3,0.5,0.7], marker='.', markersize=6, label='Ct')

# Axis and legend
ax.set_xlabel('Time [s]')
ax.set_ylabel(r'$C_p$ and $C_t$ [-]')
ax.set_xlim([0,0.3])
ax.set_ylim([0,1])
ax.legend(loc='upper right')
ax.tick_params(direction='in')

# Exporting figure
fig.savefig('MyFigure.png')
fig.savefig('MyFigure.pdf')

# Show figure to screen
plt.show()
