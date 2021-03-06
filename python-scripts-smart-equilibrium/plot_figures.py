import numpy as np
import matplotlib.pyplot as plt
import os
import math
from natsort import natsorted
from scipy.spatial import distance
from numpy import linalg as la
from matplotlib import rc
"""
import matplotlib.font_manager as fm
github_url = 'https://github.com/octaviopardo/EBGaramond12/blob/master/fonts/ttf/EBGaramond-Regular.ttf'
url = github_url + '?raw=true'  # You want the actual file, not some html

import urllib3
from urllib3 import PoolManager
from tempfile import NamedTemporaryFile

manager = PoolManager(num_pools=1)
response = manager.urlopen(github_url + '?raw=true')
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()
prop = fm.FontProperties(fname=f.name)


fig, ax = plt.subplots()
ax.plot([1, 2, 3])

prop = fm.FontProperties(fname=f.name)
ax.set_title('this is a special font:\n%s' % github_url, fontproperties=prop)
ax.set_xlabel('This is the default font')

plt.show()
"""

import os
from matplotlib import font_manager as fm, rcParams
fpath = os.path.join(rcParams["datapath"], "/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Regular.ttf")
#fpath = os.path.join(rcParams["datapath"], "/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Bold.ttf")
fpath = os.path.join(rcParams["datapath"], "/home/skyas/Dropbox/TeX-Gyre-Adventor.ttf")
prop = fm.FontProperties(fname=fpath)
#prop.set_size(18)

"""
fig, ax = plt.subplots()

fname = os.path.split(fpath)[1]
ax.set_title('This is a special font: {}'.format(fname), fontproperties=prop)
ax.set_xlabel('This is the default font')
#plt.rcParams.update(prop)

plt.show()
"""

import matplotlib
#matplotlib.rcParams['font.family'] = prop.get_name()

# Say, "the default sans-serif font is COMIC SANS"
# matplotlib.rcParams['font.sans-serif'] = "Adobe Garamond Pro"
# Then, "ALWAYS use sans-serif fonts"
# matplotlib.rcParams['font.family'] = "sans-serif"

"Adobe Garamond Pro: Adobe Garamond Pro"
# Options for the figure plotting
plot_at_selected_steps = [1, 20, 2400]  # the time steps at which the results are plotted
plot_at_steps_in_paper = [1, 20, 2400]

# Auxiliary time related constants
second = 1
minute = 60
hour = 60 * minute
day = 24 * hour
year = 365 * day

# Discretisation parameters
xl = 0.0          # the x-coordinate of the left boundary
xr = 1.0          # the x-coordinate of the right boundary
nsteps = 10000    # the number of steps in the reactive transport simulation
ncells = 100      # the number of cells in the discretization
reltol = 1e-1     # relative tolerance
abstol = 1e-4     # absolute tolerance

D  = 1.0e-9       # the diffusion coefficient (in units of m2/s)
v  = 1.0/day      # the fluid pore velocity (in units of m/s)
dt = 30 * minute  # the time step (in units of s)
T = 60.0          # the temperature (in units of K)
P = 100           # the pressure (in units of Pa)
phi = 0.1         # the porosity

dirichlet = False # the parameter that defines whether Dirichlet BC must be used
smrt_solv = True  # the parameter that defines whether classic or smart
                  # EquilibriumSolver must be used

tag = "-dt-" + "{:d}".format(dt) + \
      "-ncells-" + str(ncells) + \
      "-nsteps-" + str(nsteps) + \
      "-reltol-" + "{:.{}e}".format(reltol, 1) + \
      "-abstol-" + "{:.{}e}".format(abstol, 1)

test_tag_smart = tag + "-smart"
test_tag_class = tag + "-reference"

# /results-addAqueousPhase
#folder = 'cpp-reactivetransport-old-demo/results-pitzer-full-with-skipping-1e-13-both-solvers'
#folder = 'results-with-normalization'
#folder = 'results-deltan-with-normalization'
#folder_smart   = 'cfl-0.833/results-dt-1800-ncells-100-nsteps-10000-reltol-1.0e-01-abstol-1.0e-08-smart'
#folder_class   = 'cfl-0.833/results-dt-1800-ncells-100-nsteps-10000-reltol-1.0e-01-abstol-1.0e-08-reference'
folder_smart   = 'results-dt-1800-ncells-100-nsteps-10000-reltol-1.0e-01-abstol-1.0e-07-smart'
folder_class   = 'results-dt-1800-ncells-100-nsteps-10000-reltol-1.0e-01-abstol-1.0e-07-reference'

#folder_general = "plots-" + 'results-dt-1800-ncells-100-nsteps-10000-reltol-1.0e-01-abstol-1.0e-08'
#folder_general = 'teX-gyre-adventor'
#folder_general = 'plots-cfl-0.833-garamond'
#folder_general = 'plots-results-pitzer-garamond-1.0e-07'
folder_general = 'plots-results-pitzer-adventor-1.0e-07'

os.system('mkdir -p ' + folder_general)

fillz = len(str(123))

# Indices of the loaded data to plot
indx_ph        = 0
indx_Hcation   = 1
indx_Cacation  = 2
indx_Mgcation  = 3
indx_HCO3anion = 4
indx_CO2aq     = 5
indx_calcite   = 6
indx_dolomite  = 7

# Plotting params
circ_area = 6 ** 2
# zoom = 0.5
zoom = 0.5
custom_font = { }
time_steps = np.linspace(0, nsteps, nsteps)

xcells = np.linspace(xl, xr, ncells)  # the x-coordinates of the plots

#font
# mpl.rcParams['font.family'] = 'sans-serif'
# mpl.rcParams['font.serif'] ='TeXGyreSchola'
# mpl.rcParams['font.sans-serif'] ='Fira Code'
# mpl.rcParams['font.sans-serif'] = 'Century Gothic'
# mpl.rcParams['font.size'] = 12
# mpl.rcParams['legend.fontsize'] = 'medium'
#tick label spacing and tick width
# mpl.rcParams['xtick.major.pad'] = 4
# mpl.rcParams['ytick.major.pad'] = 5
# mpl.rcParams['xtick.major.width'] = 1
# mpl.rcParams['ytick.major.width'] = 1
#legend style
# mpl.rcParams['legend.frameon'] = True
# mpl.rcParams['legend.numpoints'] = 3
#mpl.rcParams['backend'] = 'PDF'
#mpl.rcParams['savefig.dpi'] = 200

def empty_marker(color):
    return {'facecolor': 'white', 'edgecolor': color, 's': circ_area, 'zorder': 2, 'linewidths': 1.5 }

def filled_marker(color):
    return {'color': color, 's': circ_area, 'zorder': 2, 'linewidths': 1.5 }

def line_empty_marker(color):
    return {'markerfacecolor': 'white', 'markeredgecolor':color, 'markersize': 6, 'markeredgewidth': 1.5 }

def line_filled_marker(color):
    return {'color': color, 'markersize': 6, 'markeredgewidth': 1.5 }

def line(color):
    return {'linestyle': '-', 'color': color, 'zorder': 1, 'linewidth': 2}

def line_error(color):
    return {'linestyle': ':', 'marker': 'D', 'color': color, 'zorder': 1, 'linewidth': 0.5, 'markersize': 4}

def titlestr(t):
    d = int(t / day)                 # The number of days
    h = int(int(t % day) / hour)     # The number of remaining hours
    m = int(int(t % hour) / minute)  # The number of remaining minutes
    return '{:>3d}d {:>2}h {:>2}m'.format(int(d), str(int(h)).zfill(2), str(int(m)).zfill(2))

