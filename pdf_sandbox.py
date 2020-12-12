from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

def drawHeader(canvasObj, document_number, eff_date, revision_version,
               page_number, total_pages, left=75, right=580,top=760,linespace=15):
    canvasObj.setLineWidth(.3)
    canvasObj.setFont('Helvetica', 8)
    canvasObj.drawString(left,top,'Document No.')
    canvasObj.drawString(left + 95,top,'Rev.')
    canvasObj.drawString(left + 275,top,'Effective Date')
    canvasObj.drawString(right-30,top,'Page No.')
    canvasObj.line(left,top-5,right,top-5)
    canvasObj.setFont('Helvetica-Bold', 10)
    canvasObj.drawString(left,top-linespace,document_number)
    canvasObj.drawString(left+95,top-linespace,revision_version)
    canvasObj.drawString(left + 275,top-linespace,eff_date)
    canvasObj.drawString(right-35,top-linespace,"%i of %i"%(page_number, total_pages))
    return

def drawFooter(canvasObj):
    canvasObj.setFont('Helvetica', 8)
    canvasObj.drawString(215,25,'This is a controlled document. Verify version before use.')

def drawTitle(canvasObj, title, x=75,y=715):
    canvasObj.setFont('Helvetica-Bold', 12)
    canvasObj.drawString(x,y,title)

def drawBox(canvasObj, left,right,top,bottom):
    canvasObj.setLineWidth(.8)
    canvasObj.line(left,top,left,bottom)
    canvasObj.line(right,top,right,bottom)
    canvasObj.line(left,top,right,top)
    canvasObj.line(left,bottom,right,bottom)

def drawHorizontalLines(canvasObj, left, right, ypositions):
    canvasObj.setLineWidth(.8)
    for y in ypositions:
        canvasObj.line(left,y,right,y)

def drawVerticalLines(canvasObj, top, bottom, xpositions):
    canvasObj.setLineWidth(.8)
    for x in xpositions:
        canvasObj.line(x,top,x,bottom)

