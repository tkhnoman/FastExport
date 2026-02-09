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
            path = Application.readSetting("fastExport", "directory", "")
    
            if not os.path.exists(path):
                path = None
    
            if not path:
                path = os.path.dirname(doc.fileName())
        
            file_name = os.path.basename(doc.fileName())
            filename_without_ext = os.path.splitext(file_name)[0]
            file_name_check = path + "/" + filename_without_ext + ".png"
    
            path = QFileDialog.getSaveFileName(None, "Select export target", file_name_check, "*.png", "",QFileDialog.DontConfirmOverwrite | QFileDialog.DontResolveSymlinks)[0]
            
            if path:
                export_parameters = InfoObject()

                compression = Application.readSetting("fastExport", "compression", "")
                if compression:                
                    export_parameters.setProperty("compression", int(compression)) 
                else:
                    export_parameters.setProperty("compression", 5)
                
                alpha = Application.readSetting("fastExport", "alpha", "")
                if alpha:
                    export_parameters.setProperty("alpha", alpha == 'True')
                else:
                    export_parameters.setProperty("alpha", True)
                    
                indexed = Application.readSetting("fastExport", "indexed", "")
                if indexed:
                    export_parameters.setProperty("indexed", indexed == 'True')
                else:
                    export_parameters.setProperty("indexed", False)
                    
                interlaced = Application.readSetting("fastExport", "interlaced", "")
                if indexed:
                    export_parameters.setProperty("interlaced", interlaced == 'True')
                else:
                    export_parameters.setProperty("interlaced", False)
                    
                forceSRGB = Application.readSetting("fastExport", "forceSRGB", "")
                if forceSRGB:
                    export_parameters.setProperty("forceSRGB", forceSRGB == 'True')
                else:
                    export_parameters.setProperty("forceSRGB", True)
                    
                saveSRGBProfile = Application.readSetting("fastExport", "saveSRGBProfile", "")
                if saveSRGBProfile:
                    export_parameters.setProperty("saveSRGBProfile", saveSRGBProfile == 'True')
                else:
                    export_parameters.setProperty("saveSRGBProfile", False)
                    
                transparencyFillcolor = Application.readSetting("fastExport", "transparencyFillcolor", "")
                if transparencyFillcolor:
                    export_parameters.setProperty("transparencyFillcolor", transparencyFillcolor)
            
            
                success = doc.exportImage(path, export_parameters)
            
                if success:
                    Application.writeSetting("fastExport", "directory", os.path.dirname(path))
                    Application.writeSetting("fastExport", "compression", str(export_parameters.property("compression")))
                    Application.writeSetting("fastExport", "alpha", str(export_parameters.property("alpha")))
                    Application.writeSetting("fastExport", "indexed", str(export_parameters.property("indexed")))
                    Application.writeSetting("fastExport", "interlaced", str(export_parameters.property("interlaced")))
                    Application.writeSetting("fastExport", "forceSRGB", str(export_parameters.property("forceSRGB")))
                    Application.writeSetting("fastExport", "saveSRGBProfile", str(export_parameters.property("saveSRGBProfile")))
                    Application.writeSetting("fastExport", "transparencyFillcolor", str(export_parameters.property("transparencyFillcolor")))
	
                    # print( str(export_parameters.property("transparencyFillcolor")))
                    # print( str(exportParam.property("transparencyFillcolor")))



Krita.instance().addExtension(FAST_EXPORT(Krita.instance()))
