import matplotlib.pyplot as plt

def plot_1d(data, label="Parameter"):
    plt.figure()
    
    plt.hist(data, bins=10)
    
    plt.xlabel(label)
    plt.ylabel("Frequency")
    plt.title(f"1D Distribution of {label}")
    
    plt.show()


def plot_2d(x, y, x_label="X", y_label="Y"):
    plt.figure()
    
    plt.scatter(x, y)
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f"{x_label} vs {y_label}")
    
    plt.show()
    plt.savefig("plots/plot_name.png")