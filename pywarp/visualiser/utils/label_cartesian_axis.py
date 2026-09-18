def label_cartesian_axis(plane):
    """Names of the two axes left after fixing the given one-based axes."""
    if len(plane) != 2 or len(set(plane)) != 2 or any(p not in (1,2,3,4) for p in plane):
        raise ValueError("Select two distinct axes between 1 and 4")
    return tuple(label for i,label in enumerate(("t","x","y","z"),1) if i not in plane)
