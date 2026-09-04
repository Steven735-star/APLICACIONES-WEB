# B&B — Bit and Bolt

**Workshop 3 — Web Applications**  
**Students:** Steven Rodríguez and Kevin Erazo  
**Semester:** II 2026  
**Technologies:** HTML5, CSS3, JavaScript, and jQuery

## Project Description

**B&B — Bit and Bolt** is a responsive technical service website focused on computers and smartphones.

The website presents services such as:

- Computer preventive maintenance for **$15**
- Software diagnosis and troubleshooting
- Hardware diagnosis and repair
- SSD and RAM upgrades
- Smartphone technical support
- System optimization and cleanup
- Remote software support through **AnyDesk**

The website was designed with a modern technology-oriented interface, clear service information, visible contact options, and responsive behavior for desktop, tablet, and mobile devices.

## Contact

**Phone / WhatsApp:** 0960438690

## How to Run the Project

1. Download or clone the project repository.
2. Open the project folder.
3. Open `index.html` in a modern web browser.

For a better development experience, you can also run a local server:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

An Internet connection may be required to load external resources such as jQuery or web fonts.

## Workshop Requirements Covered

The project includes all the main requirements requested in Workshop 3:

- Navigation bar with at least three links
- Hero section with a heading, short description, and action button
- Image gallery with at least four images
- Contact form with:
  - Name
  - Email
  - Message
  - Submit button
- CSS Flexbox and Grid layouts
- Hover effects on navigation links and buttons
- Responsive design using media queries
- jQuery interaction to randomly change the Hero background color
- jQuery image gallery with popup modal
- jQuery form validation
- Success alert with the required message:

```text
Form submitted successfully!
```

## Additional Features

The website also includes:

- Responsive mobile navigation
- Service cards
- Remote support section
- AnyDesk support information
- Service rating with stars
- Dynamic form fields
- Message character counter
- Direct WhatsApp contact
- Accessible gallery modal
- Keyboard support for closing the modal with the `Escape` key

## Project Structure

```text
RodriguezSteven_ErazoKevin/
├── index.html
├── style.css
├── script.js
├── README.md
├── REPORT.html
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

## Form Behavior

The workshop requires client-side validation but does not require a backend.

For this reason, the contact form validates the information entered by the user and displays the required success message when the data is valid, but it does not permanently store or send the submitted information to a server.

## Remote Support

Remote assistance is intended mainly for software-related problems that can be solved without physically accessing the device.

Remote sessions may be performed using **AnyDesk**, with the customer's authorization.

Examples of remote support include:

- Software installation
- Operating system configuration
- Performance optimization
- Application troubleshooting
- Driver-related problems
- Basic malware cleanup
- General software support

Hardware repairs, physical maintenance, and component replacements require direct technical service.

## Authors

- **Steven Rodríguez**
- **Kevin Erazo**

---

**B&B — Bit and Bolt**  
*Computer & Mobile Technical Service*