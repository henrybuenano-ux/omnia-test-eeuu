# LS01 · Entrada de leads — Runbook de implementación (GHL)

> **Cliente:** VN Supply / Venezia (Medley, FL)
> **Tarea ClickUp:** [LS01 · Entrada WhatsApp](https://app.clickup.com/t/wdx6zepq0d) — lista *🔵 02 · Lead Sources — LS01, LS02, LS03*
> **Objetivo:** registrar al lead entrante con su fuente/anuncio, crear la oportunidad en Ventas y encender el bot de calificación.
>
> **⚠️ Estrategia de despliegue:** el workflow se construye y publica primero en **versión SMS** (v1). Cuando las plantillas de WhatsApp estén creadas y aprobadas por Meta, se cambian manualmente los nodos marcados con 🔁 a WhatsApp (v2 — diseño final, ya que WA es el canal dominante: 42 de las últimas 50 conversaciones). La sección 5 tiene el checklist exacto de migración.

---

## 1. Prerrequisitos (verificar antes de construir)

| Dependencia | Dónde | Estado |
| --- | --- | --- |
| Registro A2P aprobado (habilita SMS) | Trust Center | ✅ T3 completo |
| Número en la subcuenta con SMS activo | Settings → Phone Numbers | Verificar |
| Pipeline **Ventas** con etapa **Nuevo lead** | Settings → Pipelines | ✅ creado (T7 · 6 etapas + won/lost) |
| Custom fields de atribución: `Fuente`, `Campaña`, `Anuncio de origen`, `Canal de entrada` | Settings → Custom Fields → grupo *Atribución* | ⚠️ subtarea de setup aún en *to do* — crearlos primero si faltan |
| Tags de canal (`sms`, `whatsapp`) | Settings → Tags | Crear si no existen |
| Bot Conversation AI configurado (aunque sea en borrador) | AI Agents → Conversation AI | Necesario para el nodo 6 |
| Horario de atención definido | Settings → Business Profile | Usado por la rama fuera de horario (nodo 7) |
| Usuarios Aura y Alex activos | Settings → My Staff | ✅ creados — reciben la notificación interna |

*(Para v2: integración WhatsApp activa + plantillas aprobadas.)*

---

## 2. Creación del workflow — v1 SMS

**Ruta:** Automation → Workflows → **Create Workflow** → *Start from scratch*
**Nombre:** `LS01 · Entrada WhatsApp` (mantener el nombre del diseño final; la versión SMS es transitoria)
**Carpeta sugerida:** `02 · Lead Sources`

### Nodo 1 — Trigger: Customer Replied 🔁
- **Tipo:** Trigger `Customer Replied`
- **Filtro v1:** `Reply Channel` = **SMS**
- No agregar filtro de "primera vez": el anti-duplicado se resuelve en el nodo 2 para cubrir también contactos existentes sin oportunidad abierta.

### Nodo 2 — If/Else: anti-duplicado
- **Condición:** ¿el contacto tiene una **oportunidad abierta** en el pipeline **Ventas**?
  - En GHL: branch con condición `Opportunity` → `Pipeline = Ventas` + `Status = Open`.
- **Rama Sí:** → **End** (el lead ya está en gestión; no duplicar oportunidad ni reiniciar bot).
- **Rama No:** continúa al nodo 3.

### Nodo 3 — Update Contact Field: atribución 🔁
- **v1:** `Fuente` = **SMS** · `Canal de entrada` = **SMS**
- `Campaña` y `Anuncio de origen`: **dejar vacíos en v1** (el referral CTWA solo existe en WhatsApp). Atribución solo hacia adelante — no adivinar.

### Nodo 4 — Add Tag: tag de canal 🔁
- **v1:** tag `sms`

### Nodo 5 — Create Opportunity
- **Pipeline:** Ventas
- **Etapa:** Nuevo lead
- **Nombre de oportunidad:** `{{contact.name}} — Lead entrante`
- **Status:** Open

### Nodo 6 — Conversation AI: Bot ON
- Acción que habilita el bot en la conversación (arranca la calificación contratista / cliente final).
- Verificar que el contacto **no** tenga el tag `stop bot` (si la taxonomía de control ya está activa, agregar esa condición antes de encender el bot).
- Sin cambios entre v1 y v2: el bot responde por el mismo canal de la conversación.

### Nodo 7 — If/Else + Internal Notification: fuera de horario
- **Condición:** hora actual fuera del horario de atención del negocio.
  - Implementación práctica en GHL: rama If/Else sobre ventana horaria, o acción `Wait until business hours` + notificación.
- **Rama fuera de horario:** `Internal Notification` a **Aura y Alex** — "Lead nuevo fuera de horario: {{contact.name}} {{contact.phone}}. Retomar en la mañana."
- **Rama dentro de horario:** → End.
- Sin cambios entre v1 y v2 (las notificaciones internas no usan plantillas).

### Settings del workflow
- **Allow re-entry:** **No** mientras la oportunidad siga abierta (el anti-duplicado del nodo 2 es la segunda barrera).
- **Timezone:** America/New_York (heredada de la subcuenta).
- **Estado inicial:** guardar en **Draft** hasta pasar el QA de la sección 4.

---

## 3. Mapa subtareas ClickUp → nodos

| Subtarea ClickUp | Nodo |
| --- | --- |
| [Trigger: mensaje WhatsApp entrante…](https://app.clickup.com/t/wdx6zepq3g) | 1 (v1 con SMS) |
| [Filtro anti-duplicado: si ya tiene oportunidad abierta → salir](https://app.clickup.com/t/wdx6zepq3h) | 2 |
| [Set atribución: Fuente=WhatsApp + campaña/anuncio (referral CTWA)](https://app.clickup.com/t/wdx6zepq3j) | 3 (CTWA queda para v2) |
| [Set canal de entrada = WA + tag de canal](https://app.clickup.com/t/wdx6zepq3k) | 3–4 (v1 con SMS) |
| [Crear oportunidad en Ventas → etapa "Nuevo lead"](https://app.clickup.com/t/wdx6zepq3n) | 5 |
| [Activar bot Conversation AI](https://app.clickup.com/t/wdx6zepq3p) | 6 |
| [Notificación interna si llega fuera de horario](https://app.clickup.com/t/wdx6zepq3q) | 7 |

Al completar cada nodo en GHL, marcar la subtarea correspondiente en ClickUp. Las subtareas con parte WhatsApp pendiente (trigger y atribución CTWA) se cierran recién con la migración v2.

---

## 4. Checklist de QA — v1 SMS (antes de publicar)

1. **Lead nuevo, dentro de horario:** enviar SMS desde un número de prueba →
   - contacto creado con `Fuente=SMS`, `Canal de entrada=SMS`, tag `sms`;
   - oportunidad en Ventas / Nuevo lead (una sola);
   - el bot responde por SMS (calificación arranca).
2. **Lead repetido:** volver a escribir desde el mismo número con la oportunidad abierta →
   - NO se crea segunda oportunidad, NO se reinicia el bot (sale por la rama Sí del nodo 2).
3. **Fuera de horario:** mensaje de prueba fuera del horario del negocio → Aura y Alex reciben la notificación interna; el resto del flujo se completa igual.
4. **Re-entry:** confirmar en Settings que el workflow no re-procesa al mismo contacto con oportunidad abierta.
5. Publicar el workflow (Draft → **Publish**) y registrar la fecha en la tarea de ClickUp.

---

## 5. Migración manual v1 → v2 (cuando las plantillas WA estén aprobadas)

Cambios a aplicar, nodo por nodo (los marcados 🔁 en la sección 2):

| Nodo | Campo | v1 (SMS) | v2 (WhatsApp) |
| --- | --- | --- | --- |
| 1 · Trigger | Reply Channel | SMS | **WhatsApp** |
| 3 · Update Contact Field | `Fuente` | SMS | **WhatsApp** |
| 3 · Update Contact Field | `Canal de entrada` | SMS | **WA** |
| 3 · Update Contact Field | `Campaña` / `Anuncio de origen` | vacíos | **mapear desde referral CTWA** si el mensaje viene de un ad (merge fields del trigger según lo que exponga la integración WA) |
| 4 · Add Tag | tag | `sms` | **`whatsapp`** |

Pasos de la migración:
1. Confirmar plantillas WA aprobadas en Meta y la integración de WhatsApp activa en la subcuenta.
2. Editar el workflow publicado y aplicar la tabla de arriba (GHL permite editar en caliente; guardar como nueva versión).
3. Re-correr el QA de la sección 4 con mensajes de WhatsApp, y agregar estos dos casos:
   - **Lead desde ad CTWA:** click en anuncio de prueba → `Campaña`/`Anuncio de origen` poblados.
   - **Lead orgánico WA:** mensaje directo sin ad → `Campaña`/`Anuncio` quedan vacíos.
4. Decidir qué hacer con la entrada SMS: si se quiere conservar SMS como canal secundario, duplicar el workflow como `LS01b · Entrada SMS` antes de cambiar los nodos (así quedan ambos canales cubiertos sin mezclar atribución).
5. Marcar en ClickUp las subtareas de trigger WA y atribución CTWA, y dejar comentario con la fecha del cambio.

---

## 6. Notas y riesgos

- **Campos de atribución faltantes:** el grupo *Atribución* de custom fields sigue en *to do* en el setup (tarea `wdx6zepq1r`). Sin esos campos, el nodo 3 no puede guardarse — crearlos es el primer paso real de la construcción.
- **Sesiones de WhatsApp vs plantillas:** las respuestas dentro de la ventana de 24 h abierta por el lead no requieren plantilla; las plantillas son necesarias para mensajes iniciados por el negocio (recordatorios, seguimientos de SP01–SP04). Aun así, arrancar en SMS evita depender de la aprobación de Meta para poner LS01 en producción.
- **Interacción con `stop bot`:** si un humano ya tomó la conversación, el nodo 6 no debe reactivar el bot; la condición por tag cubre ese caso.
- Este workflow es el gemelo de **LS02 · Entrada Instagram** (ya completo y publicado): reutilizar su estructura de anti-duplicado y creación de oportunidad como referencia dentro de la subcuenta.