def calculate_error(tol):
    '''
    abs_error_l1_ph, error_l1_ph, norm_l1_ph = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_l1_calcite, error_l1_calcite, norm_l1_calcite = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_l1_dolomite, error_l1_dolomite, norm_l1_dolomite = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_l1_hcation, error_l1_hcation, norm_l1_hcation = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_l1_cacation, error_l1_cacation, norm_l1_cacation = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_l1_mgcation, error_l1_mgcation, norm_l1_mgcation = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_l1_hco3anion, error_l1_hco3anion, norm_l1_hco3anion = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_l1_co2aq, error_l1_co2aq, norm_l1_co2aq = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)


    abs_error_rms_ph, error_rms_ph, norm_rms_ph = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_rms_calcite, error_rms_calcite, norm_rms_calcite = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_rms_dolomite, error_rms_dolomite, norm_rms_dolomite = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_rms_hcation, error_rms_hcation, norm_rms_hcation = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_rms_cacation, error_rms_cacation, norm_rms_cacation = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_rms_mgcation, error_rms_mgcation, norm_rms_mgcation = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_rms_hco3anion, error_rms_hco3anion, norm_rms_hco3anion = np.zeros(nsteps), np.zeros(nsteps), np.zeros(
        nsteps)
    abs_error_rms_co2aq, error_rms_co2aq, norm_rms_co2aq = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)

    abs_error_inf_ph, error_inf_ph, norm_inf_ph = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_inf_calcite, error_inf_calcite, norm_inf_calcite = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_inf_dolomite, error_inf_dolomite, norm_inf_dolomite = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_inf_hcation, error_inf_hcation, norm_inf_hcation = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_inf_cacation, error_inf_cacation, norm_inf_cacation = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_inf_mgcation, error_inf_mgcation, norm_inf_mgcation = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    abs_error_inf_hco3anion, error_inf_hco3anion, norm_inf_hco3anion = np.zeros(nsteps), np.zeros(nsteps), np.zeros(
        nsteps)
    abs_error_inf_co2aq, error_inf_co2aq, norm_inf_co2aq = np.zeros(nsteps), np.zeros(nsteps), np.zeros(nsteps)
    '''
    abs_error_calcite = np.zeros(ncells)
    abs_error_dolomite = np.zeros(ncells)
    abs_error_hcation = np.zeros(ncells)
    abs_error_cacation = np.zeros(ncells)
    abs_error_mgcation = np.zeros(ncells)
    abs_error_hco3anion = np.zeros(ncells)
    abs_error_co2aq = np.zeros(ncells)

    rel_error_calcite = np.zeros(ncells)
    rel_error_dolomite = np.zeros(ncells)
    rel_error_hcation = np.zeros(ncells)
    rel_error_cacation = np.zeros(ncells)
    rel_error_mgcation = np.zeros(ncells)
    rel_error_hco3anion = np.zeros(ncells)
    rel_error_co2aq = np.zeros(ncells)

    for i in plot_at_steps_in_paper:
        print("On errors figure at time step: {}".format(i))

        filearray_class = np.loadtxt(folder_class + '/' + files_class[i - 1], skiprows=1)
        filearray_smart = np.loadtxt(folder_smart + '/' + files_smart[i - 1], skiprows=1)
        data_class = filearray_class.T
        data_smart = filearray_smart.T

        # Fetch reference and approximate data
        data_class_ph, data_smart_ph = data_class[indx_ph], data_smart[indx_ph]
        data_class_calcite, data_smart_calcite = data_class[indx_calcite], data_smart[indx_calcite]
        data_class_dolomite, data_smart_dolomite = data_class[indx_dolomite], data_smart[indx_dolomite]
        data_class_cacation, data_smart_cacation = data_class[indx_Cacation], data_smart[indx_Cacation]
        data_class_mgcation, data_smart_mgcation = data_class[indx_Mgcation], data_smart[indx_Mgcation]
        data_class_hco3anion, data_smart_hco3anion = data_class[indx_HCO3anion], data_smart[indx_HCO3anion]
        data_class_co2aq, data_smart_co2aq = data_class[indx_CO2aq], data_smart[indx_CO2aq]
        data_class_hcation, data_smart_hcation = data_class[indx_Hcation], data_smart[indx_Hcation]

        diff_calcite = np.abs(data_class_calcite - data_smart_calcite)
        diff_dolomite = np.abs(data_class_dolomite - data_smart_dolomite)
        diff_cacation = np.abs(data_class_cacation - data_smart_cacation)
        diff_mgcation = np.abs(data_class_mgcation - data_smart_mgcation)
        diff_hco3anion = np.abs(data_class_hco3anion - data_smart_hco3anion)
        diff_co2aq = np.abs(data_class_co2aq - data_smart_co2aq)
        diff_hcation = np.abs(data_class_hcation - data_smart_hcation)

        for j in range(ncells):
            abs_error_calcite[j] = diff_calcite[j]
            abs_error_dolomite[j] = diff_dolomite[j]
            abs_error_cacation[j] = diff_cacation[j]
            abs_error_mgcation[j] = diff_mgcation[j]
            abs_error_hco3anion[j] = diff_hco3anion[j]
            abs_error_co2aq[j] = diff_co2aq[j]
            abs_error_hcation[j] = diff_hcation[j]

        '''
        for j in range(ncells):
            abs_error_calcite[j] = diff_calcite[j] / np.max(data_class_calcite)
            abs_error_dolomite[j] = diff_dolomite[j] / np.max(data_class_dolomite)
            abs_error_cacation[j] = diff_cacation[j] / np.max(data_class_cacation)
            abs_error_mgcation[j] = diff_mgcation[j]  / np.max(data_class_mgcation)
            abs_error_hco3anion[j] = diff_hco3anion[j] / np.max(data_class_hco3anion)
            abs_error_co2aq[j] = diff_co2aq[j] / np.max(data_class_co2aq)
            abs_error_hcation[j] = diff_hcation[j] / np.max(data_class_hcation)
        '''
        #'''


        print("|n_ref - n_approx| = ", diff_calcite[15])
        print("|n_approx| = ", data_smart_calcite[15])
        print("|n_ref| = ", data_class_calcite[15])
        print("|n_ref - n_approx| / |n_ref| = ", diff_calcite[15] / data_class_calcite[15])

        for j in range(ncells):
            rel_error_calcite[j] = diff_calcite[j] / data_class_calcite[j] if data_class_calcite[j] > tol else 0.0
            rel_error_dolomite[j] = diff_dolomite[j] / data_class_dolomite[j] if data_class_dolomite[j] > tol else 0.0
            rel_error_cacation[j] = diff_cacation[j] / data_class_cacation[j] if data_class_cacation[j] > tol else 0.0
            rel_error_mgcation[j] = diff_mgcation[j] / data_class_mgcation[j] if data_class_mgcation[j] > tol else 0.0
            rel_error_hco3anion[j] = diff_hco3anion[j] / data_class_hco3anion[j] if data_class_hco3anion[j] > tol else 0.0
            rel_error_co2aq[j] = diff_co2aq[j] / data_class_co2aq[j] if data_class_co2aq[j] > tol else 0.0
            rel_error_hcation[j] = diff_hcation[j] / data_class_hcation[j] if data_class_hcation[j] > tol else 0.0
        #'''
        t = i * dt
        plt.axes(xlim=(-0.01, 0.501))
        plt.xlabel('Distance [m]', fontproperties=prop)
        plt.ylabel('Error [%vol]', fontproperties=prop)
        plt.title(titlestr(t), fontproperties=prop, fontsize=24)
        plt.plot(xcells, abs_error_calcite * 100/(1 - phi), label='Calcite', **line_error('C0'))
        plt.plot(xcells, abs_error_dolomite * 100/(1 - phi), label='Dolomite', **line_error('C1'))
        plt.legend(loc='center right', prop=prop)
        plt.savefig(folder_general + f'/error-abs-calcite-dolomite-{i}.pdf')
        plt.tight_layout()
        plt.close()

        """
        plt.axes(xlim=(-0.01, 0.501))
        plt.xlabel('Distance [m]', fontproperties=prop)
        plt.ylabel('Error [molal]', fontproperties=prop)
        plt.yscale('log')
        plt.title(titlestr(t), fontproperties=prop, fontsize=24)
        plt.plot(xcells, abs_error_cacation, label=r'$\mathrm{Ca^{2+}}$', **line_error('C0'))
        plt.plot(xcells, abs_error_mgcation, label=r'$\mathrm{Mg^{2+}}$', **line_error('C1'))
        plt.plot(xcells, abs_error_hco3anion, label=r'$\mathrm{HCO_3^{-}}$', **line_error('C2'))
        plt.plot(xcells, abs_error_co2aq, label=r'$\mathrm{CO_2(aq)}$', **line_error('red'))
        plt.plot(xcells, abs_error_hcation, label=r'$\mathrm{H^+}$', **line_error('darkviolet'))
        plt.legend(loc='upper right', prop=prop)
        plt.savefig(folder_general + f'/error-abs-aqueous-species-{i}.pdf')
        plt.tight_layout()
        plt.close()

        """

        abs_error_cacation[abs_error_cacation == 0] = 1e-12
        abs_error_mgcation[abs_error_mgcation == 0] = 1e-12
        abs_error_hco3anion[abs_error_hco3anion == 0] = 1e-12
        abs_error_co2aq[abs_error_co2aq == 0] = 1e-12
        abs_error_hcation[abs_error_hcation == 0] = 1e-12

        plt.axes(xlim=(-0.01, 0.501))
        plt.xlabel('Distance [m]', fontproperties=prop)
        plt.ylabel('Error [log 10 molal]', fontproperties=prop)
        plt.title(titlestr(t), fontproperties=prop, fontsize=24)
        plt.plot(xcells, np.log10(abs_error_cacation), label='Ca+2', **line_error('C0'))
        plt.plot(xcells, np.log10(abs_error_mgcation), label='Mg+2', **line_error('C1'))
        plt.plot(xcells, np.log10(abs_error_hco3anion), label='HCO3-', **line_error('C2'))
        plt.plot(xcells, np.log10(abs_error_co2aq), label='CO2(aq)', **line_error('red'))
        plt.plot(xcells, np.log10(abs_error_hcation), label='H+', **line_error('darkviolet'))
        plt.legend(loc='upper right', prop=prop)
        plt.savefig(folder_general + f'/error-log10-abs-aqueous-species-{i}.pdf')
        plt.tight_layout()
        plt.close()
        '''
        plt.axes(xlim=(-0.01, 0.501))
        plt.xlabel('Distance [m]')
        plt.ylabel('Relative Error [-]')
        plt.title(titlestr(t))
        plt.plot(xcells, rel_error_calcite, label='Calcite', **line('C0'))
        plt.plot(xcells, rel_error_dolomite, label='Dolomite', **line('C1'))
        plt.legend(loc='center right')
        plt.savefig(folder_general + f'/error-rel-calcite-dolomite-{i}.pdf')
        plt.tight_layout()
        plt.close()

        plt.axes(xlim=(-0.01, 0.501))
        plt.xlabel('Distance [m]')
        plt.ylabel('Relative Error [-]')
        plt.yscale('log')
        plt.title(titlestr(t))
        plt.plot(xcells, rel_error_cacation, label=r'$\mathrm{Ca^{2+}}$', **line('C0'))
        plt.plot(xcells, rel_error_mgcation, label=r'$\mathrm{Mg^{2+}}$', **line('C1'))
        plt.plot(xcells, rel_error_hco3anion, label=r'$\mathrm{HCO_3^{-}}$', **line('C2'))
        plt.plot(xcells, rel_error_co2aq, label=r'$\mathrm{CO_2(aq)}$', **line('red'))
        plt.plot(xcells, rel_error_hcation, label=r'$\mathrm{H^+}$', **line('darkviolet'))
        plt.legend(loc='upper right')
        plt.savefig(folder_general + f'/error-rel-aqueous-species-{i}.pdf')
        plt.tight_layout()
        plt.close()
        '''
        '''
        # ------------------------------------------------------------------------------------------------------ #
        # L1-norm
        # ------------------------------------------------------------------------------------------------------ #

        # Calculate difference between reference and approximate data with l1 norm
        abs_error_l1_ph[i] = la.norm(data_class_ph - data_smart_ph, 1)
        abs_error_l1_calcite[i] = la.norm(data_class_calcite - data_smart_calcite, 1)
        abs_error_l1_dolomite[i] = la.norm(data_class_dolomite - data_smart_dolomite, 1)
        abs_error_l1_hcation[i] = la.norm(data_class_hcation - data_smart_hcation, 1)
        abs_error_l1_cacation[i] = la.norm(data_class_cacation - data_smart_cacation, 1)
        abs_error_l1_mgcation[i] = la.norm(data_class_mgcation - data_smart_mgcation, 1)
        abs_error_l1_hco3anion[i] = la.norm(data_class_hco3anion - data_smart_hco3anion, 1)
        abs_error_l1_cacation[i] = la.norm(data_class_cacation - data_smart_cacation, 1)
        abs_error_l1_co2aq[i] = la.norm(data_class_co2aq - data_smart_co2aq, 1)

        # Calculate with l1 norm of the reference data
        norm_l1_ph[i] = la.norm(data_class_ph, 1)
        norm_l1_calcite[i] = la.norm(data_class_calcite, 1)
        norm_l1_dolomite[i] = la.norm(data_class_dolomite, 1)
        norm_l1_hcation[i] = la.norm(data_class_hcation, 1)
        norm_l1_cacation[i] = la.norm(data_class_cacation, 1)
        norm_l1_mgcation[i] = la.norm(data_class_mgcation, 1)
        norm_l1_hco3anion[i] = la.norm(data_class_hco3anion, 1)
        norm_l1_cacation[i] = la.norm(data_class_cacation, 1)
        norm_l1_co2aq[i] = la.norm(data_class_co2aq, 1)

        # Calculate the error by |n_ref - n_approx|_l1 / |n_ref|_l1
        # if norm_l1_calcite[i] < tol:
        #    print(norm_l1_calcite[i])
        #    input()
        # if i >= 8000:
        #    print(f"|n_ref - n_approx|_l1 = {abs_error_l1_calcite[i]:>15} \t |n_ref|_l1 = {norm_l1_calcite[i]}")
        #    input()

        error_l1_ph[i] = abs_error_l1_ph[i] / norm_l1_ph[i] if norm_l1_ph[i] > tol else 0.0
        error_l1_calcite[i] = abs_error_l1_calcite[i] / norm_l1_calcite[i] if norm_l1_calcite[i] > tol else 0.0
        error_l1_dolomite[i] = abs_error_l1_dolomite[i] / norm_l1_dolomite[i] if norm_l1_dolomite[i] > tol else 0.0
        error_l1_hcation[i] = abs_error_l1_hcation[i] / norm_l1_hcation[i] if norm_l1_hcation[i] > tol else 0.0
        error_l1_cacation[i] = abs_error_l1_cacation[i] / norm_l1_cacation[i] if norm_l1_cacation[i] > tol else 0.0
        error_l1_mgcation[i] = abs_error_l1_mgcation[i] / norm_l1_mgcation[i] if norm_l1_mgcation[i] > tol else 0.0
        error_l1_hco3anion[i] = abs_error_l1_hco3anion[i] / norm_l1_hco3anion[i] if norm_l1_hco3anion[i] > tol else 0.0
        error_l1_cacation[i] = abs_error_l1_cacation[i] / norm_l1_cacation[i] if norm_l1_cacation[i] > tol else 0.0
        error_l1_co2aq[i] = abs_error_l1_co2aq[i] / norm_l1_co2aq[i] if norm_l1_co2aq[i] > tol else 0.0

        # ------------------------------------------------------------------------------------------------------ #
        # L2-norm
        # ------------------------------------------------------------------------------------------------------ #

        abs_error_rms_ph[i] = np.sqrt(np.mean((data_class_ph - data_smart_ph) ** 2))
        abs_error_rms_calcite[i] = np.sqrt(np.mean((data_class_calcite - data_smart_calcite) ** 2))
        abs_error_rms_dolomite[i] = np.sqrt(np.mean((data_class_dolomite - data_smart_dolomite) ** 2))
        abs_error_rms_hcation[i] = np.sqrt(np.mean((data_class_hcation - data_smart_hcation) ** 2))
        abs_error_rms_cacation[i] = np.sqrt(np.mean((data_class_cacation - data_smart_cacation) ** 2))
        abs_error_rms_mgcation[i] = np.sqrt(np.mean((data_class_mgcation - data_smart_mgcation) ** 2))
        abs_error_rms_hco3anion[i] = np.sqrt(np.mean((data_class_hco3anion - data_smart_hco3anion) ** 2))
        abs_error_rms_cacation[i] = np.sqrt(np.mean((data_class_cacation - data_smart_cacation) ** 2))
        abs_error_rms_co2aq[i] = np.sqrt(np.mean((data_class_co2aq - data_smart_co2aq) ** 2))

        norm_rms_ph[i] = np.sqrt(np.mean(data_class_ph ** 2))
        norm_rms_calcite[i] = np.sqrt(np.mean(data_class_calcite ** 2))
        norm_rms_dolomite[i] = np.sqrt(np.mean(data_class_dolomite ** 2))
        norm_rms_hcation[i] = np.sqrt(np.mean(data_class_hcation ** 2))
        norm_rms_cacation[i] = np.sqrt(np.mean(data_class_cacation ** 2))
        norm_rms_mgcation[i] = np.sqrt(np.mean(data_class_mgcation ** 2))
        norm_rms_hco3anion[i] = np.sqrt(np.mean(data_class_hco3anion ** 2))
        norm_rms_cacation[i] = np.sqrt(np.mean(data_class_cacation ** 2))
        norm_rms_co2aq[i] = np.sqrt(np.mean(data_class_co2aq ** 2))

        error_rms_ph[i] = abs_error_rms_ph[i] / norm_rms_ph[i] if norm_rms_ph[i] > tol else 0.0
        error_rms_calcite[i] = abs_error_rms_calcite[i] / norm_rms_calcite[i] if norm_rms_calcite[i] > tol else 0.0
        error_rms_dolomite[i] = abs_error_rms_dolomite[i] / norm_rms_dolomite[i] if norm_rms_dolomite[i] > tol else 0.0
        error_rms_hcation[i] = abs_error_rms_hcation[i] / norm_rms_hcation[i] if norm_rms_hcation[i] > tol else 0.0
        error_rms_cacation[i] = abs_error_rms_cacation[i] / norm_rms_cacation[i] if norm_rms_cacation[i] > tol else 0.0
        error_rms_mgcation[i] = abs_error_rms_mgcation[i] / norm_rms_mgcation[i] if norm_rms_mgcation[i] > tol else 0.0
        error_rms_hco3anion[i] = abs_error_rms_hco3anion[i] / norm_rms_hco3anion[i] if norm_rms_hco3anion[
                                                                                           i] > tol else 0.0
        error_rms_cacation[i] = abs_error_rms_cacation[i] / norm_rms_cacation[i] if norm_rms_cacation[i] > tol else 0.0
        error_rms_co2aq[i] = abs_error_rms_co2aq[i] / norm_rms_co2aq[i] if norm_rms_co2aq[i] > tol else 0.0

        # ------------------------------------------------------------------------------------------------------ #
        # Inf-norm
        # ------------------------------------------------------------------------------------------------------ #

        # Calculate difference between reference and approximate data with l1 norm
        abs_error_inf_ph[i] = la.norm(data_class_ph - data_smart_ph, np.inf)
        abs_error_inf_calcite[i] = la.norm(data_class_calcite - data_smart_calcite, np.inf)
        abs_error_inf_dolomite[i] = la.norm(data_class_dolomite - data_smart_dolomite, np.inf)
        abs_error_inf_hcation[i] = la.norm(data_class_hcation - data_smart_hcation, np.inf)
        abs_error_inf_cacation[i] = la.norm(data_class_cacation - data_smart_cacation, np.inf)
        abs_error_inf_mgcation[i] = la.norm(data_class_mgcation - data_smart_mgcation, np.inf)
        abs_error_inf_hco3anion[i] = la.norm(data_class_hco3anion - data_smart_hco3anion, np.inf)
        abs_error_inf_cacation[i] = la.norm(data_class_cacation - data_smart_cacation, np.inf)
        abs_error_inf_co2aq[i] = la.norm(data_class_co2aq - data_smart_co2aq, np.inf)

        # Calculate with l1 norm of the reference data
        norm_inf_ph[i] = la.norm(data_class_ph, np.inf)
        norm_inf_calcite[i] = la.norm(data_class_calcite, np.inf)
        norm_inf_dolomite[i] = la.norm(data_class_dolomite, np.inf)
        norm_inf_hcation[i] = la.norm(data_class_hcation, np.inf)
        norm_inf_cacation[i] = la.norm(data_class_cacation, np.inf)
        norm_inf_mgcation[i] = la.norm(data_class_mgcation, np.inf)
        norm_inf_hco3anion[i] = la.norm(data_class_hco3anion, np.inf)
        norm_inf_cacation[i] = la.norm(data_class_cacation, np.inf)
        norm_inf_co2aq[i] = la.norm(data_class_co2aq, np.inf)

        # Calculate the error by |n_ref - n_approx|_inf / |n_ref|_inf
        #if norm_inf_calcite[i] < tol:
        #    print(norm_inf_calcite[i])
        #    input()
        # if i >= 8000:
        #    print(f"|n_ref - n_approx|_inf = {abs_error_inf_calcite[i]:>15} \t |n_ref|_inf = {norm_inf_calcite[i]}")
        #    input()

        error_inf_ph[i] = abs_error_inf_ph[i] / norm_inf_ph[i] if norm_inf_ph[i] > tol else 0.0
        error_inf_calcite[i] = abs_error_inf_calcite[i] / norm_inf_calcite[i] if norm_inf_calcite[i] > tol else 0.0
        error_inf_dolomite[i] = abs_error_inf_dolomite[i] / norm_inf_dolomite[i] if norm_inf_dolomite[i] > tol else 0.0
        error_inf_hcation[i] = abs_error_inf_hcation[i] / norm_inf_hcation[i] if norm_inf_hcation[i] > tol else 0.0
        error_inf_cacation[i] = abs_error_inf_cacation[i] / norm_inf_cacation[i] if norm_inf_cacation[i] > tol else 0.0
        error_inf_mgcation[i] = abs_error_inf_mgcation[i] / norm_inf_mgcation[i] if norm_inf_mgcation[i] > tol else 0.0
        error_inf_hco3anion[i] = abs_error_inf_hco3anion[i] / norm_inf_hco3anion[i] if norm_inf_hco3anion[
                                                                                           i] > tol else 0.0
        error_inf_cacation[i] = abs_error_inf_cacation[i] / norm_inf_cacation[i] if norm_inf_cacation[i] > tol else 0.0
        error_inf_co2aq[i] = abs_error_inf_co2aq[i] / norm_inf_co2aq[i] if norm_inf_co2aq[i] > tol else 0.0
        '''
    # -----------------------------------------------------------------------------------------------------------------#
    # Plot l1-error
    # -----------------------------------------------------------------------------------------------------------------#
    '''
    step = 40
    plt.xlabel('Time Step')
    #plt.axes(ylim=(pow(10, -6), pow(10, -1)))
    #plt.yscale('log')
    plt.ylabel(r'Error in $\ell_1$-norm')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], error_l1_calcite[0:nsteps:step], label=r'$\| e_{\rm CaCO_3}\|_{\ell_1}$',
             color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_l1_dolomite[0:nsteps:step], label=r'$\| e_{\rm CaMg(CO_3)_2}\|_{\ell_1}$',
             color='C1', linewidth=1)
    leg = plt.legend(loc='lower right')
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig(folder_general + '/errors-calcite-dolomite-l1.pdf')
    plt.close()

    plt.xlabel('Time Step')
    #plt.axes(ylim=(pow(10, -5), pow(10, 0)))
    #plt.yscale('log')
    plt.ylabel(r'Error in $\ell_1$-norm')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], error_l1_cacation[0:nsteps:step], label=r'$\| e_{\rm Ca^{2+}}\|_{\ell_1}$',
             color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_l1_mgcation[0:nsteps:step], label=r'$\| e_{\rm Mg^{2+}}\|_{\ell_1}$',
             color='C1', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_l1_hco3anion[0:nsteps:step], label=r'$\| e_{\rm HCO_3^{-}}\|_{\ell_1}$',
             color='C2', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_l1_co2aq[0:nsteps:step], label=r'$\| e_{\rm CO_2(aq)}\|_{\ell_1}$',
             color='red', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_l1_hcation[0:nsteps:step], label=r'$\| e_{\rm H^+}\|_{\ell_1}$',
             color='darkviolet', linewidth=1)
    leg = plt.legend(loc='lower right')
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig(folder_general + '/errors-aqueous-l1.pdf')
    plt.close()

    step = 40
    plt.xlabel('Time Step')
    plt.axes(ylim=(pow(10, -6), pow(10, -2)))
    plt.yscale('log')
    plt.ylabel(r'Error in $\ell_1$-norm, $\log$-scale')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], error_l1_calcite[0:nsteps:step], label=r'$\| e_{\rm CaCO_3}\|_{\ell_1}$',
             color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_l1_dolomite[0:nsteps:step], label=r'$\| e_{\rm CaMg(CO_3)_2}\|_{\ell_1}$',
             color='C1', linewidth=1)
    leg = plt.legend(loc='lower right')
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig(folder_general + '/errors-calcite-dolomite-l1-log.pdf')
    plt.close()

    plt.xlabel('Time Step')
    plt.axes(ylim=(pow(10, -5), pow(10, 0)))
    plt.yscale('log')
    plt.ylabel(r'Error in $\ell_1$-norm, $\log$-scale')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], error_l1_cacation[0:nsteps:step], label=r'$\| e_{\rm Ca^{2+}}\|_{\ell_1}$',
             color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_l1_mgcation[0:nsteps:step], label=r'$\| e_{\rm Mg^{2+}}\|_{\ell_1}$',
             color='C1', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_l1_hco3anion[0:nsteps:step], label=r'$\| e_{\rm HCO_3^{-}}\|_{\ell_1}$',
             color='C2', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_l1_co2aq[0:nsteps:step], label=r'$\| e_{\rm CO_2(aq)}\|_{\ell_1}$',
             color='red', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_l1_hcation[0:nsteps:step], label=r'$\| e_{\rm H^+}\|_{\ell_1}$',
             color='darkviolet', linewidth=1)
    leg = plt.legend(loc='lower right')
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig(folder_general + '/errors-aqueous-l1-log.pdf')
    plt.close()
    

    # -----------------------------------------------------------------------------------------------------------------#
    # Plot l1-error in %
    # -----------------------------------------------------------------------------------------------------------------#

    plt.xlabel('Time Step')
    plt.ylabel(r'Error in $\ell_1$-norm [%]')
    #plt.yscale('log')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], 100 * error_l1_calcite[0:nsteps:step], label=r'$\| e_{\rm CaCO_3}\|$',
             color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], 100 * error_l1_dolomite[0:nsteps:step], label=r'$\| e_{\rm CaMg(CO_3)_2}\|$',
             color='C1', linewidth=1)
    leg = plt.legend(loc='lower right')
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig(folder_general + '/errors-calcite-dolomite-l1-percent.pdf')
    plt.close()

    plt.xlabel('Time Step')
    plt.ylabel(r'Error in $\ell_1$-norm [%]')
    #plt.yscale('log')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], 100 * error_l1_cacation[0:nsteps:step],
             label=r'$\| e_{\rm Ca^{2+}}\|$', color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], 100 * error_l1_mgcation[0:nsteps:step],
             label=r'$\| e_{\rm Mg^{2+}}\|$', color='C1', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], 100 * error_l1_hco3anion[0:nsteps:step],
             label=r'$\| e_{\rm HCO_3^{-}}\|$', color='C2', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], 100 * error_l1_co2aq[0:nsteps:step], label=r'$\| e_{\rm CO_2(aq)}\|$',
             color='red', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], 100 * error_l1_hcation[0:nsteps:step], label=r'$\| e_{\rm H^+}\|$',
             color='darkviolet', linewidth=1)
    leg = plt.legend(loc='upper left')
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig(folder_general + '/errors-aqueous-l1-percent.pdf')
    plt.close()
    '''
    '''
    # -----------------------------------------------------------------------------------------------------------------#
    # Plot RMS-error
    # -----------------------------------------------------------------------------------------------------------------#

    plt.xlabel('Time Step')
    plt.ylabel(r'RMS Error')
    plt.axes(ylim=(pow(10, -6), pow(10, -1)))
    plt.yscale('log')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], error_rms_calcite[0:nsteps:step], label=r'$\| e_{\rm Calcite}\|_{\rm RMS}$',
             color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_rms_dolomite[0:nsteps:step], label=r'$\| e_{\rm Dolomite}\|_{\rm RMS}$',
             color='C1', linewidth=1)
    leg = plt.legend(loc='lower right', bbox_to_anchor=(1, 0.13))
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig(folder_general + '/errors-calcite-dolomite-rms.pdf')
    plt.close()

    plt.xlabel('Time Step')
    plt.ylabel('RMS Error')
    plt.axes(ylim=(pow(10, -5), pow(10, 0)))
    plt.yscale('log')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], error_rms_cacation[0:nsteps:step], label=r'$\| e_{\rm Ca^{2+}}\|_{\rm RMS}$',
             color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_rms_mgcation[0:nsteps:step], label=r'$\| e_{\rm Mg^{2+}}\|_{\rm RMS}$',
             color='C1', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_rms_hco3anion[0:nsteps:step], label=r'$\| e_{\rm HCO_3^{-}}\|_{\rm RMS}$',
             color='C2', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_rms_co2aq[0:nsteps:step], label=r'$\| e_{\rm CO_2(aq)}\|_{\rm RMS}$',
             color='red', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_rms_hcation[0:nsteps:step], label=r'$\| e_{\rm H^+}\|_{\rm RMS}$',
             color='darkviolet', linewidth=1)
    leg = plt.legend(loc='lower right')
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig(folder_general + '/errors-aqueous-rms.pdf')
    plt.close()

    # -----------------------------------------------------------------------------------------------------------------#
    # Plot inf-error
    # -----------------------------------------------------------------------------------------------------------------#

    step = 40
    plt.xlabel('Time Step')
    plt.axes(ylim=(pow(10, -6), pow(10, 0)))
    plt.yscale('log')
    plt.ylabel(r'Error in $\infty$-norm')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], error_inf_calcite[0:nsteps:step],
             label=r'$\| e_{\rm CaCO_3}\|_{\infty}$',
             color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_inf_dolomite[0:nsteps:step],
             label=r'$\| e_{\rm CaMg(CO_3)_2}\|_{\infty}$',
             color='C1', linewidth=1)
    leg = plt.legend(loc='lower right')
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig('errors-calcite-dolomite-inf.pdf')
    plt.close()

    plt.xlabel('Time Step')
    plt.axes(ylim=(pow(10, -5), pow(10, 0)))
    plt.yscale('log')
    plt.ylabel(r'Error in $\infty$-norm')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], error_inf_cacation[0:nsteps:step], label=r'$\| e_{\rm Ca^{2+}}\|_{\infty}$',
             color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_inf_mgcation[0:nsteps:step], label=r'$\| e_{\rm Mg^{2+}}\|_{\infty}$',
             color='C1', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_inf_hco3anion[0:nsteps:step], label=r'$\| e_{\rm HCO_3^{-}}\|_{\infty}$',
             color='C2', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_inf_co2aq[0:nsteps:step], label=r'$\| e_{\rm CO_2(aq)}\|_{\infty}$',
             color='red', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], error_inf_hcation[0:nsteps:step], label=r'$\| e_{\rm H^+}\|_{\infty}$',
             color='darkviolet', linewidth=1)
    leg = plt.legend(loc='lower right')
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig(folder_general + '/errors-aqueous-inf.pdf')
    plt.close()

    # -----------------------------------------------------------------------------------------------------------------#
    # Plot inf-error in %
    # -----------------------------------------------------------------------------------------------------------------#

    plt.xlabel('Time Step')
    plt.ylabel(r'Error in $\infty$-norm [%]')
    plt.yscale('log')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], 100 * error_inf_calcite[0:nsteps:step], label=r'$\| e_{\rm CaCO_3}\|$',
             color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], 100 * error_inf_dolomite[0:nsteps:step], label=r'$\| e_{\rm CaMg(CO_3)_2}\|$',
             color='C1', linewidth=1)
    leg = plt.legend(loc='lower right')
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig('errors-calcite-dolomite-inf-percent.pdf')
    plt.close()

    plt.xlabel('Time Step')
    plt.ylabel(r'Error in $\infty$-norm [%]')
    plt.yscale('log')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], 100 * error_inf_cacation[0:nsteps:step],
             label=r'$\| e_{\rm Ca^{2+}}\|$', color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], 100 * error_inf_mgcation[0:nsteps:step],
             label=r'$\| e_{\rm Mg^{2+}}\|$', color='C1', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], 100 * error_inf_hco3anion[0:nsteps:step],
             label=r'$\| e_{\rm HCO_3^{-}}\|$', color='C2', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], 100 * error_inf_co2aq[0:nsteps:step], label=r'$\| e_{\rm CO_2(aq)}\|$',
             color='red', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], 100 * error_inf_hcation[0:nsteps:step], label=r'$\| e_{\rm H^+}\|$',
             color='darkviolet', linewidth=1)
    leg = plt.legend(loc='upper left')
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig(folder_general + '/errors-aqueous-inf-percent.pdf')
    plt.close()
    
    print('max |e in pH|_l1 = %2.2e' % np.max(error_l1_ph))
    print('max |e in calcite|_l1 = %2.2e' % np.max(error_l1_calcite))
    print('max |e in dolomite|_l1 = %2.2e' % np.max(error_l1_dolomite))
    print('max |e in hcation|_l1 = %2.2e' % np.max(error_l1_hcation))
    print('max |e in cacation|_l1 = %2.2e' % np.max(error_l1_cacation))
    print('max |e in mgcation|_l1 = %2.2e' % np.max(error_l1_mgcation))
    print('max |e in hco3anion|_l1 = %2.2e' % np.max(error_l1_hco3anion))
    print('max |e in cacation|_l1 = %2.2e' % np.max(error_l1_cacation))
    print('max |e in co2aq|_l1 = %2.2e\n' % np.max(error_l1_co2aq))

    print('max |e in pH|_l1 = %2.2f percent' % (100 * np.max(error_l1_ph)))
    print('max |e in calcite|_l1 = %2.2f percent' % (100 * np.max(error_l1_calcite)))
    print('max |e in dolomite|_l1 = %2.2f percent' % (100 * np.max(error_l1_dolomite)))
    print('max |e in hcation|_l1 = %2.2f percent' % (100 * np.max(error_l1_hcation)))
    print('max |e in cacation|_l1 = %2.2f percent' % (100 * np.max(error_l1_cacation)))
    print('max |e in mgcation|_l1 = %2.2f percent' % (100 * np.max(error_l1_mgcation)))
    print('max |e in hco3anion|_l1 = %2.2f percent' % (100 * np.max(error_l1_hco3anion)))
    print('max |e in cacation|_l1 = %2.2f percent' % (100 * np.max(error_l1_cacation)))
    print('max |e in co2aq|_l1 = %2.2f percent\n' % (100 * np.max(error_l1_co2aq)))
    
    print('max |e in pH|_rms = %2.2e' % np.max(error_rms_ph))
    print('max |e in calcite|_rms = %2.2e' % np.max(error_rms_calcite))
    print('max |e in dolomite|_rms = %2.2e' % np.max(error_rms_dolomite))
    print('max |e in hcation|_rms = %2.2e' % np.max(error_rms_hcation))
    print('max |e in cacation|_rms = %2.2e' % np.max(error_rms_cacation))
    print('max |e in mgcation|_rms = %2.2e' % np.max(error_rms_mgcation))
    print('max |e in hco3anion|_rms = %2.2e' % np.max(error_rms_hco3anion))
    print('max |e in cacation|_rms = %2.2e' % np.max(error_rms_cacation))
    print('max |e in co2aq|_rms = %2.2e\n' % np.max(error_rms_co2aq))

    print('max |e in pH|_rms = %2.2f percent' % (100 * np.max(error_rms_ph)))
    print('max |e in calcite|_rms = %2.2f percent' % (100 * np.max(error_rms_calcite)))
    print('max |e in dolomite|_rms = %2.2f percent' % (100 * np.max(error_rms_dolomite)))
    print('max |e in hcation|_rms = %2.2f percent' % (100 * np.max(error_rms_hcation)))
    print('max |e in cacation|_rms = %2.2f percent' % (100 * np.max(error_rms_cacation)))
    print('max |e in mgcation|_rms = %2.2f percent' % (100 * np.max(error_rms_mgcation)))
    print('max |e in hco3anion|_rms = %2.2f percent' % (100 * np.max(error_rms_hco3anion)))
    print('max |e in cacation|_rms = %2.2f percent' % (100 * np.max(error_rms_cacation)))
    print('max |e in co2aq|_rms = %2.2f percent' % (100 * np.max(error_rms_co2aq)))

    print('max |e in pH|_inf = %2.2e' % np.max(error_inf_ph))
    print('max |e in calcite|_inf = %2.2e' % np.max(error_inf_calcite))
    print('max |e in dolomite|_inf = %2.2e' % np.max(error_inf_dolomite))
    print('max |e in hcation|_inf = %2.2e' % np.max(error_inf_hcation))
    print('max |e in cacation|_inf = %2.2e' % np.max(error_inf_cacation))
    print('max |e in mgcation|_inf = %2.2e' % np.max(error_inf_mgcation))
    print('max |e in hco3anion|_inf = %2.2e' % np.max(error_inf_hco3anion))
    print('max |e in cacation|_inf = %2.2e' % np.max(error_inf_cacation))
    print('max |e in co2aq|_inf = %2.2e\n' % np.max(error_inf_co2aq))

    print('max |e in pH|_inf = %2.2f in percent' % (100 * np.max(error_inf_ph)))
    print('max |e in calcite|_inf = %2.2f in percent' % (100 * np.max(error_inf_calcite)))
    print('max |e in dolomite|_inf = %2.2f in percent' % (100 * np.max(error_inf_dolomite)))
    print('max |e in hcation|_inf = %2.2f in percent' % (100 * np.max(error_inf_hcation)))
    print('max |e in cacation|_inf = %2.2f in percent' % (100 * np.max(error_inf_cacation)))
    print('max |e in mgcation|_inf = %2.2f in percent' % (100 * np.max(error_inf_mgcation)))
    print('max |e in hco3anion|_inf = %2.2f in percent' % (100 * np.max(error_inf_hco3anion)))
    print('max |e in cacation|_inf = %2.2f in percent' % (100 * np.max(error_inf_cacation)))
    print('max |e in co2aq|_inf = %2.2f in percent' % (100 * np.max(error_inf_co2aq)))
    '''

