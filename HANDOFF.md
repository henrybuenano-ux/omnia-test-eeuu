# HANDOFF — Proyecto CRM Venezia Kitchen Cabinets & Bath (VN Supply)

> Documento de traspaso para continuar el proyecto en otra cuenta de Claude Code (cloud).
> Lee esto primero: resume qué es el proyecto, dónde vive cada cosa, los IDs, el estado y cómo seguir.

---

## 1. Qué es el proyecto

Implementación completa de un CRM en **GoHighLevel (GHL)** para el cliente **Venezia Kitchen Cabinets & Bath**.

- **Razón social:** INTERNATIONAL SUPPLY COOL INC. (dba VN Supply Kitchen Cabinets) · EIN 81-2052650 · Corporation / Manufacturing.
- **Rubro:** venta e instalación de gabinetes de cocina, cuarzo, baños, pisos SPC. Miami/Medley + West Palm Beach, FL.
- **Representante:** Stiward "Stewart" Orellana (GM, venezolano). Cálido, admite no saber de tecnología → **explicar todo en lenguaje de negocio, sin jerga técnica** (nada de "nodos, workflows, triggers" en documentos/mensajes al cliente).
- **Equipo implementador:** Profit Technology / GHL Team Latam (Henry, Oliver, German).

### Reglas/filosofía permanentes (respetarlas siempre)
- Nada de jerga técnica en material del cliente.
- No prometer cantidades exactas de automatizaciones al cliente.
- No pisar el terreno de la chica de marketing externa (ads/redes son de ella; el CRM es nuestro).
- Seguimiento **sutil**, nunca perseguir a un cliente molesto.
- **Precios: nunca por chat.** El bot nunca cotiza; deriva a un asesor humano.

---

## 2. Dónde vive cada cosa (los 3 lugares)

| Componente | Dónde | Cómo se migra |
|---|---|---|
| **El CRM** (campos, pipelines, workflows, calendarios, bot, forms) | Subcuenta GHL **Venezia** (`vuAlfQCdJFMVbxxvhEml`) | Snapshot de GHL (si algún día se mueve de cuenta GHL) |
| **Documentación / tareas** | ClickUp — folder "VN Supply / Venezia $$" | Plantilla/export de ClickUp |
| **CLI, blueprints, docs, PDFs, páginas legales** | Este repo GitHub | Clonar el repo en la cuenta nueva |

**Para continuar en otra cuenta de Claude Code:** ver sección 9.

---

## 3. Credenciales (NO están en el repo — re-agregar en la cuenta nueva)

Viven en `.env` (gitignored). En la cuenta nueva hay que volver a ponerlas como variables/secretos:
- `GHL_API_KEY` — Private Integration Token de la subcuenta Venezia (empieza `pit-...`). **SECRETO.**
- `GHL_LOCATION_ID` = `vuAlfQCdJFMVbxxvhEml` (identificador, no secreto).
- `GHL_FIREBASE_REFRESH_TOKEN` — token del API interno (Firebase JWT). **SECRETO**, rota; pedir uno fresco cuando expire.

**Conectores MCP a reconectar:** ClickUp y (si aplica) GHL. GitHub para el repo.

---

## 4. IDs clave de GHL (subcuenta Venezia)

- **Location:** `vuAlfQCdJFMVbxxvhEml`
- **Pipeline "Ventas":** `G4r0zseiK4KHs1Hh3ptj`
  - Etapa "Nuevo lead": `d299bb27-6274-4666-8fa5-f3095ae12561`
  - Etapa "Calificado": `408a08cb-15f3-4f66-a52e-4e13457880d4`
  - Etapas "Visita agendada" y "Estimado enviado": **verificar que existan** (las usan SP02/SP03).
- **Pipeline "Proyectos Activos":** `8vHsYiJP4MhrE3kBuABz`
- **Calendario "Visita / Medición":** `gshoyleB0Xbb1aLVXwIk` (custom value `link_calendario_visitas`). Hoy solo tiene al usuario **Stiward**.
- **Form "Formulario nuevo lead":** `eOlPYYCyBqHfbr9rurAM`
- **Usuario Stiward:** `cBFAFxd1X1nlExXiYh6n`
- **Widget de chat instalado:** ver `docs/web-vnskcb/instrucciones-webmaster.md`.

