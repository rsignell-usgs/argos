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

""" Some simple Config Tree Items
"""
import logging
import numpy as np

from libargos.config.abstractcti import AbstractCti, AbstractCtiEditor, InvalidInputError
from libargos.qt import Qt, QtCore, QtGui, getQApplicationInstance
from libargos.utils.misc import NOT_SPECIFIED


logger = logging.getLogger(__name__)

# Use setIndexWidget()?
 

        



class ChoiceCti(AbstractCti):
    """ Config Tree Item to store a choice between strings.
    """
    def __init__(self, nodeName, data=NOT_SPECIFIED, defaultData=0, choices=None):
        """ Constructor
            data and defaultData are used to store the currentIndex.
            choices must be a list of string.
                    
            For the (other) parameters see the AbstractCti constructor documentation.
        """
        super(ChoiceCti, self).__init__(nodeName, data=data, defaultData=defaultData)
        self.choices = [] if choices is None else choices
        
    
    def _enforceDataType(self, data):
        """ Converts to int so that this CTI always stores that type. 
        """
        return int(data)

    
    @property
    def displayValue(self):
        """ Returns the string representation of data for use in the tree view. 
        """
        return str(self.choices[self.data])
    
    
    @property
    def debugInfo(self):
        """ Returns the string with debugging information
        """
        return repr(self.choices)
    
    
    def createEditor(self, delegate, parent, _option):
        """ Creates a QComboBox for editing. 
            :type option: QStyleOptionViewItem
        """
        comboBox = QtGui.QComboBox()
        comboBox.addItems(self.choices)
        
        ctiEditor = AbstractCtiEditor(self, delegate, comboBox, parent=parent) 

        comboBox.activated.connect(ctiEditor.commitAndClose)        
        return ctiEditor
        
    
    def finalizeEditor(self, ctiEditor, delegate):
        """ Is called when the editor is closed. Disconnect signals.
        """
        comboBox = ctiEditor.mainEditor
        comboBox.activated.disconnect(ctiEditor.commitAndClose)      
        
        
    def setEditorValue(self, ctiEditor, index):
        """ Provides the combo box an data that is the current index.
        """
        comboBox = ctiEditor.mainEditor
        comboBox.setCurrentIndex(index)        
        
        
    def getEditorValue(self, ctiEditor):
        """ Gets data from the combo box editor widget.
        """
        comboBox = ctiEditor.mainEditor
        data = comboBox.currentIndex()
        return data
                


class ColorCti(AbstractCti):
    """ Config Tree Item to store a color. 
    """
    def __init__(self, nodeName, data=NOT_SPECIFIED, defaultData=''):
        """ Constructor. 
            For the (other) parameters see the AbstractCti constructor documentation.
        """
        super(ColorCti, self).__init__(nodeName, data=data, defaultData=defaultData)
        

    def _enforceDataType(self, data):
        """ Converts to str so that this CTI always stores that type. 
        """
        qColor = QtGui.QColor(data)    # TODO: store a RGB string?
        if not qColor.isValid():
            raise ValueError("Invalid color specification: {!r}".format(data))
        return qColor
        
        
    def _dataToJson(self, qColor):
        """ Converts data or defaultData to serializable json dictionary or scalar.
            Helper function that can be overridden; by default the input is returned.
        """
        return qColor.name()
    
    def _dataFromJson(self, json):
        """ Converts json dictionary or scalar to an object to use in self.data or defaultData.
            Helper function that can be overridden; by default the input is returned.
        """
        return QtGui.QColor(json) 

    
    @property
    def displayValue(self):
        """ Returns a string with the RGB value in hexadecimal (e.g. '#00FF88') 
        """
        return self._data.name().upper()    
        
    
    @property
    def debugInfo(self):
        """ Returns the string with debugging information
        """
        return ""
    
    
    def createEditor(self, delegate, parent, _option):
        """ Creates a QSpinBox for editing. 
            :type option: QStyleOptionViewItem
        """
        lineEditor = QtGui.QLineEdit(parent)
        regExp = QtCore.QRegExp(r'#?[0-9A-F]{6}', Qt.CaseInsensitive)
        validator = QtGui.QRegExpValidator(regExp, parent=lineEditor)
        lineEditor.setValidator(validator)
            
        return lineEditor
        
        
    def setEditorValue(self, lineEditor, qColor):
        """ Provides the editor widget with a data to manipulate.
        """
        lineEditor.setText(qColor.name().upper())
        
        
    def getEditorValue(self, lineEditor):
        """ Gets data from the editor widget.
        """
        text = lineEditor.text()
        if not text.startswith('#'):
            text = '#' + text

        validator = lineEditor.validator()
        if validator is not None:
            state, text, _ = validator.validate(text, 0)
            if state != QtGui.QValidator.Acceptable:
                raise InvalidInputError("Invalid input: {!r}".format(text))

        return text
    


                