"""Collection of mesh generation routines for simple geometries.
"""
# Import modules
# ---------------
# NumPy
import numpy as np
# ============================================================================= mesh_ring_2d
def mesh_ring_2d(xc, yc, inner_radius, outer_radius, nrad, ncirc, start_angle = 0,
                end_angle = 2 * np.pi, closed=True, type='quad4'):
    """ Mesh a 2D ring.

    Parameters
    ----------
    xc : float
      x-coordinate of the center
    yc : float
      y-coordinate of the center
    zc : float
      z-coordinate of the center
    inner_radius : float
      Inner radius of the ring
    outer_radius : float
      Outer radius of the ring
    nrad : int
      Number of elements in the radial direction
    ncirc : int
      Number of elements in the circunferential direction
    start_angle : float
      Starting angle
    end_angle : float
      Ending angle
    closed : bool
      Closed or open ring
    type : str
      Element type
    """
    nelements_rad = nrad
    nelements_circ = ncirc

    npoints_rad = nelements_rad + 1
    if closed:
        npoints_circ = nelements_circ
        npoints_circ_virtual = nelements_circ + 1
        include_last = False
    else:
        npoints_circ = nelements_circ + 1
        npoints_circ_virtual = nelements_circ + 1
        include_last = True

    nelements = nelements_rad * nelements_circ
    npoints = npoints_rad * npoints_circ

    # Array of node numbers and elements
    nodeID = np.arange(1, npoints + 1, step=1).astype(np.int)
    elemID = np.arange(1, nelements + 1, step=1).astype(np.int)

    # Node coordinates
    coord = np.zeros((npoints, 3))
    angle = np.linspace(start_angle, end_angle, num=npoints_circ, endpoint=include_last)
    radius = np.linspace(inner_radius, outer_radius, num=npoints_rad, endpoint=True)
    radius, angle = np.meshgrid(radius, angle, indexing='xy')
    radius = radius.flatten()
    angle = angle.flatten()
    coord[:, 0] = xc + radius * np.cos(angle)
    coord[:, 1] = yc + radius * np.sin(angle)
    coord[:, 2] = 0.0

    # Table of connectivities: build an auxiliary array of node numbers
    if type.lower() == 'quad4':
        connect = np.zeros((nelements, 4)).astype(np.int)
        nodeIDaux = np.arange(1, npoints_circ_virtual*npoints_rad+1, step=1).astype(np.int)
        # If the ring is closed, so one must account for this in the connectivities
        if closed:
            nodeIDaux[npoints_rad * (npoints_circ_virtual - 1) :] = nodeIDaux[0:npoints_rad]
        nodeID_matrix = np.reshape(nodeIDaux, (npoints_circ_virtual, npoints_rad))
        connect[:, 0] = nodeID_matrix[0:npoints_circ_virtual - 1, 0:npoints_rad - 1].flatten()
        connect[:, 1] = nodeID_matrix[0:npoints_circ_virtual - 1, 1:npoints_rad].flatten()
        connect[:, 2] = nodeID_matrix[1:npoints_circ_virtual, 1:npoints_rad].flatten()
        connect[:, 3] = nodeID_matrix[1:npoints_circ_virtual, 0:npoints_rad - 1].flatten()

        # Boundary nodes
        if closed:
            outerNodes = nodeID_matrix[0:-1, -1]
            innerNodes = nodeID_matrix[0:-1, 0]
            startNodes = []
            endNodes = []
        else:
            outerNodes = nodeID_matrix[1:-1, -1]
            innerNodes = nodeID_matrix[1:-1, 0]
            startNodes = nodeID_matrix[0, :]
            endNodes = nodeID_matrix[-1, :]

    else:
        raise RuntimeError("Invalid element type for ring mesh generator: {0}.".format(type))

    return nodeID, coord, elemID, connect, outerNodes, innerNodes, startNodes, endNodes
# ============================================================================== mesh_box_2d
def mesh_box_2d(x0, y0, lx, ly, nx, ny, type='quad4'):
    """ Mesh a 2D rectangle.

    Parameters
    ----------
    x0 : float
      x-coordinate of bottom left corner
    y0 : float
      y-coordinate of bottom left corner
    z0 : float
      z-coordinate of rectangle
    lx : float
      Length in the x-direction
    ly : float
      Length in the y-direction
    nx : int
      Number of elements in the x-direction
    ny : int
      Number of elements in the y-direction
    type : str
      Element type
    """
    nElem = nx * ny
    nPoin = (nx + 1) * (ny + 1)

    # Array of node numbers
    nodeID = np.arange(1, nPoin + 1, step=1).astype(np.int)
    elemID = np.arange(1, nElem + 1, step=1).astype(np.int)

    # Node coordinates
    coord = np.zeros((nPoin, 3))
    x = np.linspace(x0, x0 + lx, num=nx + 1, endpoint=True)
    y = np.linspace(y0, y0 + ly, num=ny + 1, endpoint=True)
    x, y = np.meshgrid(x, y, indexing='xy')
    x = x.flatten()
    y = y.flatten()
    coord[:, 0] = x
    coord[:, 1] = y
    coord[:, 2] = 0

    # Table of connectivities: build an auxiliary array of node numbers
    # Note: the ring is closed, so one must account for this in the connectivities
    if type.lower() == 'quad4':
        connect = np.zeros((nElem, 4)).astype(np.int)
        nodeID_matrix = np.reshape(nodeID, (ny + 1, nx + 1))
        connect[:, 0] = nodeID_matrix[0:ny, 0:nx].flatten()
        connect[:, 1] = nodeID_matrix[0:ny, 1:nx+1].flatten()
        connect[:, 2] = nodeID_matrix[1:ny+1, 1:nx+1].flatten()
        connect[:, 3] = nodeID_matrix[1:ny+1, 0:nx].flatten()

        # Outer and inner nodes
        bottomNodes = nodeID_matrix[0, :]
        topNodes = nodeID_matrix[-1, :]
        rightNodes = nodeID_matrix[:, -1]
        leftNodes = nodeID_matrix[:, 0]

    return nodeID, coord, elemID, connect, bottomNodes, topNodes, leftNodes, rightNodes
# ==========================================================================================