def plot_figures_ph():

    for i in plot_at_selected_steps:
        print("On pH figure at time step: {}".format(i))
        t = i * dt
        filearray_class = np.loadtxt(folder_class + '/' + files_class[i-1], skiprows=1)
        filearray_smart = np.loadtxt(folder_smart + '/' + files_smart[i-1], skiprows=1)
        data_class = filearray_class.T
        data_smart = filearray_smart.T
        data_class_ph = data_class[indx_ph]
        data_smart_ph = data_smart[indx_ph]
        plt.axes(xlim=(-0.01, 0.501), ylim=(2.5, 12.0))
        plt.xlabel('Distance [m]', fontproperties=prop)
        plt.ylabel('pH', fontproperties=prop)
        plt.title(titlestr(t), fontproperties=prop, fontsize=24)
        plt.plot(xcells, data_class_ph, label='pH', **line('teal'))
        plt.plot(xcells[status[i-1]==0], data_smart_ph[status[i-1]==0], 'o', **line_empty_marker('teal'))
        plt.plot(xcells[status[i-1]==1], data_smart_ph[status[i-1]==1], 'o', **line_filled_marker('teal'))
        plt.plot([], [], 'o', label='Smart Prediction', **line_filled_marker('black'))
        plt.plot([], [], 'o', label='Learning', **line_empty_marker('black'))
        plt.legend(loc='lower right', prop=prop)
        plt.savefig(folder_general + '/pH-{}.pdf'.format(i))
        plt.tight_layout()
        plt.close()

