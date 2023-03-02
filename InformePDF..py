def pdfInformeFacturaProyecto(request, id):
    proyecto = Proyecto.objects.get(id=id)
    cliente = Clientes.objects.all()
    #estado = EstadoFactura.objects.all()
    #detalleFactura = DetalleFactura.objects.all()
    #ingresos = Ingreso.objects.all()
    #ingreso = ingresos.first()
    
    # Asignar el id del proyecto a una variable y filtrar los ingresos por proyecto
    detallesIngreso = Ingreso.objects.filter(Proyecto=id).order_by('Factura')
    
    # Filtrar las facturas por proyecto y quitar las anuladas
    FacProyecto = Factura.objects.filter(Proyecto=id).exclude(EstadoFactura=9)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=InfFacturaProyecto.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setPageSize(landscape(A4))
    data = []

    # Establecer estilos para las tablas
    styles = getSampleStyleSheet()
    styleBH = styles['Normal']
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 8
    contador1 = Paragraph('''#''', styleBH)
    factura1 = Paragraph('''Factura''', styleBH)
    cliente = Paragraph('''Cliente''', styleBH)
    fecha1 = Paragraph('''Fecha de Factura''', styleBH)
    valFactura = Paragraph('''Val. Factura antes de impuestos''', styleBH)
    fecha2 = Paragraph('''Fecha del Ingreso''', styleBH)
    ingNeto = Paragraph('''Val. Neto Recibido''', styleBH)
    estado1 = Paragraph('''Estado Factura''', styleBH)
    AIU1 = Paragraph('''AIU''', styleBH)

    styles = getSampleStyleSheet()
    styleN = styles['BodyText']
    styleN.alignment = TA_LEFT
    styleN.fontSize = 6.6

    styles = getSampleStyleSheet()
    styleC = styles['Normal']
    styleC.alignment = TA_RIGHT
    styleC.fontSize = 6.6

    styles = getSampleStyleSheet()
    styleD = styles['Normal']
    styleD.alignment = TA_CENTER
    styleD.fontSize = 6.6

    styles = getSampleStyleSheet()
    styleF = styles['Normal']
    styleF.alignment = TA_RIGHT
    styleF.fontSize = 7
    styleF.fontName = "Helvetica-Bold"

    styles = getSampleStyleSheet()
    styleG = styles['Normal']
    styleG.alignment = TA_CENTER
    styleG.fontSize = 10
    styleG.fontName = "Helvetica-Bold"

    
    
    Contador=len(FacProyecto)
    
   
    if Contador <=18:
        Contador=18
    

    Num=round(int(Contador/18))
    s=int(Contador/Num)   
    if s>18:
        s=18

    Contador_new=[0]
    x=0

    while(x+s < Contador):
        x=x+s
        Contador_new.append(x)

    contador = 0
    #TotalFac = 0
    ValtotalIngreso=0
    TotalFacturacion=0
    SaldoXFacturar=0
    NoFactura2 = str(0)
    
    for i in range(len(Contador_new)):

        frame2=Frame(10,10,800,401, showBoundary=0)
        c.setLineWidth(.3)

        c.setFont('Helvetica',8)
        c.setFillColor(HexColor('#548236'))
        c.drawString(55,530, 'GEDIC INGENIERIA S.A.S  -  Informe de facturas por proyecto')
        c.drawString(770,530, str(date.today()))
        c.setStrokeColor(HexColor('#548236'))
        c.line(55, 525, 815, 525)
        
    
        
        c.setFillColor(HexColor('#404040'))
        c.rect(55,445,760,70,fill=True, stroke=False)

        c.setFillColor(HexColor('#548236'))
        c.setFont('Helvetica-Bold',16)
        #Cliente=str(proyecto.Clientes)
        #c.drawCentredString(420.945, 498, Cliente)
        

        c.setFillColor(HexColor('#FFFFFF'))
        c.setFont('Helvetica',12)
        #c.drawCentredString(420.945, 483, str(proyecto.Clientes.documento))
        #c.drawCentredString(420.945, 468, str(proyecto.NombreProyecto +' ' + proyecto.CodProyecto))
        c.setFont('Helvetica',10)

        c.setFillColor(HexColor('#FFFFFF'))
        #c.drawString(60,453, str('Valor del contrato antes de impuestos $'+proyectoValM))
        #c.drawRightString(805,453, str(proyecto.EstadoProyecto))

        # if proyecto.fechaInicio is None:
        #     c.drawString(480,453, str(''))
        # else:
        #     c.drawString(450,453, str('Inicio:'))
        #     c.drawString(480,453, str(proyecto.fechaInicio))
        
        # if proyecto.fechaFinReal is None:
        #     c.drawString(600,453, str(''))
        # else:
        #     c.drawString(580,453, str('Fin:'))
        #     c.drawString(600,453, str(proyecto.fechaFinReal))

        c.setFillColor(HexColor('#FFFFFF'))
        c.setFont('Helvetica',12)
        proyectoVal=round((proyecto.Valor),2)
        
        TotalFacturacionFac=0
        NoFactura2 = str(0)
        ValtotalIngresoM=''
        TotalFacturacionFacM=''
        SaldoXFacturarM=''

        for p in FacProyecto:
            valor = p.ValorFactura
            TotalFacturacionFac = valor + TotalFacturacionFac
            TotalFacturacionFacM= "{:>15,}".format(TotalFacturacionFac).replace(',','~').replace('.',',').replace('~','.')
            TotalFacturacionFacM=Paragraph(str(TotalFacturacionFacM),styleF)

            SaldoXFacturar=round((proyectoVal-TotalFacturacionFac),2)
            SaldoXFacturarM= "{:>15,}".format(SaldoXFacturar).replace(',','~').replace('.',',').replace('~','.')

        c.setFillColor(HexColor('#000000'))

        frame=Frame(35,10,800,440, showBoundary=0)
        data1=[[contador1,factura1,cliente,fecha1,valFactura,fecha2,ingNeto,estado1,AIU1]]
        
        
        

        if(i==len(Contador_new)-1):
   
            for row in detallesIngreso[Contador_new[i]:]:
                
                if row.Factura is None:
                    facturaNum= Paragraph ('Sin Factura', styleD)
                    fecha=Paragraph ('Sin Factura', styleD)
                   
                    valorIng=(row.ValorIngreso)
                    ValtotalIngreso=valorIng + ValtotalIngreso
                    ValtotalIngresoM= "{:>15,}".format(ValtotalIngreso).replace(',','~').replace('.',',').replace('~','.')
                    ValtotalIngresoM=Paragraph(str(ValtotalIngresoM),styleF)

                    valorIng= "{:>15,}".format(valorIng).replace(',','~').replace('.',',').replace('~','.')
                    valorIng=Paragraph(str(valorIng),styleC)

                    
                    clientes= Paragraph (str(row.Clientes), styleD)
                    
                    proyecto=(row.Proyecto)
                    
                    valor = 0
                    
                    NoFactura1 = str(facturaNum)
                    if NoFactura1  != NoFactura2:

                        TotalFacturacion = valor + TotalFacturacion
                    
                        TotalFacturacionM= "{:>15,}".format(TotalFacturacion).replace(',','~').replace('.',',').replace('~','.')
                        TotalFacturacionM=Paragraph(str(TotalFacturacionM),styleF)

                        SaldoXFacturar=round((proyectoVal-TotalFacturacionFac),2)
                        SaldoXFacturarM= "{:>15,}".format(SaldoXFacturar).replace(',','~').replace('.',',').replace('~','.')

                    else:
                        TotalFacturacionFac = 0
                        TotalFacturacionFacM= "{:>15,}".format(TotalFacturacionFac).replace(',','~').replace('.',',').replace('~','.')
                        TotalFacturacionFacM=Paragraph(str(TotalFacturacionFacM),styleF)
                        
                        SaldoXFacturar=round((proyectoVal-TotalFacturacionFac),2)
                        SaldoXFacturarM= "{:>15,}".format(SaldoXFacturar).replace(',','~').replace('.',',').replace('~','.')
                    
                        
                    NoFactura2 = NoFactura1

                    valorM= "{:>15,}".format(valor).replace(',','~').replace('.',',').replace('~','.')
                    valorM=Paragraph(str(valorM),styleC)
                    
                    
                    EstadoFac = Paragraph ('Sin Factura',styleD)

                    
                    fechaIngreso=(row.fechaIngreso)
                    fechaIngreso=Paragraph(str(fechaIngreso),styleD)
                    
                    AIU=Paragraph ('No',styleD)
                    

                else:
                    facturaNum= Paragraph (str(row.Factura.NumFactura), styleD)
               
                    fecha=Paragraph (str(row.Factura.fechaFactura), styleD)
                   
                    valorIng=(row.ValorIngreso)
                    ValtotalIngreso=valorIng + ValtotalIngreso
                    ValtotalIngresoM= "{:>15,}".format(ValtotalIngreso).replace(',','~').replace('.',',').replace('~','.')
                    ValtotalIngresoM=Paragraph(str(ValtotalIngresoM),styleF)

                    valorIng= "{:>15,}".format(valorIng).replace(',','~').replace('.',',').replace('~','.')
                    valorIng=Paragraph(str(valorIng),styleC)

                    
                    clientes= Paragraph (str(row.Factura.Clientes), styleD)
                    
                    proyecto=(row.Proyecto)
                    
                    valor = round((row.Factura.ValorFactura),2)
                    
                    NoFactura1 = str(facturaNum)
                    if NoFactura1  != NoFactura2:

                        TotalFacturacion = valor + TotalFacturacion
                    
                        TotalFacturacionM= "{:>15,}".format(TotalFacturacion).replace(',','~').replace('.',',').replace('~','.')
                        TotalFacturacionM=Paragraph(str(TotalFacturacionM),styleF)
                    NoFactura2 = NoFactura1

                    valorM= "{:>15,}".format(valor).replace(',','~').replace('.',',').replace('~','.')
                    valorM=Paragraph(str(valorM),styleC)
                    
                    
                    EstadoFac = Paragraph (str(row.Factura.EstadoFactura),styleD)

                    
                    fechaIngreso=(row.fechaIngreso)
                    fechaIngreso=Paragraph(str(fechaIngreso),styleD)
                    
                    AIU=(row.Factura.AIU)
                    if AIU == True:
                        AIU=Paragraph(str("Si"),styleD)
                    else:
                        AIU=Paragraph(str("No"),styleD)

 
                contador = contador+1
                contadorM=Paragraph (str(contador), styleD)
                #data1.append ([contadorM,facturaNum,clientes,fecha,valorM,fechaIngreso,valorIng,EstadoFac,AIU])
                data1.append ([contadorM,facturaNum,clientes,fecha,valorM,fechaIngreso,valorIng,EstadoFac,AIU])
            TexTotal=Paragraph(('T O T A L'), styleG)
            #TotalFactutacion=TotalFactutacion
            #ValtotalIngreso=ValtotalIngreso
            
            TotalFactutacion4 =0
            FacProyectoSin = FacProyecto.filter(EstadoFactura=8)    
            for o in FacProyectoSin:
                
                #if o.EstadoFactura != "Sin Pago":
                valorF =o.ValorFactura
                valor4= "{:>15,}".format(valorF).replace(',','~').replace('.',',').replace('~','.')
                valor4=Paragraph(str(valor4),styleC)

                #TotalFactutacion4 = valorF + TotalFactutacion4
                
                #TotalFactutacion4= "{:>15,}".format(TotalFactutacion4).replace(',','~').replace('.',',').replace('~','.')
                #TotalFactutacionM=Paragraph(str(TotalFactutacion4),styleF)

                NumFactura4=Paragraph(str(o.NumFactura),styleD)
                EstadoFactura4= Paragraph(str(o.EstadoFactura),styleD)
                Clientes4=Paragraph(str(o.Clientes),styleD)
                fechaFactura4=Paragraph(str(o.fechaFactura),styleD)

                AIU4=(o.AIU)
                if AIU4 == True:
                    AIU4=Paragraph(str("Si"),styleD)
                else:
                    AIU4=Paragraph(str("No"),styleD)

                contador = contador+1
                contadorM=Paragraph (str(contador), styleD)

                data1.append ([contadorM,NumFactura4,Clientes4,fechaFactura4,valor4,'','',EstadoFactura4,AIU4])
            
            
            #data1.append ([TexTotal,'','','',TotalFactutacionM,'',ValtotalIngresoM,'',''])
            data1.append ([TexTotal,'','','',TotalFacturacionFacM,'',ValtotalIngresoM,'',''])
            
            c.setFillColor(HexColor('#548236'))
            c.setFont('Helvetica-Bold',16)
            c.drawCentredString(420.945, 498, str(proyecto))
           
            c.setFillColor(HexColor('#FFFFFF'))
            c.setFont('Helvetica',12)
            proyectoVal=round((proyecto.Valor),2)
            proyectoValM= "{:>15,}".format(proyectoVal).replace(',','~').replace('.',',').replace('~','.')

            c.setFont('Helvetica',10)
            c.setFillColor(HexColor('#FFFFFF'))
            c.drawString(60,453, str('Valor del contrato antes de impuestos $'+proyectoValM))
            c.drawRightString(805,498, str(proyecto.EstadoProyecto))
            
            if proyecto.fechaInicio is None:
                c.drawString(380,453, str(''))
            else:
                c.drawString(350,453, str('Inicio:'))
                c.drawString(380,453, str(proyecto.fechaInicio))
    
            if proyecto.fechaFinReal is None:
                c.drawString(510,453, str(''))
            else:
                c.drawString(480,453, str('Fin:'))
                c.drawString(510,453, str(proyecto.fechaFinReal))
            
            

            c.drawString(650,453, str('Saldo por facturar $'+ SaldoXFacturarM))
            


            table=Table(data1,colWidths=[0.8 * cm, 2 * cm, 9 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm, 2 * cm, 1 * cm])
            table.setStyle(TableStyle([#estilo de la tabla
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#C6E0B4")),
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0,0),(-1,-1), 0.25, colors.black),
            ('BOX', (0,0),(-1,-1), 0.25, colors.black),
            ('SPAN',(0,-1),(-6,-1)), 
            ]) )

            

            data.append(Spacer(6,6))
            data.append(table)
            frame.addFromList(data, c)
            c.showPage()
        
        else:
           
          

            for row in detallesIngreso [Contador_new[i]: Contador_new[i+1]]:

                facturaNum= Paragraph (str(row.Factura.NumFactura), styleD)
                fecha=Paragraph (str(row.Factura.fechaFactura), styleD)
                
                
                valorIng=(row.ValorIngreso)
                ValtotalIngreso=valorIng + ValtotalIngreso
                ValtotalIngresoM= "{:>15,}".format(ValtotalIngreso).replace(',','~').replace('.',',').replace('~','.')
                ValtotalIngresoM=Paragraph(str(ValtotalIngresoM),styleF)

                valorIng= "{:>15,}".format(valorIng).replace(',','~').replace('.',',').replace('~','.')
                valorIng=Paragraph(str(valorIng),styleC)

                clientes= Paragraph (str(row.Factura.Clientes), styleD),
                proyecto=(row.Proyecto)
                valor = round((row.Factura.ValorFactura),2)
                
                NoFactura1 = str(facturaNum)
                if NoFactura1  != NoFactura2:

                    TotalFacturacion = valor + TotalFacturacion
                    
                    TotalFacturacionM= "{:>15,}".format(TotalFacturacion).replace(',','~').replace('.',',').replace('~','.')
                    TotalFacturacionM=Paragraph(str(TotalFacturacionM),styleF)
                NoFactura2 = NoFactura1
                
                
                valorM= "{:>15,}".format(valor).replace(',','~').replace('.',',').replace('~','.')
                valorM=Paragraph(str(valorM),styleC)
                EstadoFac = Paragraph (str(row.Factura.EstadoFactura),styleD)

                
                fechaIngreso=(row.fechaIngreso)
                fechaIngreso=Paragraph(str(fechaIngreso),styleD)
                
                AIU=(row.Factura.AIU)
                if AIU == True:
                    AIU=Paragraph(str("Si"),styleD)
                else:
                    AIU=Paragraph(str("No"),styleD)

                
                contador = contador+1
                contadorM=Paragraph (str(contador), styleD)
                
                data1.append ([contadorM,facturaNum,clientes,fecha,valorM,fechaIngreso,valorIng,EstadoFac,AIU])
                
        

            c.setFillColor(HexColor('#548236'))
            c.setFont('Helvetica-Bold',16)
            c.drawCentredString(420.945, 498, str(proyecto))
                
            
            c.setFillColor(HexColor('#FFFFFF'))
            c.setFont('Helvetica',12)
            proyectoVal=round((proyecto.Valor),2)
            #proyectoValM= "{:>15,}".format(proyectoVal).replace(',','~').replace('.',',').replace('~','.')

            proyectoValM= "{:>15,}".format(proyectoVal).replace(',','~').replace('.',',').replace('~','.')



            c.setFont('Helvetica',10)
            c.setFillColor(HexColor('#FFFFFF'))
           
            c.drawString(650,453, str('Saldo por facturar $'+ SaldoXFacturarM))

            c.setFont('Helvetica',10)
            c.setFillColor(HexColor('#FFFFFF'))
            c.drawString(60,453, str('Valor del contrato antes de impuestos $'+proyectoValM))
            c.drawRightString(805,498, str(proyecto.EstadoProyecto))
            
            if proyecto.fechaInicio is None:
                c.drawString(380,453, str(''))
            else:
                c.drawString(350,453, str('Inicio:'))
                c.drawString(380,453, str(proyecto.fechaInicio))
    
            if proyecto.fechaFinReal is None:
                c.drawString(510,453, str(''))
            else:
                c.drawString(480,453, str('Fin:'))
                c.drawString(510,453, str(proyecto.fechaFinReal))
            
                       

            table=Table(data1,colWidths=[0.8 * cm, 2 * cm, 9 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm, 2 * cm, 1 * cm])
            table.setStyle(TableStyle([#estilo de la tabla
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#C6E0B4")),
            ('VALIGN',(0, 0), (-1, -1),'MIDDLE'),
            ('INNERGRID', (0,0),(-1,-1), 0.25, colors.black),
            ('BOX', (0,0),(-1,-1), 0.25, colors.black),
            #('SPAN',(0,-1),(-6,-1)), 
            ]) )

            data.append(Spacer(6,6))
            data.append(table)
            frame.addFromList(data, c)
            c.showPage()    

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response 
