# -*- coding: utf-8 -*-

# This file is part of Argos.
# 
# Argos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Argos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Argos. If not, see <http://www.gnu.org/licenses/>.

""" Contains the StringCti and StringCtiEditor classes 
"""
import logging
import numpy as np

from libargos.config.abstractcti import AbstractCti, AbstractCtiEditor
from libargos.qt import QtGui
from libargos.utils.misc import NOT_SPECIFIED

logger = logging.getLogger(__name__)


class IntCti(AbstractCti):
    """ Config Tree Item to store an integer. It can be edited using a QSpinBox.
    """
    def __init__(self, nodeName, data=NOT_SPECIFIED, defaultData=0, 
                 minValue = None, maxValue = None, stepSize = 1):
        """ Constructor.
            
            :param minValue: minimum data allowed when editing (use None for no minimum)
            :param maxValue: maximum data allowed when editing (use None for no maximum)
            :param stepSize: steps between values when ediging (default = 1)
                    
            For the (other) parameters see the AbstractCti constructor documentation.
        """
        super(IntCti, self).__init__(nodeName, data=data, defaultData=defaultData)
        
        self.minValue = minValue
        self.maxValue = maxValue
        self.stepSize = stepSize
    
    
    def _enforceDataType(self, data):
        """ Converts to int so that this CTI always stores that type. 
        """
        return int(data)
    
    
    @property
    def debugInfo(self):
        """ Returns the string with debugging information
        """
        return "min = {}, max = {}, step = {}".format(self.minValue, self.maxValue, self.stepSize)
    
    
    def createEditor(self, delegate, parent, option):
        """ Creates a StringCtiEditor. 
            For the parameters see the AbstractCti constructor documentation.
        """
        return IntCtiEditor(self, delegate, parent=parent, 
                            minValue = self.minValue, maxValue = self.maxValue, 
                            stepSize = self.stepSize)
        

        
class IntCtiEditor(AbstractCtiEditor):
    """ A CtiEditor which contains a QSpinbox for editing IntCti objects. 
    """
    def __init__(self, cti, delegate, parent=None, 
                 minValue = None, maxValue = None, stepSize = 1):
        """ See the AbstractCtiEditor for more info on the parameters 
        """
        super(IntCtiEditor, self).__init__(cti, delegate, parent=parent)
        
        spinBox = QtGui.QSpinBox(parent)

        if minValue is None:
            spinBox.setMinimum(np.iinfo('i').min)
        else: 
            spinBox.setMinimum(minValue) 

        if maxValue is None:
            spinBox.setMaximum(np.iinfo('i').max)
        else: 
            spinBox.setMaximum(maxValue) 

        spinBox.setSingleStep(stepSize)
        
        self.spinBox = self.addSubEditor(spinBox, isFocusProxy=True)
        
    
    def setData(self, data):
        """ Provides the main editor widget with a data to manipulate.
        """
        self.spinBox.setValue(data)

        
    def getData(self):
        """ Gets data from the editor widget.
        """
        return self.spinBox.value()
    