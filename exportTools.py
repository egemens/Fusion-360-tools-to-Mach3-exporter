# Author-Egemen Can Senkardes 2022
# Description-

import adsk.core
import adsk.fusion
import adsk.cam
import traceback
import json
from collections import OrderedDict
from operator import getitem


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        targetPath = "/Users/egemens/Desktop"
        filename = "M700.m1s"
        targetPath = targetPath + "/" + filename

        toolList = open(
            '/Users/egemens/Library/Application Support/Autodesk/Autodesk Fusion 360/BDWRRV5P6SHD/W.login/M/D20190508192672131/CAMTools/___CLEANUP.json')
        toolList = json.load(toolList)
        toolList = toolList["data"]
        text = "hello"
        myList = {}
        logger = UiLogger(True)

        filteredList = []

        for index, tool in enumerate(toolList):
            toolNumber = tool["post-process"]["number"]
            desc = tool["description"]
            length = tool["geometry"]["LB"]
            filteredList.append(
                {"toolNumber": toolNumber, "length": length, "desc": desc})

        sortedToolList = sorted(filteredList, key=lambda d: d['toolNumber'])
        # logger.print(sortedToolList)

        machToolList = ""

        machToolList += "\' Tool List generated by Autodesk Fusion 360"
        machToolList += "\n"
        machToolList += "\' Script by Egemen Senkardes 2022"
        machToolList += "\n"

        for tool in sortedToolList:
            machToolList += "SetToolDesc("
            machToolList += str(tool["toolNumber"])
            machToolList += ", \""
            machToolList += str(tool["desc"])
            machToolList += "\")"
            machToolList += "\n"
            machToolList += "SetToolParam("
            machToolList += str(tool["toolNumber"])
            machToolList += ", 2, "
            machToolList += str(tool["length"])
            machToolList += ")"
            machToolList += "\n"

        #I use a
        machToolList = machToolList.replace("mm", "milimeter")
        machToolList = machToolList.replace("x", " by ")

        f = open(targetPath, "w")
        f.write(machToolList)
        f.close()

        ui.messageBox(machToolList)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