def plot_figures_calcite_dolomite():

    for i in plot_at_selected_steps:
        print("On calcite-dolomite figure at time step: {}".format(i))
        t = i * dt
        filearray_class = np.loadtxt(folder_class + '/' + files_class[i-1], skiprows=1)
        filearray_smart = np.loadtxt(folder_smart + '/' + files_smart[i-1], skiprows=1)
        data_class = filearray_class.T
        data_smart = filearray_smart.T
        data_class_calcite, data_class_dolomite = data_class[indx_calcite], data_class[indx_dolomite]
        data_smart_calcite, data_smart_dolomite = data_smart[indx_calcite], data_smart[indx_dolomite]
        plt.axes(xlim=(-0.01, 0.501), ylim=(-0.1, 2.1))
        plt.xlabel('Distance [m]', fontproperties=prop)
        plt.ylabel('Mineral Volume [%vol]', fontproperties=prop)
        plt.title(titlestr(t), fontproperties=prop, fontsize=24)
        plt.plot(xcells, data_class_calcite * 100/(1 - phi), label='Calcite', **line('C0'))
        plt.plot(xcells, data_class_dolomite * 100/(1 - phi), label='Dolomite', **line('C1'))
        plt.plot(xcells[status[i-1]==0], data_smart_calcite[status[i-1]==0] * 100/(1 - phi), 'o', **line_empty_marker('C0'))
        plt.plot(xcells[status[i-1]==1], data_smart_calcite[status[i-1]==1] * 100/(1 - phi), 'o', **line_filled_marker('C0'))
        plt.plot(xcells[status[i-1]==0], data_smart_dolomite[status[i-1]==0] * 100/(1 - phi), 'o', **line_empty_marker('C1'))
        plt.plot(xcells[status[i-1]==1], data_smart_dolomite[status[i-1]==1] * 100/(1 - phi), 'o', **line_filled_marker('C1'))
        plt.plot([], [], 'o', label='Smart Prediction', **line_filled_marker('black'))
        plt.plot([], [], 'o', label='Learning', **line_empty_marker('black'))
        plt.legend(loc='center right', prop=prop)
        plt.savefig(folder_general + '/calcite-dolomite-{}.pdf'.format(i))
        plt.tight_layout()
        plt.close()

