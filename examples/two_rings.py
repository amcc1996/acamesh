# ==========================================================================================
# Two rings colliding
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
from acamesh import mesh_ring_2d

title = os.path.splitext(os.path.basename(__file__))[0]

# Model geometry
inner_radius = 19.4 / 2
outer_radius = 20 / 2
thickness = outer_radius - inner_radius
xc = 0
yc = 21

# Mesh geometry
nodeId_1, coord_1, elemId_1, toc_1, outer_1, inner_1, start_1, end_1 \
  = mesh_ring_2d(xc, yc, inner_radius, outer_radius, nrad=1, ncirc=200)
nodeId_2, coord_2, elemId_2, toc_2, outer_2, inner_2, start_2, end_2 \
  = mesh_ring_2d(0, 0, inner_radius, outer_radius, nrad=1, ncirc=200)

# Update element and node numbers
nNod_1 = len(nodeId_1)
nElem_1 = np.shape(toc_1)[0]
nodeId_2 = nodeId_2 + nNod_1
toc_2 = toc_2 + nNod_1
outer_2 = outer_2 + nNod_1
elemId_2 = elemId_2 + nElem_1

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
    dat.write("\n\nMATERIALS 2\n1 ELASTIC\n0.1\n1000 0.16667\n2 ELASTIC\n0.1\n1000 0.167")
    dat.write("\n\nNUMBER_OF_STEPS 1")
    dat.write("\n\nSTEP_1")
    dat.write("\n\nINCREMENTS 1500")
    dat.write("\n1500")
    dat.write("\n 0.025 1e-6 15")
    dat.write("\n\nDYNAMICS ON")
    dat.write("\n\nMASS_MATRIX CONSISTENT")
    dat.write("\n\nINTEGRATOR NEWMARK")
    dat.write("\n\nCONTACT ON")
    dat.write("\n\nTANGENTIAL_CONTACT FRICTIONLESS")
    dat.write("\n\nNORMAL_PDASS_PARAMETER\n2E3")
    dat.write("\n\nNGAUSS_DUAL_BASIS 5")
    dat.write("\n\nNGAUSS_MORTAR_INTEGRALS 5")
    dat.write("\n\nSEARCH_ALG BRUTE_FORCE")
    dat.write("\n\nSEGMENT-BASED_INTEGRATION")
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
    dat.write("\n\nMORTAR_CANDIDATES {0}".format(len(outer_2)))
    for i in outer_2:
        dat.write("\n {0}".format(i))
    dat.write("\n\nNON-MORTAR_CANDIDATES {0}".format(len(outer_1)))
    for i in outer_1:
        dat.write("\n {0}".format(i))
    dat.write("\n\nINITIAL_VELOCITY NODE")
    for i in nodeId_1:
        velx = 0.0
        vely = -2
        dat.write("\n{0} {1} {2}".format(i, velx, vely))
    for i in nodeId_2:
        velx = 0.0
        vely = 0
        dat.write("\n{0} {1} {2}".format(i, velx, vely))
    dat.write("\n\nINITIAL_DISPLACEMENT NODE")
    for i in nodeId_1:
        dispx = 0.0
        dispy = 0.0
        dat.write("\n{0} {1} {2}".format(i, dispx, dispy))
    for i in nodeId_2:
        dispx = outer_radius / 2
        dispy = 0.0
        dat.write("\n{0} {1} {2}".format(i, dispx, dispy))
