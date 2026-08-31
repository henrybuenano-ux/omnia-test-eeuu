# Proyecto Venezia Kitchen Cabinets & Bath (VN Supply) — contexto para Claude Code

> **Lee `ghl-cli-v2.1/PLAYBOOK-GHL.md` antes de tocar nada.** Ahí están todos los gotchas de
> GHL aprendidos en producción. Las formas de nodos VALIDADAS están en
> `ghl-cli-v2.1/gohighlevel/utils/wf_toolkit.py` — úsalas, no fabriques atributos.
> Ver también `HANDOFF.md` (estado del proyecto) y la carpeta ClickUp "VN Supply / Venezia $$".

## 0. Cliente (lenguaje de negocio, cero jerga)
- **Venezia Kitchen Cabinets & Bath** / VN Supply · razón social **INTERNATIONAL SUPPLY COOL INC.** (EIN 81-2052650). Gabinetes, cuarzo, baños, pisos SPC. Miami/Medley + West Palm Beach, FL.
- Representante: **Stiward "Stewart" Orellana** (venezolano, cálido, NO técnico → explicar en resultados de negocio, nunca "workflow/nodo/trigger/API" en material del cliente).
- Reglas permanentes: no prometer cantidades de automatizaciones · no pisar a la chica de marketing (ads/redes son de ella; el CRM es nuestro) · **precios nunca por chat** (deriva a humano) · seguimiento sutil.

## 1. Arranque de sesión
`.env` en la raíz (NO en git — contiene secretos):
```
GHL_API_KEY=pit-...                 # Private Integration Token (API pública)
GHL_LOCATION_ID=vuAlfQCdJFMVbxxvhEml
GHL_FIREBASE_REFRESH_TOKEN=AMf-...  # API interna (workflows); si da 401, pedir uno nuevo de la extensión Chrome
```
⚠️ **Gotcha de entorno (visto acá):** el shell inyecta a veces un token de Firebase VIEJO en `os.environ`. Los scripts deben **sobreescribir** el valor del `.env` (`os.environ[k]=v`), NO usar `setdefault` (el `cargar_env` del toolkit usa setdefault → falla de refresh silenciosa).

## 2. Reglas al escribir en GHL
- **Subcuenta EN PRODUCCIÓN**: todo lo nuevo es aditivo; lo heredado no se edita ni reutiliza.
- **Idempotencia** obligatoria; **dry-run por defecto**, `--aplicar` para escribir.
- **Workflows nuevos = DRAFT** hasta revisión humana. **Publicar es SOLO por el toggle de la UI** (por API es ruleta y la lectura del estado miente — playbook §2.7).
- Tras cada PUT de workflow: `verificar_triggers()` + confirmar `allowMultiple` (`put_workflow()` lo maneja).
- **Textos para UI de bots: contar caracteres SIEMPRE** (límite 500 en campos de acciones; entregar el conteo).
- La verdad está en la API + prueba en vivo, no en el panel (cachea).

## 3. Protocolo de pruebas
- 1 prueba = 1 contacto nuevo, creado CON etiquetas ANTES de escribir.
- Verificar por API (registro de auditoría "ojito"), no por el panel del contacto.

## 4. Gestión
- `HANDOFF.md` = estado vivo del proyecto. ClickUp folder "VN Supply / Venezia $$" = tareas.
- El `.env` NUNCA se commitea.

## 5. IDs del proyecto (Venezia · subcuenta `vuAlfQCdJFMVbxxvhEml`)

### Pipelines / etapas
| Pipeline | ID | Etapas |
|---|---|---|
| Ventas | `G4r0zseiK4KHs1Hh3ptj` | Nuevo lead (`d299bb27-6274-4666-8fa5-f3095ae12561`) · Calificado (`408a08cb-15f3-4f66-a52e-4e13457880d4`) · Visita agendada · Estimado enviado · Negociación |
| Proyectos Activos | `8vHsYiJP4MhrE3kBuABz` | Pagado · Fabricación · Listo para instalar · Instalación · Terminado |
| Reseñas de Google | `k3FujnI2kbdTdvqXZf4J` | Da clic para votar · Votaron 1-3 · Votaron 4-5 · Dejó reseña |