def plot_figures_log10_aqueous_species():

    for i in plot_at_selected_steps:
        print("On aqueous-species figure at time step: {}".format(i))
        t = i * dt
        filearray_class = np.loadtxt(folder_class + '/' + files_class[i-1], skiprows=1)
        filearray_smart = np.loadtxt(folder_smart + '/' + files_smart[i-1], skiprows=1)
        data_class = filearray_class.T
        data_smart = filearray_smart.T
        data_class_cacation  = data_class[indx_Cacation]
        data_class_mgcation  = data_class[indx_Mgcation]
        data_class_hco3anion = data_class[indx_HCO3anion]
        data_class_co2aq     = data_class[indx_CO2aq]
        data_class_hcation   = data_class[indx_Hcation]
        data_smart_cacation  = data_smart[indx_Cacation]
        data_smart_mgcation  = data_smart[indx_Mgcation]
        data_smart_hco3anion = data_smart[indx_HCO3anion]
        data_smart_co2aq     = data_smart[indx_CO2aq]
        data_smart_hcation   = data_smart[indx_Hcation]
        plt.axes(xlim=(-0.01, 0.501), ylim=(-6, 1))
        plt.xlabel('Distance [m]', fontproperties=prop)
        plt.ylabel('Concentration [log10 molal]', fontproperties=prop)
        plt.title(titlestr(t), fontproperties=prop, fontsize=24)
        plt.plot(xcells, np.log10(data_class_cacation), label='Ca+2', **line('C0'))[0],
        plt.plot(xcells, np.log10(data_class_mgcation), label='Mg+2', **line('C1'))[0],
        plt.plot(xcells, np.log10(data_class_hco3anion), label='HCO3-', **line('C2'))[0],
        plt.plot(xcells, np.log10(data_class_co2aq), label='CO2(aq)', **line('red'))[0],
        plt.plot(xcells, np.log10(data_class_hcation), label='H+', **line('darkviolet'))[0],
        plt.plot(xcells[status[i-1]==0], np.log10(data_smart_cacation[status[i-1]==0]), 'o', **line_empty_marker('C0'))[0],
        plt.plot(xcells[status[i-1]==1], np.log10(data_smart_cacation[status[i-1]==1]), 'o', **line_filled_marker('C0'))[0],
        plt.plot(xcells[status[i-1]==0], np.log10(data_smart_mgcation[status[i-1]==0]), 'o', **line_empty_marker('C1'))[0],
        plt.plot(xcells[status[i-1]==1], np.log10(data_smart_mgcation[status[i-1]==1]), 'o', **line_filled_marker('C1'))[0],
        plt.plot(xcells[status[i-1]==0], np.log10(data_smart_hco3anion[status[i-1]==0]), 'o', **line_empty_marker('C2'))[0],
        plt.plot(xcells[status[i-1]==1], np.log10(data_smart_hco3anion[status[i-1]==1]), 'o', **line_filled_marker('C2'))[0],
        plt.plot(xcells[status[i-1]==0], np.log10(data_smart_co2aq[status[i-1]==0]), 'o', **line_empty_marker('red'))[0],
        plt.plot(xcells[status[i-1]==1], np.log10(data_smart_co2aq[status[i-1]==1]), 'o', **line_filled_marker('red'))[0],
        plt.plot(xcells[status[i-1]==0], np.log10(data_smart_hcation[status[i-1]==0]), 'o', **line_empty_marker('darkviolet'))[0],
        plt.plot(xcells[status[i-1]==1], np.log10(data_smart_hcation[status[i-1]==1]), 'o', **line_filled_marker('darkviolet'))[0],
        plt.plot([], [], 'o', label='Smart Prediction', **line_filled_marker('black'))
        plt.plot([], [], 'o', label='Learning', **line_empty_marker('black'))
        plt.legend(loc='upper right', prop=prop)
        plt.savefig(folder_general + '/aqueous-species-log10-{}.pdf'.format(i))
        plt.tight_layout()
        plt.close()



