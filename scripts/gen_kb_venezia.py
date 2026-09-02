# -*- coding: utf-8 -*-
"""Genera docs/Base_Conocimiento_Bot_Venezia.pdf — KB del bot Venezia.
v2 (sep-2026): agrega la política de la VISITA DE MEDICIÓN (tiene costo, se reintegra
como crédito al comprar; el bot NO la cotiza ni la llama 'gratis' → deriva a especialista).
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                ListFlowable, ListItem)

NAVY = colors.HexColor("#1F3B63")
OUT = "docs/Base_Conocimiento_Bot_Venezia.pdf"

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Title"], textColor=NAVY, fontSize=20, spaceAfter=6)
SUB = ParagraphStyle("SUB", parent=ss["Normal"], fontSize=9, textColor=colors.HexColor("#555"))
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=NAVY, fontSize=13, spaceBefore=12, spaceAfter=4)
H3 = ParagraphStyle("H3", parent=ss["Heading3"], textColor=NAVY, fontSize=11, spaceBefore=8, spaceAfter=2)
BODY = ParagraphStyle("BODY", parent=ss["Normal"], fontSize=9.5, leading=13)
NOTE = ParagraphStyle("NOTE", parent=BODY, fontSize=9.5, leading=13)

def bullets(items):
    return ListFlowable([ListItem(Paragraph(t, BODY), leftIndent=10) for t in items],
                        bulletType="bullet", start="•", leftIndent=12)

def callout(html):
    t = Table([[Paragraph(html, NOTE)]], colWidths=[16*cm])
    t.setStyle(TableStyle([("BOX",(0,0),(-1,-1),0.8,NAVY),
                           ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#FBF3E9")),
                           ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
                           ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    return t

f = []
f += [Paragraph("Base de Conocimiento — Asistente Virtual", H1)]
f += [Paragraph("Venezia Kitchen Cabinets &amp; Bath · Documento para GHL Conversation AI", SUB)]
f += [Spacer(1,4), Paragraph("Regla base: el asistente solo afirma lo que está en este documento. "
      "Si no está aquí, NO lo inventa — deriva a un asesor humano.", BODY), Spacer(1,6)]
f += [callout("<b>■ PRODUCTO ESTRELLA:</b> el <b>White Shaker</b> (gabinete de cocina) es el producto más "
      "buscado por los clientes. Cuando alguien llegue indeciso o no sepa qué elegir, sugerir el White "
      "Shaker como punto de partida."), Spacer(1,6)]

f += [Paragraph("1. La empresa", H2)]
f += [bullets([
 "Venezia Kitchen Cabinets &amp; Bath — venta e instalación de gabinetes de cocina, encimeras (countertops), pisos y baños.",
 "Ubicaciones: <b>Miami</b> (11825 NW 100 Rd, Suite 5) y <b>West Palm Beach</b> (377 N Cleary Rd, Suite 2-3).",
 "Web: veneziakcb.com · Atiende a homeowners, contratistas y diseñadores."])]

f += [Paragraph("2. Productos", H2)]
f += [Paragraph("2.1 Kitchen Cabinets (Gabinetes de cocina)", H3)]
f += [Paragraph("10 estilos RTA (Ready-to-Assemble / prehechos). Todos: frameless, caja de ¾ de plywood, "
      "bisagras y correderas soft-close. Tamaños estándar con retiro inmediato.", BODY)]
f += [bullets([
 "<b>■ White Shaker (PRODUCTO ESTRELLA — el más buscado)</b> — blanco pintado, puertas de madera sólida, instalación atornillada.",
 "<b>Gola White High Gloss</b> — blanco brillante, perfil Gola de aluminio, puertas de particle board.",
 "<b>Gola Honey Oak</b> — texturizado cálido, perfil Gola negro.",
 "<b>Blue Shaker · Gray Shaker · Espresso Shaker</b> — pintados, madera sólida.",
 "<b>Walnut Double Shaker · Coffee Double Shaker</b> — madera sólida.",
 "<b>White Raised Panel · Coffee Raised Panel</b> — estilo tradicional detallado, madera sólida."])]
f += [Paragraph("2.2 Quartz Countertops (Encimeras de cuarzo)", H3)]
f += [Paragraph("Cuarzo <b>Calacatta</b>, <b>Carrara</b> y <b>Pure Color</b>, en <b>Jumbo (3cm)</b> y Super Jumbo. "
      "No poroso, resistente a rayaduras, manchas, bacterias y humedad. Se pueden ver en el showroom de West Palm Beach.", BODY)]
f += [bullets([
 "<b>Calacatta (selección):</b> Affogato, Amarena, Basalt Gray, Bruna, Bellagio, Carpi, Dolci, Duke Gray, Everest Sunrise, "
 "Farfalle, Flavia, Fiori, Fragola, Golden, Jaz Gray, Monaco, Montpellier, Oro, Portofino, Royal, Sicilia, Sorrento, Taj Mahal, "
 "Versailles, Palermo, Napoles, Positano, y más.",
 "<b>Carrara:</b> Gray, White Light.",
 "<b>Pure Color:</b> White, Light Gray Cemento, Dark Gray Cemento.",
 "<b>Crystal:</b> Black Galaxy, White Galaxy, Dark Gray."])]
f += [Paragraph("2.3 SPC Vinyl Flooring (Pisos vinílicos SPC)", H3)]
f += [Paragraph("Stone Plastic Composite, rígido y resistente al agua. Amplia selección de colores.", BODY)]
f += [bullets(["Wear layer 22 mil","Espesor total 9mm","Underlayment con aislamiento acústico",
 "Instalación click-on","Núcleo rígido, water resistant"])]
f += [Paragraph("2.4 Bathrooms (Baños)", H3)]
f += [bullets([
 "<b>Bathroom Sinks (cerámicos):</b> top mount y undermount, redondos y cuadrados. Códigos CS1914, CS2213, CS1813.",
 "<b>Vanity Quartz Tops</b> prefabricados: Carrara Grey y Gold, tamaños 24\"-60\", single/double hole.",
 "<b>LED Bathroom Mirrors:</b> memoria, anti-fog, dimmable, backlit + front-lit, vidrio templado. 24\"-72\" (códigos LM…).",
 "<b>Bathroom Faucets:</b> FC-001 a FC-013. Colores: Chrome, Brush Nickel, Brush Gold, Matte Black.",
 "<b>Shower Systems:</b> SH 001 a SH 006. Chrome, Brush Nickel, Matte Black."])]
f += [Paragraph("2.5 Shower Doors (Mamparas de vidrio templado)", H3)]
f += [Paragraph("Vidrio templado <b>10mm clear</b>, con <b>soft-close</b>. Tamaño estándar <b>60\"W × 76\"H</b>. Double bypass sliding.", BODY)]
f += [bullets([
 "<b>Opción A</b> — 1 panel fijo + 1 corrediza: BL-045HC (soft close, 4 colores) · BL-045A (sin soft close, 2 colores).",
 "<b>Opción B</b> — 2 corredizas: BL-X604 (soft close, 4 colores) · BL-604 (sin soft close, 2 colores).",
 "Colores: Chrome, Brush Nickel, Matte Black, Brush Gold."])]
f += [Paragraph("2.6 Kitchen Sinks &amp; Faucets", H3)]
f += [bullets([
 "<b>Kitchen Sinks:</b> acero inoxidable 16-gauge, cuadrados y redondos. Códigos S2318, S3218, S1000, HMS. Tamaños 24x18 a 32x18.",
 "<b>Kitchen Faucets:</b> acero inoxidable, FC-014 a FC-019. Chrome, Brush Nickel, Brush Gold, Matte Black."])]
f += [Paragraph("2.7 PVC Wall Profile Panels (Paneles de pared)", H3)]
f += [Paragraph("Accesorio decorativo para paredes de acento. PVC, diseño fluted, liviano y de fácil instalación.", BODY)]

f += [Paragraph("3. Preguntas frecuentes (FAQs)", H2)]
f += [bullets([
 "<b>Tiempos:</b> gabinetes RTA/prehechos → entrega + instalación en ~1 semana. A medida → ~15 días fabricación + ~1 semana instalación.",
 "<b>Pago:</b> 100% por adelantado, vía Clover, en tienda.",
 "<b>Estimado:</b> sale el mismo día — minutos si el cliente ya tiene medidas; 1-2 horas si hay que diseñar.",
 "<b>Visita de medición:</b> <b>tiene un costo</b>, que se <b>reintegra como crédito</b> al concretar la compra. "
 "El asistente <b>NO</b> la llama gratis ni cotiza ese costo por chat → ofrece que un <b>especialista</b> coordine la visita y explique los términos.",
 "<b>Zonas:</b> Miami y West Palm Beach, Florida.",
 "<b>Showroom de cuarzos:</b> West Palm Beach (377 N Cleary Rd, Suite 2-3)."])]

f += [Paragraph("4. Política de precios (IMPORTANTE)", H2)]
f += [bullets([
 "El asistente <b>NUNCA da precio exacto por chat.</b>",
 "Si es contratista/profesional → mencionar <b>precio especial B2B</b> y derivar a un vendedor.",
 "Para cotización formal → capturar datos y derivar a asesor (el estimado sale el mismo día).",
 "La <b>visita de medición NO es gratis</b>: nunca decir 'gratis/sin costo' ni dar su costo — un especialista explica los términos."])]

f += [Paragraph("5. Reglas de conversación", H2)]
f += [bullets([
 "Bilingüe: responder en el idioma del cliente (español o inglés).",
 "Mensajes cortos (2-3 líneas máximo).",
 "Cliente indeciso → sugerir el <b>White Shaker</b> (producto estrella) como punto de partida.",
 "Si no sabe la respuesta o piden algo fuera de este documento → derivar a un asesor humano.",
 "No prometer instalación a contratistas que solo compran producto.",
 "<b>Visita de medición:</b> nunca decir que es gratis ni dar su costo. Ofrecer que un especialista coordine la visita y explique los términos."])]

SimpleDocTemplate(OUT, pagesize=letter, topMargin=2*cm, bottomMargin=2*cm,
                  leftMargin=2*cm, rightMargin=2*cm).build(f)
print("PDF generado:", OUT)
