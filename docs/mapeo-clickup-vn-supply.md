# Mapeo ClickUp — VN Supply / Venezia (VN SKCB)

> **Destino:** folder `VN Supply / Venezia` (ID `1000460000002755`) · space **Activos**
> **Subcuenta GHL:** `vuAlfQCdJFMVbxxvhEml` (VENEZIA KITCHEN CABINETS & BATH)
> **Convención:** 1 lista = bloque funcional · 1 tarea = entregable/workflow · 1 subtarea = 1 nodo/paso
> **Estado:** BORRADOR para aprobación — nada creado en ClickUp todavía.
>
> 🔴 = bloqueado por entregable del cliente · 🟡 = parcialmente bloqueado

---

## 🏗️ 00 · Setup — Subcuenta, Dominio, A2P, Campos, Pipelines y Calendario

### T1. Configuración base de subcuenta (white-label)
- Completar perfil de negocio: nombre, dirección Medley FL, logo, branding
- Zona horaria America/New_York + idioma por defecto
- Crear usuarios: Stewart (admin), Aura y Alex (vendedores) con permisos de venta 🟢 *(faltan correos de Aura y Alex)*
- Instalar y probar app Lead Connector en los 3 teléfonos

### T2. Dominio de correo corporativo (info@vnskcb.com)
- 🔴 Obtener acceso a GoDaddy (lo administra el hermano de Stewart)
- Configurar dedicated sending domain en GHL
- Registros DKIM + SPF + DMARC en GoDaddy
- Test de entregabilidad (inbox placement a Gmail/Outlook)

### T3. Registro A2P
- 🔴 Publicar política de privacidad + términos y condiciones en la web
- 🔴 Definir línea telefónica definitiva
- Comprar/portar número en GHL y asignarlo
- Enviar registro de brand + campaign A2P
- Verificar aprobación y hacer test de SMS saliente

### T4. SSL / candado en la web
- Verificar certificado actual del dominio
- Si falta: activar SSL desde GoDaddy/hosting y forzar HTTPS

### T5. Custom fields (~38) — grupo Contacto
- Grupo **Calificación**: Tipo de cliente (Contratista/Cliente final), ¿Tiene medidas? (Sí/No), Idioma preferido (ES/EN)
- Grupo **Producto**: Producto de interés, Tipo de gabinete (RTA/A medida), Color/estilo, Presupuesto estimado
- Grupo **Proyecto**: Medidas / notas de medición, Dirección de instalación, Ciudad (Miami/WPB), Fecha visita
- Grupo **Estimado**: Nº estimado, Monto, Link PDF, Fecha de envío, Fecha última respuesta
- Grupo **Proyecto activo**: Fecha de pago, Tipo de entrega (RTA 1 sem / medida 15d+1sem), Fecha inicio fabricación, Fecha instalación programada
- Grupo **Atribución**: Fuente, Campaña, Anuncio de origen, Canal de entrada (WA/IG/Web)
- Grupo **Integraciones**: clover_customer_id *(se deja creado aunque el add-on no va aún)*
- Grupo **Post-venta**: Puntuación encuesta (1-5), ¿Dejó review? (Sí/No)

### T6. Taxonomía de tags
- Tags de calificación: `contratista`, `cliente-final`, `con-medidas`, `sin-medidas`
- Tags de control: `stop bot` (ya existe), `handover-humano`, `no-contactar`
- Tags de ciclo: `cliente-historico` (migración Clover), `reactivacion` (base de 647), `compro`, `review-dejada`
- Documentar reglas de uso (qué workflow pone/quita cada tag)

### T7. Pipeline "Ventas" (7 etapas)
- Crear pipeline: Nuevo lead → Contactado → Calificado → Visita agendada → Estimado enviado → Negociación → Ganado/Perdido
- Eliminar los 4 deals "(Example)" y despublicar el "Marketing Pipeline" genérico
- Configurar probabilidades y visibilidad en funnel

### T8. Pipeline "Proyectos Activos" (5 etapas)
- Crear pipeline: Pagado → Fabricación → Listo para instalar → Instalación → Terminado
- Regla operativa: la oportunidad entra al ganar en Ventas (movimiento manual mientras no exista integración Clover)

### T9. Custom values de marca
- Logo, colores, teléfono, dirección de showroom, link de Google Review, link de calendario, firma de correo

### T10. Vistas / filtros guardados (3)
- Vista "Contratistas activos" (tipo=contratista, pipeline Ventas)
- Vista "Estimados sin respuesta >7 días"
- Vista "Proyectos en fabricación/instalación"

### T11. Calendario "Visita / Medición"
- Crear calendario round-robin Aura + Alex, citas de 60 min con buffer de traslado
- Horarios de atención por sucursal + auto-confirmación
- Formulario de la cita: dirección, tipo de proyecto, notas
- 🟢 Definir regla de depósito para visitas (decisión de semana 1)
- Conectar Google Calendar de los vendedores (evitar dobles reservas)

---

## 🤖 01 · Bot Conversation AI — Bilingüe + Calificación

