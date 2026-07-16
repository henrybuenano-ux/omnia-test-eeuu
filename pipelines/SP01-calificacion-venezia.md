# SP01 · Calificación Contratista / Cliente Final — Blueprint de build (Venezia / VN Supply)

**Workflow GHL:** `SP01 · Calificación`
**Subcuenta:** VN Supply / Venezia (⚠️ no es la subcuenta "omnia" de la agencia)
**Tarea ClickUp:** https://app.clickup.com/t/wdx6zepq0h

Enrutador central del pipeline de ventas: en cuanto se conoce el tipo de cliente, cada perfil toma su camino. El B2B (contratista) tiene precio especial y no se le promete instalación; el B2C (cliente final) es donde está el margen y el proceso de visita/estimado.

---

## Dependencias (todas ya creadas en Venezia)

| Recurso | ID / referencia | Estado |
| --- | --- | --- |
| Pipeline "Ventas" (6 etapas) | `G4r0zseiK4KHs1Hh3ptj` — Nuevo lead → Contactado → **Calificado** → Visita agendada → Estimado enviado → Negociación | ✅ T7 |
| Dropdown `Tipo de cliente` | Carpeta Calificación (Contratista / Cliente final) — **trigger del workflow** | ✅ T5 |
| Dropdown `¿Tiene medidas?` | Carpeta Calificación (Sí / No) | ✅ T5 |
| Dropdown `Idioma preferido` | Carpeta Calificación (ES / EN) — decide idioma de los mensajes | ✅ T5 |
| Campos `Medidas`, `Dirección instalación`, `Ciudad (proyecto)` | Carpeta Proyecto | ✅ T5 |
| Calendario "Visita / Medición" | `gshoyleB0Xbb1aLVXwIk` — link en custom value `{{custom_values.link_calendario_visitas}}` | ✅ T11 |
| Tags | `contratista`, `cliente-final`, `con-medidas`, `sin-medidas` | ✅ T6 |
| Workflow SYNC (bot→dropdown) | Rellena `Tipo de cliente` real → **es quien enciende SP01** | ⏳ T8 (bot) |

> ⚠️ **Round-robin de vendedores:** hoy solo **Stiward** tiene usuario. Aura y Alex están pendientes de alta (T1/T11). Montar el nodo de asignación con los usuarios que existan y añadir a Aura/Alex cuando tengan cuenta.

---

## Estructura del workflow

### 1 · Trigger — Contact Changed
- **Filtro:** custom field `Tipo de cliente` **is not empty** (tiene valor).
- Lo rellena el workflow SYNC cuando el dato viene del bot, o el vendedor a mano.
- **Allow re-enrollment:** ON (un contacto puede recalificarse si cambia de tipo).

### 2 · Branch principal — If/Else sobre `Tipo de cliente`
Tres ramas. Usar los **dropdowns reales**, no los campos espejo `(bot)`.

---

### Rama 3a · Contratista (B2B)
1. **Add Tag** `contratista`.
2. **Assign to user** — round-robin entre vendedores con usuario (hoy Stiward; añadir Aura/Alex).
3. **Send WhatsApp/SMS** — plantilla de bienvenida B2B, **bilingüe según `Idioma preferido`**:
   - ES: "¡Hola {{contact.first_name}}! Gracias por escribir a Venezia. Como profesional del sector tienes **precio especial de contratista**. Un asesor te contacta enseguida para tu proyecto."
   - EN: "Hi {{contact.first_name}}! Thanks for reaching out to Venezia. As a trade professional you get **special contractor pricing**. An advisor will contact you shortly about your project."
   - *(No mencionar instalación — el B2B no la incluye.)*
4. **Update Opportunity Stage** → **Calificado** (pipeline Ventas).

---

### Rama 3b · Cliente Final CON medidas (`¿Tiene medidas?` = Sí)
1. **Add Tag** `cliente-final` + `con-medidas`.
2. **If/Else** — ¿el campo `Medidas` (o fotos) está vacío?
   - **Vacío →** Send WA/SMS pidiendo medidas/fotos (bilingüe): "Para preparar tu estimado hoy mismo, ¿nos envías las medidas o unas fotos del espacio?" / "To prepare your estimate today, could you send us the measurements or a few photos of the space?"
   - **Con dato →** continúa.
3. **Update Opportunity Stage** → **Calificado**.
4. **Internal Notification** al vendedor asignado: *"Cliente final con medidas — preparar estimado HOY"* (regla del negocio: el estimado sale el mismo día).

---

### Rama 3c · Cliente Final SIN medidas (`¿Tiene medidas?` = No)
1. **Add Tag** `cliente-final` + `sin-medidas`.
2. **Send WA/SMS** con el link del calendario (bilingüe): "Agenda tu visita de medición gratis: {{custom_values.link_calendario_visitas}}" / "Book your free measuring visit: {{custom_values.link_calendario_visitas}}"
3. **Wait 24h** — condición de salida: *cita creada en calendario Visita/Medición* (si agenda, sale del wait).
4. **Recordatorio 1** (si no agendó): reenviar link, tono suave.
5. **Wait 72h** — misma condición de salida.
6. **Recordatorio 2** (si no agendó): último toque.
7. **If** sigue sin agendar → **Create Task** al vendedor: "Llamar a {{contact.first_name}} — no agendó visita".
   > 🔒 **Regla anti-spam:** máximo **2** recordatorios de agendamiento; después queda en manos del vendedor.

*(No es necesario un update de etapa aquí: la etapa "Visita agendada" la mueve SP02 cuando se crea la cita.)*

---

### 4 · (implícito en cada rama) Update de etapa
Cada rama deja la oportunidad en la etapa correcta del pipeline Ventas (Contratista y Final-con-medidas → **Calificado**; Final-sin-medidas espera a SP02).

---

## Notas de canal (EEUU)
- Venezia opera en EEUU con A2P → los **SMS del snapshot funcionan tal cual**; no hace falta migrar todo a plantillas de WhatsApp como en clientes de España.
- Si el canal elegido es WhatsApp y el contacto está fuera de la ventana de 24h, los primeros toques necesitan **plantilla Meta**; dentro de ventana (el contacto respondió) el mensaje es libre.
- Todos los textos: **bilingües ES/EN** ramificados por `Idioma preferido`.

## Prueba de cadena completa
Bot escribe campo texto → SYNC (T8) rellena el dropdown `Tipo de cliente` → **SP01 dispara** → la rama correcta deja la oportunidad en la etapa y con los tags esperados.
