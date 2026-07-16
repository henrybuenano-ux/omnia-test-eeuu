# Sistema de reseñas Google — Snapshot RBD (Venezia / VN Supply)

**Fecha:** 16/07/2026
**Decisión:** el workflow de reseñas diseñado a mano (`PS01 · Encuesta de satisfacción + Google Review`) queda **cancelado** y se sustituye por el **snapshot estándar de reseñas (RBD)** que ya se implementa para todos los clientes (mismo sistema escaneado e inventariado en Termycal el 14/07).

## Fuente

Inventario de la carpeta de automatizaciones "Reseñas de Google" del snapshot, documentado en ClickUp:

- Tarea origen (Termycal): `[RBD] Sistema de reseñas Google (snapshot) — inventario + adaptaciones` — https://app.clickup.com/t/wdx6zeq7wx
- Tarea nueva (Venezia): `[RBD] Sistema de reseñas Google (snapshot) — importación + adaptaciones Venezia` — https://app.clickup.com/t/wdx6zeqek6
- Tarea cancelada (diseño manual): https://app.clickup.com/t/wdx6zepq0q

## Piezas del snapshot

| Pieza | Notas |
| --- | --- |
| Pipeline "Reseñas de Google" | 4 etapas: Da clic → Votaron 1-3 → Votaron 4-5 → Dejó reseña |
| Survey 1-5 | Con redirect a Google para los 4-5 |
| Form "Valoración - Comentarios 1-3" | Gestión privada del insatisfecho |
| Trigger link de valoración | Lo envía el conector |
| Custom value link de Google | En Venezia ya existe el slot 🟡 "Link Google Review" (T9), pendiente del link real "write a review" del GBP |

Los IDs son propios de cada subcuenta: se completan tras importar el snapshot en Venezia (subtarea 00).

## Workflows

| Workflow | Función | Adaptaciones clave para Venezia |
| --- | --- | --- |
| AP01-RBD (conector) | Oportunidad → Terminado (Proyectos Activos) → Wait 24-48h → envía trigger link | SMS vía A2P sirve tal cual (EEUU); mensaje bilingüe EN/ES; allow re-enrollment ON |
| RBD 01 | Clic en trigger link → tag + nota + oportunidad "Da clic para votar" | Eliminar nodo "Remove from Workflow FT1 reactivación" (no existe en esta subcuenta) |
| RBD 02 | Votó 1-3 → form privado + alerta interna | Avisos a Stewart (llamada de recuperación); el 1-3 NUNCA recibe link de Google; form bilingüe |
| RBD 03 | Votó 4-5 → etapa + avisos; el redirect del survey lleva a Google | Verificar custom field de score importado; redirect al GBP de Venezia; guardar link en custom value |
| RBD 04 | "No puedo entrar al link" → reenvío de link directo | Frases del trigger en EN y ES; link desde custom value |
| RBD 05 | Review Received (Google) → oportunidad "Dejó reseña" + WON + avisos | Requiere GBP conectado; assign/avisos a Stewart; sustituye al tag manual `review-dejada` y al re-ask del diseño anterior |

## Principio del sistema

Encuesta-filtro: el insatisfecho (1-3) se gestiona en privado y se convierte en llamada de recuperación; solo el cliente contento (4-5) llega a Google. La detección de reseña dejada es real (trigger Review Received vía Google Business Profile), no por confirmación del cliente.
