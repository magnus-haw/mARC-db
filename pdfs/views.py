import io
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from .utils import mARC_Run_sheet
from data.models import Run
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create your views here.
def DownloadRunSheetPDF(request,run_pk):
    # Retrieve run object
    print(run_pk)
    run = get_object_or_404(Run, pk=run_pk)
    
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    mycanvas = canvas.Canvas(buffer, pagesize=letter)
    mARC_Run_sheet(mycanvas,run)
    mycanvas.save()
    
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='%s_%s.pdf'%(run.name, run.date.date()))
