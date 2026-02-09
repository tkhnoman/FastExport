import os
from krita import *
from PyQt5.QtWidgets import QFileDialog, QListWidget, QInputDialog, QMessageBox, QLabel


class FAST_EXPORT(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass
    
    def createActions(self, window):
        exportAction = window.createAction(
            "fastExport", "Fast Export"
        )
        
        exportAction.triggered.connect(self.fastExport)
        

    def fastExport(self):
        
        app = Krita.instance()
        doc = app.activeDocument()

        if doc is None:
            QMessageBox.information(app.activeWindow().qwindow(), "Error", "No active document found.")
        else:
            path = app.readSetting("fastExport", "directory", "")
    
            if not os.path.exists(path):
                path = None
    
            if not path:
                path = os.path.dirname(doc.fileName())
        
            file_name = os.path.basename(doc.fileName())
            filename_without_ext = os.path.splitext(file_name)[0]
            file_name_check = path + "/" + filename_without_ext + ".png"
    
            path = QFileDialog.getSaveFileName(None, "Select export target", file_name_check, "*.png", "",QFileDialog.DontConfirmOverwrite | QFileDialog.DontResolveSymlinks)[0]
            
            if path:
                exportParam = InfoObject()

                compression = app.readSetting("fastExport", "compression", "")
                if compression:                
                    exportParam.setProperty("compression", int(compression)) 
                else:
                    exportParam.setProperty("compression", 5)
                
                alpha = app.readSetting("fastExport", "alpha", "")
                if alpha:
                    exportParam.setProperty("alpha", alpha == 'True')
                else:
                    exportParam.setProperty("alpha", True)
                    
                indexed = app.readSetting("fastExport", "indexed", "")
                if indexed:
                    exportParam.setProperty("indexed", indexed == 'True')
                else:
                    exportParam.setProperty("indexed", False)
                    
                interlaced = app.readSetting("fastExport", "interlaced", "")
                if interlaced:
                    exportParam.setProperty("interlaced", interlaced == 'True')
                else:
                    exportParam.setProperty("interlaced", False)
                    
                forceSRGB = app.readSetting("fastExport", "forceSRGB", "")
                if forceSRGB:
                    exportParam.setProperty("forceSRGB", forceSRGB == 'True')
                else:
                    exportParam.setProperty("forceSRGB", True)
                    
                saveSRGBProfile = app.readSetting("fastExport", "saveSRGBProfile", "")
                if saveSRGBProfile:
                    exportParam.setProperty("saveSRGBProfile", saveSRGBProfile == 'True')
                else:
                    exportParam.setProperty("saveSRGBProfile", False)
                    
                transparencyFillcolor = app.readSetting("fastExport", "transparencyFillcolor", "")
                if transparencyFillcolor:
                    exportParam.setProperty("transparencyFillcolor", transparencyFillcolor)
            
            
                success = doc.exportImage(path, exportParam)
            
                if success:
                    app.writeSetting("fastExport", "directory", os.path.dirname(path))
                    app.writeSetting("fastExport", "compression", str(exportParam.property("compression")))
                    app.writeSetting("fastExport", "alpha", str(exportParam.property("alpha")))
                    app.writeSetting("fastExport", "indexed", str(exportParam.property("indexed")))
                    app.writeSetting("fastExport", "interlaced", str(exportParam.property("interlaced")))
                    app.writeSetting("fastExport", "forceSRGB", str(exportParam.property("forceSRGB")))
                    app.writeSetting("fastExport", "saveSRGBProfile", str(exportParam.property("saveSRGBProfile")))
                    app.writeSetting("fastExport", "transparencyFillcolor", str(exportParam.property("transparencyFillcolor")))
	
                    # print( str(exportParam.property("transparencyFillcolor")))
                    # print( str(exportParam.property("transparencyFillcolor")))



Krita.instance().addExtension(FAST_EXPORT(Krita.instance()))
