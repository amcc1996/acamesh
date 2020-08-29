# acamesh
Academic mesh generation package

## Overview
`acamesh` is a simple finite element mesh generation package in Python. It focuses on structured and quasi-structured meshes of simple geometries commonly used for benchmark and debugging tests.
This package aims at compiling and storing some meshing routines for such simple scenarios that have been extremely useful over the last years on the course of my research.

## Installation
Change directory into the `acamesh` root path and run
```
sudo pip3 install -e .
```

## Usage
`acamesh` provides standalone mesh generation routines that cna receive different inputs and provide different outputs, so beware to read the short documentation of the subroutine first.
The current implementations are:

* `mesh_ring_2d` : generates a structured finite element mesh on a 2D open or closed ring
* `mesh_box_2d` : generated a structured finite element mesh on a 2D rectangle
