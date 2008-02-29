#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "matplotlib2DViewer.py"
 #                                    created: 9/14/04 {2:48:25 PM} 
 #                                last update: 10/5/07 {10:11:32 AM} { 2:45:36 PM}
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  See the file "license.terms" for information on usage and  redistribution
 #  of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##
 
__docformat__ = 'restructuredtext'

from fipy.tools import numerix
from matplotlibViewer import MatplotlibViewer

class Matplotlib2DGridContourViewer(MatplotlibViewer):
    """
    Displays a contour plot of a 2D `CellVariable` object.    

    The `Matplotlib2DGridContourViewer` plots a 2D `CellVariable` using Matplotlib_.

    .. _Matplotlib: http://matplotlib.sourceforge.net/


    """


    def __init__(self, vars, limits = None, title = None):
        """
        Creates a `Matplotlib2DViewer`.
        
        >>> from fipy import *
        >>> from fipy.tools.numerix import *
        >>> mesh = Grid2D(nx=50, ny=100, dx=0.1, dy=0.01)
        >>> x, y = mesh.getCellCenters()
        >>> xyVar = CellVariable(mesh=mesh, name="x y", value=x * y)
        >>> k = Variable(name="k")
        >>> viewer = Matplotlib2DGridContourViewer(vars=sin(k * xyVar), 
        ...                                        limits={'ymin':0.1, 'ymax':0.9, 'datamin':-0.9, 'datamax':2.0},
        ...                                        title="Matplotlib2DGridContourViewer test")
        >>> for kval in range(10):
        ...     k.setValue(kval)
        ...     viewer.plot()
        >>> viewer._promptForOpinion()
        >>> del viewer

        :Parameters:
          - `vars`: A `CellVariable` object.
          - `limits`: A dictionary with possible keys `'xmin'`, `'xmax'`, 
            `'ymin'`, `'ymax'`, `'datamin'`, `'datamax'`. Any limit set to 
            a (default) value of `None` will autoscale.
          - `title`: displayed at the top of the Viewer window

        """
        MatplotlibViewer.__init__(self, vars = vars, limits = limits, title = title)
        
        self.colorbar = None
        self._plot()
        
        import pylab
        # colorbar will not automatically update
        # http://sourceforge.net/mailarchive/forum.php?thread_id=10159140&forum_id=33405
        ##from fipy.tools.numerix import array
        ##self.colorbar = pylab.colorbar(array(self.vars[0]))
        self.colorbar = pylab.colorbar()
        
    def _getSuitableVars(self, vars):
        from fipy.meshes.numMesh.grid2D import Grid2D
        from fipy.variables.cellVariable import CellVariable
        vars = [var for var in MatplotlibViewer._getSuitableVars(self, vars) \
          if (isinstance(var.getMesh(), Grid2D) and isinstance(var, CellVariable))]
        if len(vars) == 0:
            from fipy.viewers import MeshDimensionError
            raise MeshDimensionError, "The mesh must be a Grid2D instance"
        # this viewer can only display one variable
        return [vars[0]]
        
    def _plot(self):
##         pylab.clf()
        
##         ## Added garbage collection since matplotlib objects seem to hang
##         ## around and accumulate.
##         import gc
##         gc.collect()

        mesh = self.vars[0].getMesh()
        shape = mesh.getShape()
        X, Y = mesh.getCellCenters()
        X = X.reshape(shape, order="FORTRAN")
        Y = Y.reshape(shape, order="FORTRAN")
        Z = self.vars[0].getValue().reshape(shape, order="FORTRAN")
        
        zmin, zmax = self._autoscale(vars=self.vars,
                                     datamin=self._getLimit(('datamin', 'zmin')),
                                     datamax=self._getLimit(('datamax', 'zmax')))

        numberOfContours = 10
        smallNumber = 1e-7
        diff = zmax - zmin
        
        if diff < smallNumber:            
            V = numerix.arange(numberOfContours + 1) * smallNumber / numberOfContours + zmin
        else:
            V = numerix.arange(numberOfContours + 1) * diff / numberOfContours + zmin

        import pylab
        pylab.jet()

        pylab.contourf(X, Y, Z, V)

        pylab.xlim(xmin=self._getLimit('xmin'),
                   xmax=self._getLimit('xmax'))

        pylab.ylim(ymin=self._getLimit('ymin'),
                   ymax=self._getLimit('ymax'))

if __name__ == "__main__": 
    import fipy.tests.doctestPlus
    fipy.tests.doctestPlus.execButNoTest()

        
