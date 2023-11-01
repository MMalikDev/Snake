import matplotlib.pyplot as plt

plt.ion()


def plot(scores, mean_scores, record):
    plt.figure("Progress Tracker", facecolor="black")

    plt.clf()
    plt.style.use("dark_background")
    plt.title(f"High Score: {record}")

    plt.xlabel(f"Number of Games ({len(scores)} Total)")
    plt.ylabel("Score")

    plt.plot(scores)
    plt.plot(mean_scores)

    plt.ylim(ymin=0)

    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))

    plt.show()
    plt.pause(0.1)