def plot_figures_aqueous_species():

    for i in plot_at_selected_steps:
        print("On aqueous-species figure at time step: {}".format(i))
        t = i * dt
        filearray_class = np.loadtxt(folder_class + '/' + files_class[i-1], skiprows=1)
        filearray_smart = np.loadtxt(folder_smart + '/' + files_smart[i-1], skiprows=1)
        data_class = filearray_class.T
        data_smart = filearray_smart.T
        data_class_cacation  = data_class[indx_Cacation]
        data_class_mgcation  = data_class[indx_Mgcation]
        data_class_hco3anion = data_class[indx_HCO3anion]
        data_class_co2aq     = data_class[indx_CO2aq]
        data_class_hcation   = data_class[indx_Hcation]
        data_smart_cacation  = data_smart[indx_Cacation]
        data_smart_mgcation  = data_smart[indx_Mgcation]
        data_smart_hco3anion = data_smart[indx_HCO3anion]
        data_smart_co2aq     = data_smart[indx_CO2aq]
        data_smart_hcation   = data_smart[indx_Hcation]
        plt.axes(xlim=(-0.01, 0.501), ylim=(0.5e-5, 2))
        plt.xlabel('Distance [m]', fontproperties=prop)
        plt.ylabel('Concentration [molal]', fontproperties=prop)
        plt.yscale('log')
        plt.title(titlestr(t), fontproperties=prop, fontsize=24)
        plt.plot(xcells, data_class_cacation, label='Ca+2', **line('C0'))[0],
        plt.plot(xcells, data_class_mgcation, label='Mg+2', **line('C1'))[0],
        plt.plot(xcells, data_class_hco3anion, label='HCO3-', **line('C2'))[0],
        plt.plot(xcells, data_class_co2aq, label='CO2(aq)', **line('red'))[0],
        plt.plot(xcells, data_class_hcation, label=r'H+', **line('darkviolet'))[0],
        plt.plot(xcells[status[i-1]==0], data_smart_cacation[status[i-1]==0], 'o', **line_empty_marker('C0'))[0],
        plt.plot(xcells[status[i-1]==1], data_smart_cacation[status[i-1]==1], 'o', **line_filled_marker('C0'))[0],
        plt.plot(xcells[status[i-1]==0], data_smart_mgcation[status[i-1]==0], 'o', **line_empty_marker('C1'))[0],
        plt.plot(xcells[status[i-1]==1], data_smart_mgcation[status[i-1]==1], 'o', **line_filled_marker('C1'))[0],
        plt.plot(xcells[status[i-1]==0], data_smart_hco3anion[status[i-1]==0], 'o', **line_empty_marker('C2'))[0],
        plt.plot(xcells[status[i-1]==1], data_smart_hco3anion[status[i-1]==1], 'o', **line_filled_marker('C2'))[0],
        plt.plot(xcells[status[i-1]==0], data_smart_co2aq[status[i-1]==0], 'o', **line_empty_marker('red'))[0],
        plt.plot(xcells[status[i-1]==1], data_smart_co2aq[status[i-1]==1], 'o', **line_filled_marker('red'))[0],
        plt.plot(xcells[status[i-1]==0], data_smart_hcation[status[i-1]==0], 'o', **line_empty_marker('darkviolet'))[0],
        plt.plot(xcells[status[i-1]==1], data_smart_hcation[status[i-1]==1], 'o', **line_filled_marker('darkviolet'))[0],
        plt.plot([], [], 'o', label='Smart Prediction', **line_filled_marker('black'))
        plt.plot([], [], 'o', label='Learning', **line_empty_marker('black'))
        plt.legend(loc='upper right', prop=prop)
        plt.savefig(folder_general + '/aqueous-species-{}.pdf'.format(i))
        plt.tight_layout()
        plt.close()


