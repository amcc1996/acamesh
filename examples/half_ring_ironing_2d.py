# ==========================================================================================
# Ironing with a half-ring in 2D (Neo-Hookean)
#
# António Manuel Couto Carneiro
# @ CM2S                                                Department of Mechanical Engineering
#                                          Faculty of Engineering of the University of Porto
#                               ------------------------------------------------------------
#                               Computational Multi-Scale Modelling of Solids and Structures
# ==========================================================================================
# Import modules
# --------------
# Operating system directives
import os
# NumPy library
import numpy as np
# Meshing library
from acamesh import mesh_ring_2d, mesh_box_2d

title = os.path.splitext(os.path.basename(__file__))[0]

# Model geometry
dx = 9
dy = 3
xb = -dx / 2
yb = -dy

inner_radius = 2.8
outer_radius = 3.0
thickness = outer_radius - inner_radius
xc = -dx * 0.3
yc = outer_radius * 1.01

# Mesh geometry
nodeId_1, coord_1, elemId_1, toc_1, outer_1, inner_1, start_1, end_1 \
  = mesh_ring_2d(xc, yc, inner_radius, outer_radius, nrad=1, ncirc=20, closed=False,
                 start_angle=np.pi, end_angle=2*np.pi)
nodeId_2, coord_2, elemId_2, toc_2, bot_2, top_2, left_2, right_2 \
  = mesh_box_2d(xb, yb, dx, dy, nx=20, ny=3)

# Update element and node numbers
nNod_1 = len(nodeId_1)
nElem_1 = np.shape(toc_1)[0]
nodeId_2 = nodeId_2 + nNod_1
toc_2 = toc_2 + nNod_1
top_2 = top_2 + nNod_1
bot_2 = bot_2 + nNod_1
elemId_2 = elemId_2 + nElem_1

# Material 1
rho_1 = 0.1
E_1 = 1000
v_1 = 0.3
mu_1 = E_1 / (2 * (1 + v_1))
K_1 = E_1 / (3 * (1 - 2 * v_1))

# Material 2
rho_2 = 0.1
E_2 = 1.0
v_2 = 0.3
mu_2 = E_2 / (2 * (1 + v_2))
K_2 = E_2 / (3 * (1 - 2 * v_2))