### T1. Auditoría del bot actual de Instagram
- Exportar/copiar prompts y respuestas del bot existente antes de tocar nada
- Documentar qué funciona y qué reconstruir (mensajes largos, delay 1s robótico)

### T2. Base de conocimiento
- 🟡 Cargar lista completa de productos + producto estrella (pendiente cliente)
- FAQs: tiempos (RTA ~1 sem / medida 15d+1sem), pago 100% adelantado vía Clover en tienda, zonas de servicio
- Política de precios: NO dar precio exacto por chat; contratista → mencionar precio especial B2B

### T3. Prompt principal
- Personalidad: cercana, profesional, bilingüe ES/EN con detección automática de idioma
- **Mensajes cortos** (ajuste pedido por el cliente — máx. 2-3 líneas por mensaje)
- Delay de respuesta 6-8 segundos
- Guardrails: no inventar precios ni fechas, no prometer instalación B2B, escalar si el cliente se molesta

### T4. Flujo de calificación (el corazón del bot)
- Pregunta 1: ¿contratista/handyman/showroom o cliente final? → set custom field + tag
- Rama contratista: capturar empresa, volumen, si trae planos → handover a vendedor con contexto
- Rama cliente final: ¿tiene medidas? → Sí: pedir medidas/fotos y pasar a estimado · No: ofrecer visita
- Captura de datos mínimos: nombre, teléfono, ciudad, producto de interés

### T5. Agendamiento desde el bot
- Conectar bot al calendario "Visita / Medición" (slots reales)
- Confirmación de cita dentro de la conversación

### T6. Handover a humano
- Trigger por: petición explícita, molestia detectada, caso fuera de alcance
- Poner tag `stop bot` + notificación interna a Aura/Alex con resumen de la conversación

### T7. Pruebas end-to-end
- Test ES y EN por rama (contratista / final con medidas / final sin medidas)
- Verificar delay, largo de mensajes y que los custom fields se escriben bien

---

## 🔵 02 · Lead Sources — LS01, LS02, LS03

### LS01 · Entrada WhatsApp
- Trigger: mensaje entrante por WhatsApp de contacto nuevo o sin oportunidad abierta
- Filtro anti-duplicado: si ya tiene oportunidad abierta → salir
- Set atribución: Fuente=WhatsApp + campaña/anuncio de origen (si viene de CTWA, capturar referral del anuncio)
- Set canal de entrada = WA + tag de canal
- Crear oportunidad en Ventas → etapa "Nuevo lead"
- Activar bot Conversation AI
- Notificación interna si llega fuera de horario del bot-humano

### LS02 · Entrada Instagram (reconstruir)
- Trigger: DM de Instagram entrante
- Misma lógica de anti-duplicado + atribución (Fuente=Instagram, anuncio si viene de ad)
- Crear oportunidad → "Nuevo lead"
- Activar bot (el existente se reemplaza por el nuevo de la lista 01)

### LS03 · Formulario Web / Chat Widget
- 🔴 Requiere accesos a la web (GoDaddy / hosting)
- Construir formulario GHL: nombre, teléfono, email, tipo de cliente, producto, ¿tiene medidas?, mensaje
- Instalar chat widget en vnskcb.com con branding del cliente
- Trigger: form submitted / chat iniciado
- Mapping campos del form → custom fields
- Crear oportunidad → "Nuevo lead" + notificación a vendedores
- Auto-respuesta inmediata (WA o SMS) para abrir conversación

---

## 🟢 03 · Sales Pipeline — SP01, SP02, SP03, SP04

### SP01 · Calificación Contratista / Cliente Final
- Trigger: custom field "Tipo de cliente" se llena (por bot o manual)
- Rama **Contratista**: tag `contratista` + asignar vendedor + plantilla de bienvenida B2B (precio especial) → etapa "Calificado"
- Rama **Cliente final con medidas**: solicitar medidas/fotos si faltan → etapa "Calificado" → aviso a vendedor para estimado el mismo día
- Rama **Cliente final sin medidas**: invitación a agendar visita con link del calendario → seguimiento si no agenda en 24h/72h
- Actualizar etapa según rama completada

### SP02 · Visita / Medición agendada (anti no-show)
- Trigger: cita creada en calendario "Visita / Medición"
- Mover oportunidad → "Visita agendada"
- Confirmación inmediata por WA/SMS con fecha, hora y dirección
- Recordatorio 24h antes (con opción de reagendar)
- Recordatorio 2h antes
- Rama **no-show**: mensaje de reagendamiento + tarea al vendedor + volver a "Calificado"
- Rama **asistió**: marcar cita completada → aviso al vendedor para preparar estimado

### SP03 · Estimado enviado + seguimiento sutil
- Trigger: oportunidad movida a "Estimado enviado" (o field "Link PDF" se llena)
- Envío del estimado PDF por WhatsApp + email (plantilla con marca)
- Cadencia educativa (enfoque NO agresivo — pedido explícito del cliente): día 1 (¿llegó bien?), día 3 (contenido de valor: cómo elegir gabinete), día 7 (casos/fotos de proyectos), luego 1 vez al mes
- Cualquier respuesta del cliente → detener secuencia + notificar vendedor
- Rama a "Negociación" (respondió interesado) o "Perdido" (rechazo explícito) — movimiento por vendedor
- Registrar fecha de última respuesta en custom field

