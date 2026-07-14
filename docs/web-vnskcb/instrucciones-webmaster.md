# Instrucciones para el webmaster — veneziakcb.com

**De:** Equipo CRM de VN Supply / Venezia Kitchen Cabinets
**Objetivo:** 3 cambios puntuales en la página. Son necesarios para que la empresa pueda activar mensajes de texto (registro A2P con las operadoras de EE. UU.).

---

## 1. Links en el footer (en TODAS las páginas del sitio)

Agregar en el pie de página dos enlaces, **visibles para cualquier visitante**, con estos textos exactos en inglés:

| Texto del enlace | URL de destino |
|---|---|
| Terms and Conditions | `https://veneziakcb.com/terms-and-conditions/` |
| Privacy Policy | `https://veneziakcb.com/privacy-policy/` |

Notas:
- Las dos páginas **ya existen y funcionan** — están como carpetas estáticas en `public_html/terms-and-conditions/` y `public_html/privacy-policy/`. **No moverlas, renombrarlas ni borrarlas.**
- Si prefieres ponerlos como HTML directo:

```html
<div style="text-align:center; padding:12px 0; font-size:14px;">
  <a href="https://veneziakcb.com/terms-and-conditions/">Terms and Conditions</a>
  &nbsp;|&nbsp;
  <a href="https://veneziakcb.com/privacy-policy/">Privacy Policy</a>
</div>
```

- Deben verse en el footer de **todas** las páginas (el revisor del registro entra a la home y busca estos links abajo).

---

## 2. Widget de chat (script global)

Pegar el siguiente código **justo antes de la etiqueta `</body>`** de la plantilla del sitio, para que cargue en todas las páginas (es una burbuja de chat flotante):

```html
<!-- Chat widget — VN Supply / Venezia -->
<script src="https://widgets.leadconnectorhq.com/loader.js"
  data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js"
  data-widget-id="6a56689cc6e06ac8e8af88e4"></script>
```

Notas:
- En Joomla: editar el `index.php` de la plantilla activa (o el módulo de footer si el sitio usa uno con posición global).
- El script no interfiere con el diseño — solo agrega la burbuja de chat abajo a la derecha.

---

## 3. Formulario de contacto (embed en una página)

Pegar el siguiente código embed (iframe) **dentro del contenido** de la página de contacto/cotización que indique el cliente (o crear una página nueva "Free Estimate" con su ítem de menú):

```html
<!-- Formulario nuevo lead — VN Supply / Venezia -->
<iframe
    src="https://link.veneziakcb.com/widget/form/eOlPYYCyBqHfbr9rurAM"
    style="width:100%;height:745px;border:none;border-radius:8px"
    id="inline-eOlPYYCyBqHfbr9rurAM"
    data-layout="{'id':'INLINE'}"
    data-trigger-type="alwaysShow"
    data-trigger-value=""
    data-activation-type="alwaysActivated"
    data-activation-value=""
    data-deactivation-type="neverDeactivate"
    data-deactivation-value=""
    data-form-name="Formulario nuevo lead"
    data-height="745"
    data-layout-iframe-id="inline-eOlPYYCyBqHfbr9rurAM"
    data-form-id="eOlPYYCyBqHfbr9rurAM"
    title="Formulario nuevo lead">
</iframe>
<script src="https://link.veneziakcb.com/js/form_embed.js"></script>
```

Notas:
- El iframe es responsive; darle ancho completo del contenedor.
- En el editor de Joomla, pegar en modo **código/HTML** (no en el editor visual, porque recorta los iframes). Si el editor es TinyMCE, usar el botón "Toggle Editor" o "Code".

---

## Checklist de verificación (cuando termines)

- [ ] En la home, abajo en el footer, se ven "Terms and Conditions" y "Privacy Policy" y ambos links abren bien
- [ ] Los links también se ven en las demás páginas del sitio
- [ ] La burbuja de chat aparece en todas las páginas y abre al hacer clic
- [ ] El formulario se ve completo en su página y al enviarlo llega la confirmación
- [ ] Nada más del sitio cambió (menú, diseño, imágenes intactos)

Cualquier duda técnica, escribir a este mismo contacto. Gracias 🙏