### Bot / calendario / usuario / form
| Qué | ID |
|---|---|
| Agente Conversation AI "Venezia" (UI) | `bwrV3bQiCiK9YzgjguVj` |
| Calendario "Visita / Medición" | `gshoyleB0Xbb1aLVXwIk` |
| Usuario Stiward | `cBFAFxd1X1nlExXiYh6n` |
| Form "Formulario nuevo lead" | `eOlPYYCyBqHfbr9rurAM` |

### Workflows (todos publicados salvo nota)
| Nombre | ID |
|---|---|
| LS01 · Entrada WhatsApp | `fafda04c-92fc-4a87-a67b-747283e84f4f` |
| LS02 · Entrada Instagram (draft) | `da80e76b-efee-48a9-bb9c-35e99447877a` |
| LS03 · Formulario Web (draft) | `3d1aafbb-adff-4c85-a391-c57037fbe755` |
| SP01 · Calificación | `78905a7e-9f2a-4311-a39b-5117d7f332f8` |
| SP02 · Visita agendada (anti no-show) | `7847d6d3-389f-40dc-980f-447b691583e6` |
| SP02.1 · Visita agendada (show) | `4123a621-1d4d-4a62-8b8a-a908c7f0ceba` |
| SP02.2 · Visita agendada (Cancel/no-show) | `7874a1f2-1d39-4273-ac31-11df054fe117` |
| SP03 · Estimado enviado + seguimiento | `b0758d53-f104-48b2-9b85-3d5b4c445051` |
| SP04 · Reactivación base 670 (draft) | `9068063e-28ab-4843-aba7-f2db36340ceb` |
| SP05 · Pagado / WON | `4f7ddf83-1081-4a4a-afe6-b23371be6e26` |
| SYNC · Tipo de cliente | `bd2fdfa7-6475-42a3-8dc0-8ce2e053639f` |
| SYNC · ¿Tiene medidas? | `38f637f9-7b04-4e62-aeb4-5d0b5ea4a1b4` |
| SYNC · Idioma | `4b70faef-9975-4d1f-a58c-515be02566fe` |
| AP01-a Pagado / -b Listo / -c Instalación / -d Terminado / Fabricación | `58aee8f9…` / `af7a8621…` / `02443c51…` / `3668cb43…` / `756a0989…` |
| RBD 01–05 (reseñas Google) | `c0e26ee1…` `f89e6e17…` `aeae702d…` `8fd70388…` `fe2d1e77…` |
| SETUP · Apagar IA — clientes Clover | `8ecdc1fb-f138-48f1-98bd-76ba8837dbe8` (folder `c954dac0-…`) |

### Custom fields clave (dropdown real ↔ espejo texto `(bot)`)
| Campo | Dropdown/real | Espejo `(bot)` (texto) |
|---|---|---|
| Tipo de cliente | `uRyyBlP4qXHQt8NPCPaI` | `w4pYiqNYkQK7NvULIWJp` |
| ¿Tiene medidas? | `ey7voH2m0srqqsdlOMSJ` | `5wJ6ih7H7GtQMJ0iZqYf` |
| Idioma preferido | `NWjGFvTx97l1HIKjdaGw` | `Sz4ekQZPeV2Oori3Ls79` |
| Producto de interés | `ySuO57WB78pe6UUTjbz9` | `1EPzs8q0Z5MsYbuIaSZ5` |
| Ciudad (bot) | — | `gZsMVx9y44eaWx56H6Ca` |

Otros: Medidas/notas `RZnnavHf90AUBc9SV2r8` · STATUS DEL LEAD `2GXRWRmV0Eqs1TOahh6D` · Link PDF estimado `Az68QcAeuDNt0nUhj86m` · Fecha última respuesta `t6cCPPhtqpykq9Brobzf` · **Origen Clover** `oJlElAPUTTFwmGiJDIkG` · Es cliente desde `ZYzi4NUjvrDdwUvTxHwO` · Marketing permitido `q7y7zsPJcLNWH2GYxb1X`.

### Tags operativos
`contratista` · `cliente-final` · `con-medidas` · `sin-medidas` · **`cliente-antiguo`** (Clover → IA apagada) · `human handover`.

## 6. Migración Clover (hecha)
Base limpia: **3,704 contactos únicos** (2,529 con Marketing=Yes). Archivo: `Venezia_Clover_import_GHL.csv`. Los `Origen Clover` no vacíos = clientes viejos → tag `cliente-antiguo` → IA apagada (workflow SETUP + filtro en LS01).