### SP04 · Nurturing y reactivación de base (los 647)
- Segmentación previa: la base actual no tiene fuente ni tags y 96% no tiene email → campaña **WhatsApp/SMS first**
- Importar tags `reactivacion` al segmento objetivo
- Mensaje 1: reintroducción de la marca + pregunta abierta (¿sigues con tu proyecto de cocina?)
- Respuesta → entra a SP01 (calificación) + quitar tag `reactivacion`
- Sin respuesta: 2 toques más espaciados (día 7, día 21) y luego frecuencia mensual educativa
- Opt-out: palabra clave para no-contactar → tag `no-contactar` + DND
- Límite de envío diario (drip) para proteger el número A2P

---

## 🔴 04 · Active Projects — AP01

### AP01 · Proyecto: fabricación e instalación
- Trigger: oportunidad creada/movida a "Pagado" en pipeline Proyectos Activos (manual post-pago Clover; fallback documentado mientras no exista el add-on)
- Mensaje al cliente: confirmación de pago + qué sigue + tiempos según su tipo de gabinete
- Rama **RTA (prehecho)**: recordatorio interno de programar entrega+instalación ~1 semana
- Rama **A medida**: mover a "Fabricación" + timer 15 días + aviso interno al día 12 para confirmar avance
- Al mover a "Listo para instalar": mensaje al cliente para coordinar fecha de instalación
- Al mover a "Instalación": confirmación de fecha + recordatorio 24h antes
- Al mover a "Terminado": mensaje de cierre + disparo de PS01
- Notificaciones internas a Stewart en cada cambio de fase

---

## 🌟 05 · Reviews — PS01

### PS01 · Encuesta de satisfacción + Google Review
- Trigger: oportunidad movida a "Terminado" en Proyectos Activos
- Delay 24-48h post-instalación
- Encuesta 1-5 por WA/SMS (una sola pregunta)
- Rama **4-5★**: agradecimiento + link directo a Google Review + tag `review-dejada` al confirmar
- Rama **1-3★**: alerta interna inmediata a Stewart (llamada de recuperación) — NO se envía link de review
- Registrar puntuación en custom field
- Re-ask de review a los 7 días si dijo que sí pero no la dejó (1 solo recordatorio)

---

## 📊 06 · Migración Clover, Plantillas, Dashboard y Capacitación

### T1. Migración de base de datos histórica de Clover
- 🔴 Obtener exportación de clientes de Clover (pendiente cliente)
- Limpieza: normalizar teléfonos, deduplicar contra los 647 existentes en GHL
- Mapping columnas Clover → custom fields GHL
- Import con tag `cliente-historico` + fuente=Clover
- Verificación post-import (conteos, muestreo)

### T2. Plantillas de estimado y comunicación con marca
- 🟡 Recibir ejemplos de estimados PDF de Zoho (pendiente cliente)
- Plantilla de envío de estimado (WA + email) con branding
- Plantillas de confirmación/recordatorio de visita
- Plantillas de proyecto activo (pago, fabricación, instalación)
- Plantillas bilingües donde aplique

### T3. Dashboard / panel de reportes
- Widget: leads por fuente y por anuncio (atribución — no mencionarla explícitamente en docs del cliente)
- Widget: conversión por etapa del pipeline Ventas
- Widget: valor del pipeline + proyectos activos por fase
- Widget: reviews conseguidas / promedio encuesta

### T4. Capacitación (2 sesiones)
- Sesión 1 — Stewart + Aura + Alex: pipeline, oportunidades, conversaciones, app Lead Connector
- Sesión 2 — operación diaria: calendario, estimados, qué hace el bot y cuándo intervenir
- Mini-guía de referencia en lenguaje de negocio (sin jerga técnica)

### T5. QA final y entrega
- Test end-to-end por cada fuente de entrada (WA, IG, Web) hasta review
- Checklist de cierre contra el alcance aprobado
- Cobro del 50% restante ($1,400)

---

## Resumen

| Lista | Tareas | Subtareas aprox. |
|---|---|---|
| 🏗️ 00 · Setup | 11 | 44 |
| 🤖 01 · Bot Conversation AI | 7 | 24 |
| 🔵 02 · Lead Sources | 3 | 20 |
| 🟢 03 · Sales Pipeline | 4 | 26 |
| 🔴 04 · Active Projects | 1 | 9 |
| 🌟 05 · Reviews | 1 | 7 |
| 📊 06 · Migración y cierre | 5 | 19 |
| **Total** | **32** | **~149** |

**Excluido por decisión:** lista 07 · Add-on Clover ↔ GHL (n8n) — no va por el momento (el campo `clover_customer_id` queda creado en el setup para no migrar dos veces).
