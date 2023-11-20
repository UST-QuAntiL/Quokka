from matplotlib import pyplot as plt
import matplotlib as mpl
import io
import base64
import numpy as np

def visualizeOptimizationLandscape(optimization_path, show=False):
    xs, ys, vals = np.array([]), np.array([]), np.array([])
    for k in range(len(optimization_path)):
        xs = np.append(xs, optimization_path[k]["params"][0])
        ys = np.append(ys, optimization_path[k]["params"][1])
        vals = np.append(vals, optimization_path[k]["obj_value"])

    # determine radii for each data point, progressively decreasing from 1/30 of the x-axis width to 1/150
    radius_start = (np.max(xs)-np.min(xs))/30
    radius_end = radius_start/5
    radii = np.linspace(radius_start, radius_end, len(vals))

    # prepare color map, coloring the data points according to their values
    cmap = mpl.colormaps["viridis"]
    norm = mpl.colors.Normalize(vmin=np.min(vals), vmax=np.max(vals))

    # prepare and arrange figure/axes
    fig = plt.figure(figsize=tuple(np.array([2,1])*5))
    gs = fig.add_gridspec(2, 2, height_ratios=[12,1], wspace=0.25, hspace=0.3)
    ax_path = fig.add_subplot(gs[0, 0])
    ax_progress = fig.add_subplot(gs[0, 1])
    ax_cbar = fig.add_subplot(gs[1, 0])

    # plot optimization path
    # -simple version
    #ax_path.plot(xs, ys, zorder=-1, color="black") # simple black line plot

    # -better version with arrows
    # 1) prepare vectors starting at the last point and ending just where the circle of the next point begins (considering its radius)
    vectors = []
    for x_pre, x_suc, y_pre, y_suc, radius in zip(xs[1:], xs[:-1], ys[1:], ys[:-1], radii[1:]):
        vector = np.array([x_pre-x_suc, y_pre-y_suc])
        vlen = np.sqrt(vector[0]**2+vector[1]**2)
        vectors.append(vector*(1-radius/vlen))
    vectors = np.array(vectors)

    # 2) plot the arrows
    ax_path.quiver(xs[:-1], ys[:-1], vectors[:,0], vectors[:,1], scale_units='xy', angles='xy', scale=1, headlength=4, headaxislength=4, color='lightgrey')

    #plot the data points as circles
    for i, (val, radius) in enumerate(zip(vals, radii)):
        circle = plt.Circle((xs[i], ys[i]), radius, alpha=1, color=cmap(norm(val)))
        ax_path.add_patch(circle)

    ax_path.set_title("Optimization Path")
    ax_path.set_xlabel("Parameter 1")
    ax_path.set_ylabel("Parameter 2")

    # add the color bar
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                 cax=cbar_ax, orientation='horizontal', label='Objective Value')

    # plot the optimization progress
    ax_progress.plot(vals)
    ax_progress.set_xlabel("Iteration")
    ax_progress.set_ylabel("Objective Value")
    ax_progress.set_title("Optimization Progress")

    if show:
        plt.show()

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