### Custom fields (los que importan)
Espejo de texto que escribe el bot (Contact Info) → dropdown real (lo llena SYNC/T8):

| Campo texto `(bot)` | key | → Dropdown real | key |
|---|---|---|---|
| Tipo de cliente (bot) | `contact.tipo_de_cliente_bot` | Tipo de cliente | `contact.tipo_de_cliente` (`uRyyBlP4qXHQt8NPCPaI`) |
| ¿Tiene medidas? (bot) | `contact.tiene_medidas_bot` | ¿Tiene medidas? | `contact.tiene_medidas` (`ey7voH2m0srqqsdlOMSJ`) |
| Idioma preferido (bot) | `contact.idioma_preferido_bot` | Idioma preferido | `contact.idioma_preferido` (`NWjGFvTx97l1HIKjdaGw`) |
| Ciudad (bot) | `contact.ciudad_bot` | (se queda texto) | — |
| Producto de interés (bot) | `contact.producto_de_inters_bot` | Producto de interés | `contact.producto_de_inters` (`ySuO57WB78pe6UUTjbz9`) |

Otros: `Medidas / notas de medición` (`contact.medidas__notas_de_medicin`, LARGE_TEXT), `STATUS DEL LEAD` (`contact.status_del_lead`), `PROYECTO` (`contact.proyecto`), `Link PDF estimado` (`contact.link_pdf_estimado`), `Fecha última respuesta` (`contact.fecha_ltima_respuesta`, DATE), `Dirección de instalación` (`contact.direccin_de_instalacin`).

**Valores fijos de dropdowns (ya alineados por API):**
- Tipo de cliente: Contratista · Handyman · Showroom · Cliente final · Arquitecto · Diseñador · Remodelador · Otro
- Producto de interés: Por definir · Kitchen Cabinets · Quartz Countertops · Bathroom Vanities · Vinyl Flooring · Closets · Commercial · Otro
- ¿Tiene medidas?: Sí · No · Idioma: Español · English

---

## 5. ClickUp (documentación / tareas)

- **Folder:** "VN Supply / Venezia $$" = `1000460000002755`
- **Lista 01 · Bot Conversation AI:** `1000460000003980`
- **Lista 03 · Sales Pipeline (SP01–SP04):** `1000460000003982`

Tareas clave (bot): T1 Auditoría `wdx6zepq06` ✅ · T3 Prompt `wdx6zepq08` ✅ · T4 Calificación `wdx6zepq09` · T5 Agendamiento `wdx6zepq0a` · T6 Handover `wdx6zepq0b` · T7 Pruebas `wdx6zepq0c` · T8 SYNC `wdx6zepq92`.
Tareas (pipeline): SP01 `wdx6zepq0h` · SP02 `wdx6zepq0j` · SP03 `wdx6zepq0m` · SP04 `wdx6zepq0n`.

> **Las descripciones de estas tareas son la fuente de verdad** de cada blueprint (prompt del bot, specs de Contact Info, receta del SYNC, mensajes bilingües de SP01–SP04). Léelas al retomar.

---

## 6. El CLI (vendored: leadgenjay/gohighlevel-cli)

En `cli_anything/gohighlevel/`. Habla con la API v2 (`services.leadconnectorhq.com`) y el API interno (Firebase).

**Qué SÍ puede crear por CLI:** workflows con **trigger por tag** + cadenas lineales (sms, email, wait, tag, webhook, ai, internal_notification, task-notification). Crea todo en **draft**.

**Qué NO puede (hay que armar a mano en el Standard builder):**
- Triggers que no sean por tag (ej. **Contact Changed**, **Appointment Status**, **Opportunity Stage Changed**).
- Nodos **Condition / If-Else** (branching).
- **Waits relativos** a una cita (24h/2h antes).
- Acciones del **Conversation AI** (el bot) — todo eso es UI.

