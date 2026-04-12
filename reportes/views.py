from django.shortcuts import render
from reservas.models import Reserva


# =========================
# REPORTE
# =========================
def reporte_reservas(request):
    reservas = Reserva.objects.all().order_by('-creada')

    fecha = request.GET.get('fecha')

    if fecha:
        reservas = reservas.filter(fecha__icontains=fecha)

    return render(request, 'reportes/reporte.html', {
        'reservas': reservas,
        'fecha': fecha
    })


# =========================
# EXPORTAR PDF
# =========================
def exportar_pdf(request):
    from django.http import HttpResponse
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.lib import colors

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_reservas.pdf"'

    doc = SimpleDocTemplate(response)

    data = [["ID", "Usuario", "Cancha", "Fecha", "Horario", "Total"]]

    for r in Reserva.objects.all():
        usuario_nombre = r.usuario.username if r.usuario else "Anónimo"
        data.append([r.id, usuario_nombre, r.cancha_nombre, r.fecha, r.horario, f"${r.total}"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.black),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.grey)
    ]))

    doc.build([table])
    return response


# =========================
# EXPORTAR EXCEL
# =========================
def exportar_excel(request):
    import openpyxl
    from django.http import HttpResponse

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reservas"

    ws.append(["ID", "Usuario", "Cancha", "Fecha", "Horario", "Total"])

    for r in Reserva.objects.all():
        usuario_nombre = r.usuario.username if r.usuario else "Anónimo"
        ws.append([r.id, usuario_nombre, r.cancha_nombre, r.fecha, r.horario, r.total])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reporte_reservas.xlsx"'

    wb.save(response)
    return response


# =========================
# EXPORTAR TXT
# =========================
def exportar_txt(request):
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="reporte_reservas.txt"'

    for r in Reserva.objects.all():
        usuario_nombre = r.usuario.username if r.usuario else "Anónimo"
        response.write(f"{r.id} - {usuario_nombre} - {r.cancha_nombre} - {r.fecha} - {r.horario} - ${r.total}\n")

    return response