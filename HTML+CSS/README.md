# Workshop 2 - Website (HTML + CSS)

## Web Applications - Semester II 2026

This project is the continuation of Workshop 1. The original HTML website was modified by adding CSS to improve the layout and visual presentation of its content.

## Main improvements

- The CSS was split into several thematic stylesheets instead of one large file, following the structure proposed in the workshop guide.
- Each page only links the stylesheets it actually needs.
- The header and navigation menu were redesigned.
- Sections and articles use spacing, borders, rounded corners and shadows.
- Images are responsive and visually consistent.
- The weekly schedule table was styled and made horizontally scrollable on small screens.
- The contact form was styled for clearer input and button presentation.
- Responsive rules were added for mobile devices.

## Stylesheets

| File | Purpose | Used on |
|---|---|---|
| `css/base.css` | Reset, typography, colors, links | All pages |
| `css/layout.css` | Header, nav, main wrapper, footer | All pages |
| `css/components.css` | Sections, articles, images | All pages |
| `css/tables.css` | Table styling | `pages/schedule.html` |
| `css/forms.css` | Form styling | `pages/contact.html` |
| `css/responsive.css` | Media queries for mobile | All pages (loaded last) |

## Project structure

```text
HTML+CSS/
├── index.html
├── README.md
├── css/
│   ├── base.css
│   ├── layout.css
│   ├── components.css
│   ├── tables.css
│   ├── forms.css
│   └── responsive.css
├── images/
│   ├── profile.png
│   ├── img1.png
│   ├── img2.jpeg
│   └── img3.jpeg
└── pages/
    ├── contact.html
    ├── courses.html
    ├── hobbies.html
    ├── resources.html
    └── schedule.html
```

## Author

Paúl Rodríguez