def plot_computing_costs():

    step = 20

    data_class = np.loadtxt('{}/profiling-steps.txt'.format(folder_class)).T
    data_smart = np.loadtxt('{}/profiling-steps.txt'.format(folder_smart)).T

    timings_transport = data_class[0] * 1e6  # in microseconds
    timings_equilibrium_class = data_class[1] * 1e6  # in microseconds
    timings_equilibrium_smart = data_smart[1] * 1e6  # in microseconds
    timings_equilibrium_smart_ideal = (data_smart[1] - data_smart[3] - data_smart[7]) * 1e6  # in microseconds

    plt.xlabel('Time Step', fontproperties=prop)
    plt.ylabel('Computing Cost [μs]', fontproperties=prop)
    plt.yscale('log')
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], timings_equilibrium_class[0:nsteps:step], label="Chemical Equilibrium (Conventional)", color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], timings_equilibrium_smart[0:nsteps:step], label="Chemical Equilibrium (Smart)", color='C1', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], timings_equilibrium_smart_ideal[0:nsteps:step], label="Chemical Equilibrium (Smart, Ideal)", color='C3', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], timings_transport[0:nsteps:step], label="Transport", color='C2', linewidth=1)
    leg = plt.legend(loc='lower right', bbox_to_anchor=(1, 0.53), prop=prop)
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    #plt.show()
    #plt.savefig(folder_general + '/computing-costs.pdf')
    plt.savefig(folder_general + '/computing-costs-with-ideal.pdf')
    plt.close()