with open(title + ".dat", "w") as dat:
    dat.write("TITLE\n{0}".format(title))
    dat.write("\n\nANALYSIS_TYPE 2")
    dat.write("\n\nLARGE_STRAIN_FORMULATION ON")
    dat.write("\n\nSOLUTION_ALGORITHM 2")
    dat.write("\n\nSOLVER PARDISO")
    dat.write("\n\nPARALLEL_SOLVER 1")
    dat.write("\n\nVTK_OUTPUT ASCII EVERY 1")
    dat.write("\n\nMAX_CONSECUTIVE_INCREMENT_CUTS 4")
    dat.write("\n\nELEMENT_GROUPS 2\n1 1 1\n2 1 2")
    dat.write("\n\nELEMENT_TYPES 1\n1 QUAD4_FBAR \n4 GP")
    dat.write("\n\nMATERIALS 2\n1 OGDEN\n{0}\n1\n{1} 2\n{2}\n2 OGDEN\n{3}\n1\n{4} 2\n{5}".format(rho_1, mu_1, K_1, rho_2, mu_2, K_2))
    dat.write("\n\nDYNAMICS ON")
    dat.write("\n\nMASS_MATRIX CONSISTENT")
    dat.write("\n\nINTEGRATOR NEWMARK")
    dat.write("\n\nDAMPING_MATRIX RAYLEIGH")
    dat.write("\n\nRAYLEIGH_DAMPING\n0.5 0.5")
    dat.write("\n\nCONTACT ON")
    dat.write("\n\nTANGENTIAL_CONTACT FRICTIONLESS")
    dat.write("\n\nNORMAL_PDASS_PARAMETER\n2E3")
    dat.write("\n\nNGAUSS_DUAL_BASIS 5")
    dat.write("\n\nNGAUSS_MORTAR_INTEGRALS 5")
    dat.write("\n\nSEARCH_ALG BRUTE_FORCE")
    dat.write("\n\nSEGMENT-BASED_INTEGRATION")
    dat.write("\n\nNUMBER_OF_STEPS 2")
    dat.write("\n\nSTEP_1")
    dat.write("\n\nINCREMENTS 10")
    dat.write("\n10")
    dat.write("\n 0.1 1e-6 15")
    dat.write("\n\nNODES_WITH_PRESCRIBED_DISPLACEMENTS {0}\nFIXED".format(len(bot_2)))
    for i in bot_2:
        dat.write("\n{0} 11 0.0 0.0 0.0".format(i))
    dat.write("\n\nNODES_WITH_PRESCRIBED_DISPLACEMENTS {0}\nLINEAR\n0 -1.4".format(len(start_1) + len(end_1)))
    for i in start_1:
        dat.write("\n{0} 01 0.0 0.0 0.0".format(i))
    for i in end_1:
        dat.write("\n{0} 01 0.0 0.0 0.0".format(i))
    dat.write("\n\nNODES_WITH_PRESCRIBED_DISPLACEMENTS {0}\nFIXED".format(len(start_1) + len(end_1)))
    for i in start_1:
        dat.write("\n{0} 10 0.0 0.0 0.0".format(i))
    for i in end_1:
        dat.write("\n{0} 10 0.0 0.0 0.0".format(i))
    dat.write("\n\nSTEP_2")
    dat.write("\n\nINCREMENTS 100")
    dat.write("\n100")
    dat.write("\n 0.01 1e-6 15")
    dat.write("\n\nNODES_WITH_PRESCRIBED_DISPLACEMENTS {0}\nFIXED".format(len(bot_2)))
    for i in bot_2:
        dat.write("\n{0} 11 0.0 0.0 0.0".format(i))
    dat.write("\n\nNODES_WITH_PRESCRIBED_DISPLACEMENTS {0}\nLINEAR\n1 4".format(len(start_1) + len(end_1)))
    for i in start_1:
        dat.write("\n{0} 10 0.0 0.0 0.0".format(i))
    for i in end_1:
        dat.write("\n{0} 10 0.0 0.0 0.0".format(i))
    dat.write("\n\nNODES_WITH_PRESCRIBED_DISPLACEMENTS {0}\nUNIFORM".format(len(start_1) + len(end_1)))
    for i in start_1:
        dat.write("\n{0} 01 0.0 -1.4 0.0".format(i))
    for i in end_1:
        dat.write("\n{0} 01 0.0 -1.4 0.0".format(i))
    dat.write("\n\nNODE_COORDINATES {0} CARTESIAN".format(len(nodeId_1) + len(nodeId_2)))
    for i in range(len(nodeId_1)):
        dat.write("\n{0} {1} {2} {3}".format(nodeId_1[i], coord_1[i, 0], coord_1[i, 1],
                                             coord_1[i, 2]))
    for i in range(len(nodeId_2)):
        dat.write("\n{0} {1} {2} {3}".format(nodeId_2[i], coord_2[i, 0], coord_2[i, 1],
                                             coord_2[i, 2]))
    dat.write("\n\nELEMENTS {0}".format(len(elemId_1) + len(elemId_2)))
    for i in range(len(elemId_1)):
        dat.write("\n{0} 1 ".format(elemId_1[i]))
        for j in toc_1[i, :]:
            dat.write("{0} ".format(j))
    for i in range(len(elemId_2)):
        dat.write("\n{0} 2 ".format(elemId_2[i]))
        for j in toc_2[i, :]:
            dat.write("{0} ".format(j))
    dat.write("\n\nNUMBER_OF_CANDIDATE_INTERFACES 1")
    dat.write("\nLINE2")
    dat.write("\n\nNON-MORTAR_CANDIDATES {0}".format(len(top_2)))
    for i in top_2:
        dat.write("\n {0}".format(i))
    dat.write("\n\nMORTAR_CANDIDATES {0}".format(len(outer_1)))
    for i in outer_1:
        dat.write("\n {0}".format(i))
    dat.write("\n\nINITIAL_VELOCITY NODE")
    for i in nodeId_1:
        velx = 0.0
        vely = 0.0
        dat.write("\n{0} {1} {2}".format(i, velx, vely))
    for i in nodeId_2:
        velx = 0.0
        vely = 0
        dat.write("\n{0} {1} {2}".format(i, velx, vely))
    dat.write("\n\nINITIAL_DISPLACEMENT GLOBAL\n0.0 0.0 0.0")
