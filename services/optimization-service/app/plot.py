from matplotlib import pyplot as plt
import matplotlib as mpl
import io
import base64

def visualizeOptimizationLandscape(optimization_path):
    xs, ys, vals = [], [], []
    for k in range(len(optimization_path)):
        xs.append(optimization_path[k]["params"][0])
        ys.append(optimization_path[k]["params"][1])
        vals.append(optimization_path[k]["obj_value"])

    radius = (max(xs)-min(xs))/30
    cmap = mpl.colormaps["viridis"]
    norm = mpl.colors.Normalize(vmin=min(vals), vmax=max(vals))

    fig, ax = plt.subplots()
    ax.plot(xs, ys, zorder=-1, color="black")
    for i, val in enumerate(vals):
        circle = plt.Circle((xs[i], ys[i]), radius, alpha=1, color=cmap(norm(val)))
        ax.add_patch(circle)

    fig.subplots_adjust(bottom=0.15)
    cbar_ax = fig.add_axes([0.20, 0.05, 0.6, 0.035])
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                 cax=cbar_ax, orientation='horizontal', label='Objective Value')

    figure_base64 = figure_to_base64(fig)
    plt.close(fig)
    return figure_base64

def figure_to_base64(fig):
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format="png", bbox_inches="tight")
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode("utf-8")
    plt.savefig("temp_visualized.png", format="png", bbox_inches="tight")
    plt.close(fig)
    return my_base64_jpgData