def plot_on_demand_learning_countings():

    statuses = np.loadtxt(folder_smart + '/statuses.txt')
    learnings = ncells - np.sum(statuses, 1)
    learnings = np.where(learnings > 0, learnings, -1)  # replace 0's by -1 to improve figure

    plt.xlabel('Time Step', fontproperties=prop)
    plt.ylabel('On-demand learnings (at each step)', fontproperties=prop)
    plt.ylim(bottom=0, top=6)
    plt.ticklabel_format(style='plain', axis='x')

    plt.plot(learnings)
    plt.tight_layout()
    plt.savefig(folder_general + '/on-demand-learning-countings.pdf')
    plt.close()

def plot_on_demand_learnings_total():

    step = 1
    data_smart = np.loadtxt('{}/profiling-steps.txt'.format(folder_smart)).T
    total_learnings = data_smart[9]

    plt.xlabel('Time Step', fontproperties=prop)
    plt.ylabel('Accumulated on-demand learnings', fontproperties=prop)
    plt.ylim(bottom=0, top=max(total_learnings[0:nsteps:step]))
    plt.ticklabel_format(style='plain', axis='x')
    #plt.plot(time_steps[0:nsteps:step], total_learnings[0:nsteps:step], color='C0', linewidth=0.5)
    plt.plot(time_steps[0:nsteps:step], total_learnings[0:nsteps:step], color='C0', linewidth=1.5)
    plt.tight_layout()
    plt.savefig(folder_general + '/on-demand-learning-total.pdf')
    plt.close()

def plot_on_demand_learnings_total_initial_steps(nsteps_initial):

    step = 1
    data_smart = np.loadtxt('{}/profiling-steps.txt'.format(folder_smart)).T
    total_learnings = data_smart[9]

    plt.xlabel('Time Step', fontproperties=prop)
    plt.ylabel('Accumulated on-demand learnings (over all steps)', fontproperties=prop)
    plt.ylim(bottom=0, top=total_learnings[nsteps_initial] + 1)
    plt.ticklabel_format(style='plain', axis='x')
    xint = range(0, int(time_steps[nsteps_initial]))
    plt.xticks(xint)
    plt.plot(xint, total_learnings[0:nsteps_initial:step], color='C0', linewidth=1.5, marker='D')
    plt.tight_layout()
    plt.savefig(folder_general + '/on-demand-learning-total-initial-steps-'+ str(nsteps_initial) + '.pdf')
    plt.close()

def plot_computing_costs_vs_total_learnings():

    step = 40
    data_smart = np.loadtxt('{}/profiling-steps.txt'.format(folder_smart)).T

    timings_estimate = data_smart[2] * 1e6  # in microseconds
    timings_search = data_smart[3] * 1e6  # in microseconds
    timings_taylor = data_smart[4] * 1e6  # in microseconds

    plt.xlabel('Time Step', fontproperties=prop)
    plt.ylabel('Computing Cost [μs]', fontproperties=prop)
    #plt.xscale('log')
    plt.yscale('log')
    plt.ticklabel_format(style='plain', axis='x')
    #plt.plot(time_steps[0:nsteps:step], timings_estimate[0:nsteps:step], label="Estimation", color='C2', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], timings_search[0:nsteps:step], label="NN Search", color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], timings_taylor[0:nsteps:step], label="Taylor Extrapolation", color='C1', linewidth=1)

    leg = plt.legend(loc='lower right', prop=prop)
    for line in leg.get_lines(): line.set_linewidth(2.0)
    plt.tight_layout()
    plt.savefig(folder_general + '/search-traylor-vs-total-learnings.pdf')
    plt.close()

def plot_speedups():

    step = 80
    data_class = np.loadtxt('{}/profiling-steps.txt'.format(folder_class)).T
    data_smart = np.loadtxt('{}/profiling-steps.txt'.format(folder_smart)).T

    speedup = data_class[1] /data_smart[1]
    speedup_ideal = data_class[1] / (data_smart[1] - data_smart[3] - data_smart[7])

    plt.xlabel('Time Step', fontproperties=prop)
    plt.ylabel('Speedup [-]', fontproperties=prop)
    plt.ticklabel_format(style='plain', axis='x')
    plt.plot(time_steps[0:nsteps:step], speedup_ideal[0:nsteps:step], label="Speedup: Conventional vs. Smart (Ideal search)", color='C0', linewidth=1)
    plt.plot(time_steps[0:nsteps:step], speedup[0:nsteps:step], label="Speedup: Conventional vs. Smart ", color='C1', linewidth=1)

    leg = plt.legend(loc='lower right', prop=prop)
    for line in leg.get_lines():
        line.set_linewidth(2.0)
    plt.tight_layout()
    #plt.show()
    plt.savefig(folder_general + '/speedups.pdf')
    plt.savefig(folder_general + '/speedups.pdf')
    try: plt.savefig(folder_general + '/speedups.pdf')
    except PermissionError: print("""No permission to save plots to this directory""")
    plt.close()

def count_trainings(status):
    counter = [st for st in status if st == 0]
    return (len(counter), len(status))

if __name__ == '__main__':

    # Load the status data, where 0 stands for conventional learning and 1 for smart prediction
    status = np.loadtxt(folder_smart + '/statuses.txt')

    # Count the percentage of the trainings needed
    training_counter = count_trainings(np.array(status).flatten())
    title = "%2.2f percent is training (%d out of %d cells)" % (
        100 * training_counter[0] / training_counter[1], training_counter[0], training_counter[1])
    text = ["Number of chemical equilibrium trainings: %d" % training_counter[0],
            "Number of smart chemical equilibrium estimations: %d" % (training_counter[1] - training_counter[0]),
            ("Percentage of smart chemical kineics predictions: %2.2f" % (
                    100 - 100 * training_counter[0] / training_counter[1])) + "$\%$"]
    print(title)

    print("Collecting files...")
    # Collect files with results corresponding to smart or reference (classical) solver
    files_smart = [file for file in natsorted( os.listdir(folder_smart) ) if ("profiling" not in file and "statuses" not in file)]
    files_class = [file for file in natsorted( os.listdir(folder_class) ) if ("profiling" not in file)]

    plot_on_demand_learning_countings()
    plot_on_demand_learnings_total()
    plot_speedups()
    plot_computing_costs_vs_total_learnings()
    plot_computing_costs()
    plot_figures_ph()
    plot_figures_calcite_dolomite()
    plot_figures_log10_aqueous_species()

    tolerance = 1e-12
    calculate_error(tolerance)


'''
plt.plot(xcells, data_class_cacation, label='Ca+2', **line('C0'))[0],
plt.plot(xcells, data_class_mgcation, label='Mg+2', **line('C1'))[0],
plt.plot(xcells, data_class_hco3anion, label='HCO3-', **line('C2'))[0],
plt.plot(xcells, data_class_co2aq, label='CO2(aq)', **line('red'))[0],
plt.plot(xcells, data_class_hcation, label=r'H+', **line('darkviolet'))[0],
        
'''
