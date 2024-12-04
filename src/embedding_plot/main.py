import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Embedding dimensions: Formaility, Negativity , Activity
words = ["Hello", "Shutup", "Go away", "Run", "Walk"]

# Embedding dimensions
embeddings = {
    "Hello": [0.5, 0.6, 0.3],
    "Shutup": [0.2, 1.0, 0.2],
    "Go away": [0.2, 0.9, 0.4],
    "Run": [0.2, 0.5, 0.9],
    "Walk": [0.3, 0.5, 0.7]
}

x = [embeddings[word][0] for word in words]
y = [embeddings[word][1] for word in words]
z = [embeddings[word][2] for word in words]
# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot each point
for i in range(len(words)):
    ax.scatter(x[i], y[i], z[i], label=words[i])

# Label axes
ax.set_xlabel('Formality')
ax.set_ylabel('Negativity')
ax.set_zlabel('Activity Level')

# Add a legend
ax.legend()

try:
    # Show the plot
    plt.show()
except KeyboardInterrupt:
    print("Caught Ctrl-C")