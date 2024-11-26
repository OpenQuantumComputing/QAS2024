import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MaxNLocator

import numpy as np

def __plot_landscape(A, extent, fig):
    if not fig:
        fig = plt.figure(figsize=(6, 6), dpi=80, facecolor="w", edgecolor="k")
    _ = plt.xlabel(r"$\gamma$")
    _ = plt.ylabel(r"$\beta$")
    ax = fig.gca()
    _ = plt.title("Expectation value")
    im = ax.imshow(A, interpolation="nearest", origin="lower", extent=extent)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    _ = plt.colorbar(im, cax=cax)


def plot_E(qaoa_instance, fig=None):
    angles = qaoa_instance.landscape_p1_angles
    dgamma = (qaoa_instance.gamma_grid[1]-qaoa_instance.gamma_grid[0])/2
    dbeta = (qaoa_instance.gamma_grid[1]-qaoa_instance.gamma_grid[0])/2
    extent = [
        angles["gamma"][0]-dgamma,
        angles["gamma"][1]+dgamma,
        angles["beta"][0]-dbeta,
        angles["beta"][1]+dbeta,
    ]
    return __plot_landscape(qaoa_instance.exp_landscape(), extent, fig=fig)


def plot_Var(qaoa_instance, fig=None):
    angles = qaoa_instance.landscape_p1_angles
    dgamma = (qaoa_instance.gamma_grid[1]-qaoa_instance.gamma_grid[0])/2
    dbeta = (qaoa_instance.gamma_grid[1]-qaoa_instance.gamma_grid[0])/2
    extent = [
        angles["gamma"][0]-dgamma,
        angles["gamma"][1]+dgamma,
        angles["beta"][0]-dbeta,
        angles["beta"][1]+dbeta,
    ]
    return __plot_landscape(qaoa_instance.var_landscape(), extent, fig=fig)


def plot_ApproximationRatio(
    qaoa_instance, maxdepth, mincost, maxcost, label, style="", fig=None, shots=None
):
    if not shots:
        exp = np.array(qaoa_instance.get_Exp())
    else:
        exp = []
        for p in range(1, qaoa_instance.current_depth + 1):
            ar, sp = __apprrat_successprob(qaoa_instance, p, shots=shots)
            exp.append(ar)
        exp = np.array(exp)

    if not fig:
        ax = plt.figure().gca()
    else:
        ax = fig.gca()
    plt.hlines(1, 1, maxdepth, linestyles="solid", colors="black")
    plt.plot(
        np.arange(1, maxdepth + 1),
        (maxcost - exp) / (maxcost - mincost),
        style,
        label=label,
    )
    plt.ylim(0, 1.01)
    plt.xlim(1 - 0.25, maxdepth + 0.25)
    _ = plt.ylabel("appr. ratio")
    _ = plt.xlabel("depth")
    _ = plt.legend(loc="lower right", framealpha=1)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
