# LS01 · Entrada WhatsApp — Runbook de implementación (GHL)

> **Cliente:** VN Supply / Venezia (Medley, FL)
> **Tarea ClickUp:** [LS01 · Entrada WhatsApp](https://app.clickup.com/t/wdx6zepq0d) — lista *🔵 02 · Lead Sources — LS01, LS02, LS03*
> **Objetivo:** WhatsApp es el canal dominante verificado (42 de las últimas 50 conversaciones). Este workflow registra al lead con su fuente/anuncio, crea la oportunidad en Ventas y enciende el bot de calificación.

---

## 1. Prerrequisitos (verificar antes de construir)

| Dependencia | Dónde | Estado esperado |
| --- | --- | --- |
| Integración WhatsApp activa en la subcuenta | Settings → WhatsApp | Número conectado y aprobado |
| Pipeline **Ventas** con etapa **Nuevo lead** | Settings → Pipelines | ✅ creado (T7 · 6 etapas + won/lost) |
| Custom fields de atribución: `Fuente`, `Campaña`, `Anuncio de origen`, `Canal de entrada` | Settings → Custom Fields → grupo *Atribución* | ⚠️ subtarea de setup aún en *to do* — crearlos primero si faltan |
| Tag de canal (`whatsapp` / `canal-wa`) | Settings → Tags | Crear si no existe |
| Bot Conversation AI configurado (aunque sea en borrador) | AI Agents → Conversation AI | Necesario para el paso 6 |
| Horario de atención definido | Settings → Business Profile | Usado por la rama fuera de horario (paso 7) |
| Usuarios Aura y Alex activos | Settings → My Staff | ✅ creados — reciben la notificación interna |

---

## 2. Creación del workflow

**Ruta:** Automation → Workflows → **Create Workflow** → *Start from scratch*
**Nombre:** `LS01 · Entrada WhatsApp`
**Carpeta sugerida:** `02 · Lead Sources`

### Nodo 1 — Trigger: Customer Replied
- **Tipo:** Trigger `Customer Replied`
- **Filtro:** `Reply Channel` = **WhatsApp**
- No agregar filtro de "primera vez": el anti-duplicado se resuelve en el nodo 2 para cubrir también contactos existentes sin oportunidad abierta.

### Nodo 2 — If/Else: anti-duplicado
- **Condición:** ¿el contacto tiene una **oportunidad abierta** en el pipeline **Ventas**?
  - En GHL: branch con condición `Opportunity` → `Pipeline = Ventas` + `Status = Open`.
- **Rama Sí:** → **End** (el lead ya está en gestión; no duplicar oportunidad ni reiniciar bot).
- **Rama No:** continúa al nodo 3.

### Nodo 3 — Update Contact Field: atribución
- `Fuente` = **WhatsApp**
- `Canal de entrada` = **WA**
- `Campaña` y `Anuncio de origen`: mapear desde el **referral CTWA** (Click-to-WhatsApp) si existe:
  - Usar los merge fields del trigger (`{{message.ad_source_id}}` / datos de referral del mensaje) según lo que exponga la integración de WhatsApp de la subcuenta.
  - Si el mensaje NO viene de un ad, dejar `Campaña`/`Anuncio` vacíos — **atribución solo hacia adelante**, no adivinar.

### Nodo 4 — Add Tag: tag de canal
- Agregar tag `whatsapp` (o el tag de canal definido en la taxonomía T6).

### Nodo 5 — Create Opportunity
- **Pipeline:** Ventas
- **Etapa:** Nuevo lead
- **Nombre de oportunidad:** `{{contact.name}} — WhatsApp`
- **Status:** Open

### Nodo 6 — Conversation AI: Bot ON
- Acción que habilita el bot en la conversación (arranca la calificación contratista / cliente final).
- Verificar que el contacto **no** tenga el tag `stop bot` (si la taxonomía de control ya está activa, agregar esa condición antes de encender el bot).

### Nodo 7 — If/Else + Internal Notification: fuera de horario
- **Condición:** hora actual fuera del horario de atención del negocio.
  - Implementación práctica en GHL: rama If/Else sobre ventana horaria, o acción `Wait until business hours` + notificación.
- **Rama fuera de horario:** `Internal Notification` a **Aura y Alex** — "Lead nuevo por WhatsApp fuera de horario: {{contact.name}} {{contact.phone}}. Retomar en la mañana."
- **Rama dentro de horario:** → End.

### Settings del workflow
- **Allow re-entry:** **No** mientras la oportunidad siga abierta (el anti-duplicado del nodo 2 es la segunda barrera).
- **Timezone:** America/New_York (heredada de la subcuenta).
- **Estado inicial:** guardar en **Draft** hasta pasar el QA de la sección 4.

---

## 3. Mapa subtareas ClickUp → nodos

| Subtarea ClickUp | Nodo |
| --- | --- |
| [Trigger: mensaje WhatsApp entrante…](https://app.clickup.com/t/wdx6zepq3g) | 1 |
| [Filtro anti-duplicado: si ya tiene oportunidad abierta → salir](https://app.clickup.com/t/wdx6zepq3h) | 2 |
| [Set atribución: Fuente=WhatsApp + campaña/anuncio (referral CTWA)](https://app.clickup.com/t/wdx6zepq3j) | 3 |
| [Set canal de entrada = WA + tag de canal](https://app.clickup.com/t/wdx6zepq3k) | 3–4 |
| [Crear oportunidad en Ventas → etapa "Nuevo lead"](https://app.clickup.com/t/wdx6zepq3n) | 5 |
| [Activar bot Conversation AI](https://app.clickup.com/t/wdx6zepq3p) | 6 |
| [Notificación interna si llega fuera de horario](https://app.clickup.com/t/wdx6zepq3q) | 7 |

Al completar cada nodo en GHL, marcar la subtarea correspondiente en ClickUp.

---

## 4. Checklist de QA (antes de publicar)

1. **Lead nuevo, dentro de horario:** enviar WA desde un número de prueba →
   - contacto creado con `Fuente=WhatsApp`, `Canal de entrada=WA`, tag de canal;
   - oportunidad en Ventas / Nuevo lead (una sola);
   - el bot responde (calificación arranca).
2. **Lead repetido:** volver a escribir desde el mismo número con la oportunidad abierta →
   - NO se crea segunda oportunidad, NO se reinicia el bot (sale por la rama Sí del nodo 2).
3. **Lead desde ad CTWA:** click en anuncio de prueba → `Campaña`/`Anuncio de origen` poblados.
4. **Lead orgánico:** mensaje directo sin ad → `Campaña`/`Anuncio` quedan vacíos.
5. **Fuera de horario:** mensaje de prueba fuera del horario del negocio → Aura y Alex reciben la notificación interna; el resto del flujo se completa igual.
6. **Re-entry:** confirmar en Settings que el workflow no re-procesa al mismo contacto con oportunidad abierta.
7. Publicar el workflow (Draft → **Publish**) y registrar la fecha en la tarea de ClickUp.

---

## 5. Notas y riesgos

- **Campos de atribución faltantes:** el grupo *Atribución* de custom fields sigue en *to do* en el setup (tarea `wdx6zepq1r`). Sin esos campos, el nodo 3 no puede guardarse — crearlos es el primer paso real de la construcción.
- **Referral CTWA:** la disponibilidad de campaña/anuncio depende de que el número de WhatsApp esté conectado vía la integración nativa; validar con un ad de prueba antes de dar la atribución por buena.
- **Interacción con `stop bot`:** si un humano ya tomó la conversación, el nodo 6 no debe reactivar el bot; la condición por tag cubre ese caso.
- Este workflow es el gemelo de **LS02 · Entrada Instagram** (ya completo y publicado): reutilizar su estructura de anti-duplicado y creación de oportunidad como referencia dentro de la subcuenta.
