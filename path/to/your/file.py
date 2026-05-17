# Placeholder for empty input in plot_metrics()

# This function now handles empty input gracefully by providing a default placeholder.

def plot_metrics(data):
    if not data:
        return "No data available."
    # Existing plotting logic here...