**Notas técnicas:**
- Crear/editar custom fields por Python requiere header `User-Agent: Mozilla/5.0` (si no, Cloudflare 403 error 1010).
- `opportunities` usa snake_case (`location_id`, `pipeline_id`).
- Bug menor conocido: `utils/ghl_client.py:56` tiene un location default ajeno (`YB8rMdFShcHGcZGW87mA`); se sobreescribe con la env var, no afecta.

---

## 7. Arquitectura del bot (Conversation AI "Venezia")

Regla dura de GHL: **el bot NO pone tags** y con **Contact Info solo escribe texto simple** (no dropdowns).

```
Cliente → BOT (Conversation AI)
   ├─ Contact Info → escribe campos de TEXTO (bot)
   ├─ Appointment Booking → agenda visita (T5)
   └─ Human Handover (nativo) → pasa a persona (T6)
        │ (al escribirse el texto se dispara solo)
        ▼
   SYNC (T8, Standard builder): Contact Changed → Condition → Update dropdown + Add Tag
        ▼
   SP01 dispara
```

- **Prompt final del bot:** en la tarea T3 (`wdx6zepq08`). Nombre del asistente: **Vanne**. Bilingüe, mensajes 2-3 líneas, White Shaker producto estrella, precios nunca por chat.
- **Delay 6-8s:** se configura en *Timing & Pacing*, no en el prompt.
- **Base de conocimiento:** `docs/Base_Conocimiento_Bot_Venezia.pdf` (ya subida a la KB del bot).
- **Regla de idioma:** instrucciones al bot en inglés (da igual, el modelo es bilingüe); **example phrases y mensajes al cliente en ES + EN**; valores de campo = token fijo, no se traduce.

---

## 8. Estado actual (a la fecha del handoff)

**Lista 01 · Bot:**
- T1 Auditoría ✅ (fusionada en el prompt) · T3 Prompt ✅ · Política de precios ✅
- T4 Calificación 🔵 spec listo → Oliver configura Contact Info en el builder
- T5 Agendamiento 🔵 acción lista → falta correos Aura/Alex
- T6 Handover 🔵 spec nativo (Human Handover 4 escenarios + Stop Bot + Summary Settings) → Oliver configura
- T8 SYNC 🔵 receta lista → build en Standard builder (3 workflows, uno por campo)
- T7 Pruebas E2E ⬜ pendiente (se dejó para el final)

**Lista 03 · Pipeline:**
- SP01 Calificación ✅ (blueprint completo con bifurcación con/sin medidas y mensajes bilingües; con/sin medidas SOLO aplica a Cliente final)
- SP02 Visita anti no-show 🔵 ~15% — reescrito: "completada" sale sola con Wait post-cita; reagendamiento manual (staff marca Cancelled/No Show); + ítem de capacitación
- SP03 Estimado enviado 🔵 2 triggers resueltos (campo Link PDF + etapa) + guardrail link vacío; falta Stop-on-Response y stamping de Fecha última respuesta
- SP04 Reactivación base 647 ✅ (solo WhatsApp/SMS, sin email)

**Pendientes del cliente:** correos de Aura y Alex (calendario + handover) · teléfono definitivo para A2P · export de Clover para migración · plantillas WA de reactivación aprobadas por Meta (SP04).

---

## 9. Cómo continuar en la cuenta nueva de Claude Code

1. **Dar acceso al repo** `henrybuenano-ux/omnia-test-eeuu` a la cuenta nueva (o transferir/forkear) y abrir una sesión de Claude Code sobre ese repo.
2. **Re-agregar los secretos** (sección 3) como variables de entorno / `.env` — NO están en el repo.
3. **Reconectar los MCP** (ClickUp, GitHub) en la cuenta nueva.
4. **Leer este HANDOFF + las descripciones de las tareas de ClickUp** (sección 5) — ahí está el detalle de cada blueprint.
5. Continuar con lo pendiente (sección 8), empezando por lo que Oliver arme en el builder + T7 (pruebas E2E).

> La conversación de esta sesión NO se transfiere entre cuentas. Este documento + ClickUp son el reemplazo. Manténlos actualizados.