def mARC_Run_sheet(mycanvas, run, linespace = 15):
    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']

    drawHeader(mycanvas, "TSF-18-046", date, "B", 25, 35)
    drawFooter(mycanvas)
    drawTitle(mycanvas,title)

    ### Draw lines
    drawBox(mycanvas, 75,580,705,50)
    drawHorizontalLines(mycanvas, 75,580,[705-i*linespace for i in range(1,5)])
    drawHorizontalLines(mycanvas, 75,580,[580-i*linespace for i in range(0,3)])
    drawVerticalLines(mycanvas, 705,705-4*linespace,[330])
    drawVerticalLines(mycanvas, 580,580-2*linespace,[330])
    drawBox(mycanvas, 78,577,510,420)
    drawHorizontalLines(mycanvas, 78,577,[480-i*linespace for i in range(0,4)])
    drawVerticalLines(mycanvas, 510,420,[77+ 55*(i+1) for i in range(0,6)])
    drawVerticalLines(mycanvas, 495,420,[577- 55*(i+1) for i in range(0,2)])
    drawHorizontalLines(mycanvas, 77+6*55,577,[495])
    drawHorizontalLines(mycanvas, 75,580,[250,180])
    drawHorizontalLines(mycanvas, 205,315,[370-i*12 for i in range(0,4)])
    drawHorizontalLines(mycanvas, 205+110+15,315+110+15,[370-i*12 for i in range(0,4)])
    drawHorizontalLines(mycanvas, 205+220+30,315+220+30,[370-i*12 for i in range(0,4)])

    ### Insert labels & run data
    mycanvas.setFont('Helvetica', 10)
    mycanvas.drawString( 77,694,"DATE        %s"%run.date.date())
    mycanvas.drawString(332,694,"TIME            %s"%run.date.time())
    mycanvas.drawString( 77,679,"TEST        %s"%run.test.name)
    mycanvas.drawString(332,679,"RUN(S)        %s"%run.name)
    mycanvas.drawString( 77,664,"OPERATOR      %s"%run.operator.name)
    mycanvas.drawString(332,664,"TEST ENGINEER      %s"%run.test_engineer.name)
    mycanvas.drawString(332,649,"PI            %s"%run.principle_investigator.name)

    mycanvas.setFont('Helvetica', 10)
    mycanvas.drawString(77,634,"RUN OBJECTIVES")
    P=Paragraph(run.objective,style)
    w,h = P.wrap(503, 60)
    mycanvas.setFont('Helvetica', 9)
    P.drawOn(mycanvas,77,604)

    mycanvas.setFont('Helvetica', 10)
    mycanvas.drawString( 77,569,"Nozzle exit diameter (cm)      %s"%run.nozzle.diameter)
    mycanvas.drawString(332,569,"# Disks         %s"%run.disks.count())
    mycanvas.drawString( 77,554,"Total Cathode Time (h:m:s)        %s"%("TBD"))
    mycanvas.drawString(332,554,"Cathode type:  %s         # Cathode starts: %s"%(run.cathode.type,"TBD"))

    mycanvas.drawString(260,533,"DESIRED TEST CONDITIONS")
    drawHorizontalLines(mycanvas, 260,397,[530])
    mycanvas.drawString( 77,516,"Main gas: %s"%run.gassettings.plasma_gas)
    mycanvas.drawString(295,516,"Shield gas: %s"%run.gassettings.shield_gas)
    mycanvas.drawString(500,516,"Purge gas: %s"%run.gassettings.purge_gas)

    mycanvas.drawString(80,499,"Cond."); mycanvas.drawString(80,489,"ID")
    mycanvas.drawString(135,499,"Current"); mycanvas.drawString(135,489,"(A)")
    mycanvas.drawString(190,499,"Main"); mycanvas.drawString(190,489,"(g/s)")
    mycanvas.drawString(245,499,"Shield"); mycanvas.drawString(245,489,"(g/s)")
    mycanvas.drawString(300,499,"Purge"); mycanvas.drawString(300,489,"(g/s)")
    mycanvas.drawString(355,499,"Z"); mycanvas.drawString(355,489,"(in)")
    mycanvas.drawString(472,499,"Duration (s)")
    mycanvas.drawString(428,485,"SW")
    mycanvas.drawString(488,485,"L1")
    mycanvas.drawString(543,485,"L2")

    y=469
    mycanvas.setFont('Helvetica', 8)
    conditioninstance_set = run.conditioninstance_set.all()
    print(conditioninstance_set)
    for cond in conditioninstance_set:
        mycanvas.drawString(80,y,cond.name)
        mycanvas.drawString(135,y,str(cond.condition.current))
        mycanvas.drawString(190,y,str(cond.condition.plasma_gas_flow))
        mycanvas.drawString(245,y,str(cond.condition.shield_gas_flow))
        mycanvas.drawString(300,y,str(None))
        mycanvas.drawString(355,y,str(None))
        mycanvas.drawString(428,y,str(cond.sweep_insertion))
        mycanvas.drawString(488,y,str(cond.l1_insertion))
        mycanvas.drawString(543,y,str(cond.l2_insertion))
        y-= 15

    mycanvas.setFont('Helvetica', 10)
    mycanvas.drawString(270,405,"MODELS AND SENSORS")
    drawHorizontalLines(mycanvas, 270,388,[402])
    mycanvas.drawString(255,385,"SW")
    mycanvas.drawString(380,385,"L1")
    mycanvas.drawString(505,385,"L2")
    mycanvas.drawString(77,372,"Material or Sensor Type")
    mycanvas.drawString(77,360,"S/N")
    mycanvas.drawString(77,348,"Size")
    mycanvas.drawString(77,336,"Sensor Limits")

    mycanvas.drawString(290,315,"PROCEDURE")
    drawHorizontalLines(mycanvas, 290,355,[312])
    P2=Paragraph(run.objective,style)
    w,h = P2.wrap(503, 60)
    P2.drawOn(mycanvas,77,280)

    mycanvas.drawString(295,240,"CAMERAS")
    drawHorizontalLines(mycanvas, 295,345,[237])
    y = 215
    mycanvas.drawString(77,y,"Camera")
    mycanvas.drawString(175,y,"Lens")
    mycanvas.drawString(265,y,"Filter")
    mycanvas.drawString(355,y,"Mode")
    mycanvas.setFont('Helvetica', 6)
    cs = run.camerasettings_set.all()
    for cam in cs:
        y-= 12
        mycanvas.drawString(77,y,cam.camera.name)
        mycanvas.drawString(175,y,str(cam.lens))
        mycanvas.drawString(265,y,str(cam.opticalfilter))
        mycanvas.drawString(355,y,str(cam.record_type))
    
    mycanvas.setFont('Helvetica', 10)
    mycanvas.drawString(255,165,"ADDITIONAL DIAGNOSTICS")
    drawHorizontalLines(mycanvas, 255,385,[162])
    y = 150
    mycanvas.drawString(77,y,"Purpose")
    mycanvas.drawString(175,y,"Sensor model")
    mycanvas.drawString(335,y,"Units")
    mycanvas.setFont('Helvetica', 6)
    dgs = run.diagnostics.all()
    for dg in dgs:
        y-= 10
        mycanvas.drawString(77,y,dg.name)
        mycanvas.drawString(175,y,str(dg.sensor))
        mycanvas.drawString(335,y,str(dg.units))
    
    ### End first page, start new page
    mycanvas.showPage()
    drawHeader(mycanvas, "TSF-18-046", date, "B", 26, 35)
    drawFooter(mycanvas)
    drawBox(mycanvas, 75,580,730,50)
    drawHorizontalLines(mycanvas, 75,580,[710,350,275])
    drawVerticalLines(mycanvas, 710,350,[330])

    mycanvas.drawString(77,713,"Total Arc-On Duration ")
    drawHorizontalLines(mycanvas, 160,215,[713])
    mycanvas.drawString(218,713,"min:sec")

    mycanvas.setFont('Helvetica', 10)
    mycanvas.drawString(270,335,"POST-TEST PHOTO")
    drawHorizontalLines(mycanvas, 270,365,[332])

    mycanvas.setFont('Helvetica', 10)
    mycanvas.drawString(245,260,"NOTES (include notes from checklist)")
    drawHorizontalLines(mycanvas, 245,412,[257])

    mycanvas.drawString(100,690,"ARC HEATER/CHAMBER COOLING")
    drawHorizontalLines(mycanvas, 100,265,[687])
    mycanvas.drawString(125,678,"(DISTILLED WATER)")
    drawHorizontalLines(mycanvas, 125,220,[675])
    plist = ["HCW-TI-101 Temp (F)", "HCW-ST-101 Conduct. (uS)", "HCW-PI-130 Arc supply (PSIG)",
             "HCW-PI-133 Arc return (PSIG)", "HCW-PI-140 Spare supply (PSIG)", 
             "HCW-PI-146 Spare return (PSIG)", "HCW-PI-147 Chamber supply (PSIG)"]
    y=660
    mycanvas.setFont('Helvetica', 7)
    for p in plist:
        mycanvas.drawString(95,y,p)
        y -= 10
    if run.distilledwaterloop:
        mycanvas.drawString(250,660,str(run.distilledwaterloop.temperature))
        mycanvas.drawString(250,650,str(run.distilledwaterloop.conductivity))
        mycanvas.drawString(250,640,str(run.distilledwaterloop.arc_supply_pressure))
        mycanvas.drawString(250,630,str(run.distilledwaterloop.arc_return_pressure))
        mycanvas.drawString(250,620,str(run.distilledwaterloop.spare_supply_pressure))
        mycanvas.drawString(250,610,str(run.distilledwaterloop.spare_return_pressure))
        mycanvas.drawString(250,600,str(run.distilledwaterloop.chamber_supply_pressure))
    drawHorizontalLines(mycanvas, 230,290,[658-10*i for i in range(0,7)])

    mycanvas.setFont('Helvetica', 10)
    mycanvas.drawString(100,560,"VACUUM SYSTEM COOLING")
    drawHorizontalLines(mycanvas, 100,235,[557])
    mycanvas.drawString(125,548,"(TAP WATER)")
    drawHorizontalLines(mycanvas, 125,185,[545])
    plist = ["VPW-PI-220 heat ex. Press (PSIG)", "VPW-FI-220 heat ex. Press (GPM)", "VPW-PI-230 vac. pump Press. (PSIG)",
             "VPW-FI-230 vac. pump Flow (GPM)", "VPW-TI-280 vac. pump exit T (F)"]
    y=535
    mycanvas.setFont('Helvetica', 7)
    for p in plist:
        mycanvas.drawString(95,y,p)
        y -= 10
    if run.vacuumwaterloop:
        mycanvas.drawString(250,535,str(run.vacuumwaterloop.ex_pressure))
        mycanvas.drawString(250,525,str(run.vacuumwaterloop.ex_flow))
        mycanvas.drawString(250,515,str(run.vacuumwaterloop.vac_pressure))
        mycanvas.drawString(250,505,str(run.vacuumwaterloop.vac_flow))
        mycanvas.drawString(250,495,str(run.vacuumwaterloop.vac_exit_temperature))
    drawHorizontalLines(mycanvas, 230,290,[533-10*i for i in range(0,5)])

    mycanvas.setFont('Helvetica', 10)
    mycanvas.drawString(420,690,"SENSOR COOLING")
    drawHorizontalLines(mycanvas, 420,510,[687])
    mycanvas.drawString(420,678,"(DISTILLED WATER)")
    drawHorizontalLines(mycanvas, 420,515,[675])
    plist = ["SKW-TI-401 Temp (F)", "SKW-ST-401 Conduct. (uS)", "SKW-PI-440 sensor supply (PSIG)"]
    y=660
    mycanvas.setFont('Helvetica', 7)
    for p in plist:
        mycanvas.drawString(340,y,p)
        y -= 10
    if run.sensorwaterloop:
        mycanvas.drawString(490,660,str(run.sensorwaterloop.temperature))
        mycanvas.drawString(490,650,str(run.sensorwaterloop.conductivity))
        mycanvas.drawString(490,640,str(run.sensorwaterloop.arc_supply_pressure))
    drawHorizontalLines(mycanvas, 475,535,[658-10*i for i in range(0,3)])

from django.conf import settings
import mARC.settings as app_settings

settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)
import django
django.setup()
from data.models import Run
from system.models import ConditionInstance, Condition

run = Run.objects.filter(name="Run_14").first()
date = "05/13/2019"
title = "Appendix A: mARC Run Sheet"

mycanvas = canvas.Canvas('form.pdf', pagesize=letter)
mARC_Run_sheet(mycanvas,run)
print(run.date.time())
mycanvas.save()