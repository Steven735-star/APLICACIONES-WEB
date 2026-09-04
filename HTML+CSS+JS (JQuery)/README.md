# Workshop 3 — SRK TechCare

**Autores:** Steven Rodríguez y Kevin Erazo  
**Asignatura:** Web Applications — Semester II 2026  
**Tecnologías:** HTML5, CSS3, JavaScript y jQuery 4.0.0

## Descripción
SRK TechCare es una página web responsive de servicio técnico para computadoras y celulares. Presenta mantenimiento preventivo de computadoras desde $15, diagnóstico de software/hardware y soporte remoto mediante AnyDesk.

## Cómo ejecutar
1. Descomprime la carpeta `RodriguezSteven_ErazoKevin`.
2. Abre `index.html` en un navegador moderno con conexión a Internet para cargar jQuery y la tipografía web.
3. También puedes ejecutar un servidor local desde esta carpeta:
   - Python: `python3 -m http.server 8000`
   - Abre `http://localhost:8000`

## Requisitos del Workshop cubiertos
- Navigation Bar con más de tres enlaces.
- Hero Section con título, descripción y botón.
- Galería de cuatro imágenes.
- Formulario con nombre, email, mensaje y botón de envío.
- CSS Flexbox y Grid.
- Efectos hover.
- Diseño responsive mediante media queries.
- jQuery: botón del Hero cambia el color de fondo aleatoriamente.
- jQuery: galería abre imágenes en un popup modal.
- jQuery: validación de formulario y alerta exacta `Form submitted successfully!`.
- Funcionalidades adicionales: menú móvil, calificación por estrellas, contador de caracteres y contacto directo por WhatsApp.

## Estructura
```
RodriguezSteven_ErazoKevin/
├── index.html
├── style.css
├── script.js
├── REPORT.html
├── README.md
├── REPOSITORY_LINK.txt
└── assets/
    ├── logo.svg
    ├── favicon.svg
    ├── gallery-computer.svg
    ├── gallery-phone.svg
    ├── gallery-remote.svg
    ├── gallery-upgrade.svg
    └── screenshot-desktop.png
```

## Nota sobre el formulario
El workshop exige validación en el navegador, no un backend. Por eso, el formulario demuestra validación y muestra el mensaje solicitado, pero no almacena ni envía datos a un servidor.