if __name__ == "__main__":
    # some sample data
    optimization_path = {0: {"obj_value": 10., "params": [2, 2]}, 1: {"obj_value": 7., "params": [1.9, 2.2]}, 2: {"obj_value": 6., "params": [2.2, 2.32]}, 3: {"obj_value": 4., "params": [2.4, 2.33]}, 4: {"obj_value": 4., "params": [2.45, 2.36]}, 5: {"obj_value": 3., "params": [2.5, 2.43]}, 6: {"obj_value": 1., "params": [2.52, 2.45]}}
    optimization_path = [{'obj_value': -5.308, 'params': [1.0, 1.0]}, {'obj_value': -5.698, 'params': [2.0, 1.0]}, {'obj_value': -5.1265, 'params': [2.0, 2.0]}, {'obj_value': -5.947, 'params': [2.563673134935923, 0.17400205995928264]}, {'obj_value': -5.6335, 'params': [3.559599141673872, 0.08382784467019955]}, {'obj_value': -5.4645, 'params': [2.287497995459434, -0.2428040008593454]}, {'obj_value': -5.6965, 'params': [2.7954289034190665, 0.2677531334186704]}, {'obj_value': -5.457, 'params': [2.404377022546706, 0.36667989619812447]}, {'obj_value': -5.645, 'params': [2.561777328584156, 0.049016437112986436]}, {'obj_value': -6.2845, 'params': [2.523302781780331, 0.22171458018293866]}, {'obj_value': -5.5845, 'params': [2.4665655522499126, 0.2479278742379147]}, {'obj_value': -5.5545, 'params': [2.564883359581954, 0.2683761869885682]}, {'obj_value': -5.7035, 'params': [2.4934138887793322, 0.21259226824051639]}, {'obj_value': -5.3315, 'params': [2.5325536334744334, 0.23430673519841222]}, {'obj_value': -5.7205, 'params': [2.529981815439055, 0.20758903118880653]}, {'obj_value': -5.169, 'params': [2.5155024200857974, 0.2212792484881905]}, {'obj_value': -5.3565, 'params': [2.5257698395835444, 0.21868598069503958]}, {'obj_value': -5.44, 'params': [2.524417391261267, 0.22545843311374503]}, {'obj_value': -5.6905, 'params': [2.521378542135232, 0.22137991758590245]}, {'obj_value': -5.5135, 'params': [2.523709292258193, 0.2226025123581607]}, {'obj_value': -5.4095, 'params': [2.523707458393871, 0.22082581072190832]}, {'obj_value': -5.436, 'params': [2.52281471836675, 0.22172916385275793]}, {'obj_value': -5.7235, 'params': [2.5234778682351253, 0.2215444350151469]}, {'obj_value': -5.5135, 'params': [2.523385716799007, 0.22194420254128502]}, {'obj_value': -5.696, 'params': [2.5232081117311416, 0.22168236866657381]}, {'obj_value': -5.5645, 'params': [2.5232866760221486, 0.22176191520753324]}]
    optimization_path = [{'obj_value': -5.0635, 'params': [1.0, 1.0]}, {'obj_value': -5.5225, 'params': [2.0, 1.0]}, {'obj_value': -5.798, 'params': [2.0, 2.0]}, {'obj_value': -5.758, 'params': [2.8574105030911796, 2.5146331015285845]}, {'obj_value': -5.799, 'params': [1.6950641643722189, 2.3962500929337263]}, {'obj_value': -5.464, 'params': [1.4895787740578967, 2.2538571353572694]}, {'obj_value': -5.69, 'params': [1.892961727279377, 2.549013159790239]}, {'obj_value': -5.4775, 'params': [1.5956529927418774, 2.3204713429104986]}, {'obj_value': -5.2785, 'params': [1.657174789360605, 2.4459556787488967]}, {'obj_value': -5.2475, 'params': [1.7968033380012676, 2.3236268146458503]}, {'obj_value': -5.2145, 'params': [1.6821782730638042, 2.4574072986022957]}, {'obj_value': -5.706, 'params': [1.7189480486914046, 2.3760976099644306]}, {'obj_value': -5.723, 'params': [1.6714627099478856, 2.3757675674777157]}, {'obj_value': -5.5805, 'params': [1.6936159525345356, 2.411807834012469]}, {'obj_value': -5.9445, 'params': [1.7008942443588688, 2.391049581074374]}, {'obj_value': -5.718, 'params': [1.7065779387221442, 2.3856894715013457]}, {'obj_value': -5.8135, 'params': [1.6982939884291928, 2.3881345410810493]}, {'obj_value': -5.6915, 'params': [1.7082712300809635, 2.3936215915537487]}, {'obj_value': -5.441, 'params': [1.699540501349754, 2.387385407371099]}, {'obj_value': -5.4445, 'params': [1.702368556099737, 2.39233063616935]}, {'obj_value': -5.4995, 'params': [1.6991995493071825, 2.392020511528843]}, {'obj_value': -5.5175, 'params': [1.700949113303161, 2.3900745612205463]}, {'obj_value': -5.1915, 'params': [1.7004722336459412, 2.3912951936499396]}, {'obj_value': -5.015, 'params': [1.7013663505460546, 2.3911742178551516]}, {'obj_value': -5.6455, 'params': [1.7008510409581543, 2.390809293515516]}, {'obj_value': -5.6695, 'params': [1.7009880867995988, 2.391084129537695]}, {'obj_value': -5.7065, 'params': [1.7008769701272084, 2.3910965022947392]}]
    visualizeOptimizationLandscape(optimization_path, show=True)
