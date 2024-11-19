# smoothing.py


def apply_smoothing(data, smoothing_window):
    """Applies a rolling mean smoothing to the data over the specified window."""
    if smoothing_window:
        return data.rolling(year=smoothing_window, center=True).mean()
    return data
