import matplotlib.pyplot as plt
import seaborn as sns

def plot_1d(data, label="Parameter", use_kde=False):
    plt.figure()

    if use_kde:
        sns.kdeplot(data, fill=True)
        plt.ylabel("Density")
    else:
        plt.hist(data, bins=10)
        plt.ylabel("Frequency")

    plt.xlabel(label)
    plt.title(f"1D Distribution of {label}")

    plt.savefig(f"plots/{label}_1d.png")
    plt.show()


def plot_2d(x, y, x_label="X", y_label="Y", use_kde=False):
    plt.figure()

    if use_kde:
        sns.scatterplot(x=x, y=y)
        sns.kdeplot(x=x, y=y, fill=True, alpha=0.3)
    else:
        plt.scatter(x, y)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f"{x_label} vs {y_label}")

    plt.savefig(f"plots/{x_label}_vs_{y_label}.png")
    plt.show()


def plot_2d(x, y, x_label="X", y_label="Y"):
    plt.figure()
    
    plt.scatter(x, y)
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f"{x_label} vs {y_label}")
    
    plt.show()
    plt.savefig("plots/plot_name.png")