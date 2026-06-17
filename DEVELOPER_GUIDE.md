# Urugano Realty — Developer Guide

Housing platform for international students and expats in Rwanda. Built as a Frappe app.

---

## Table of Contents

1. [Stack](#stack)
2. [Project Structure](#project-structure)
3. [Getting Started](#getting-started)
4. [DocTypes](#doctypes)
5. [Pages & Routing](#pages--routing)
6. [Python Controllers](#python-controllers)
7. [API Endpoints](#api-endpoints)
8. [Template System](#template-system)
9. [Reusable Components](#reusable-components)
10. [Design System](#design-system)
11. [Icons](#icons)
12. [Adding a New Page](#adding-a-new-page)
13. [Adding a New API Endpoint](#adding-a-new-api-endpoint)

---

## Stack

| Layer | Technology |
|---|---|
| Framework | [Frappe](https://frappeframework.com) (Python) |
| Templating | Jinja2 (server-rendered HTML) |
| CSS | Tailwind CSS v4 (`@import "tailwindcss"`) |
| Interactivity | [Alpine.js](https://alpinejs.dev) v3 (CDN, `defer`) |
| Icons | [Lucide](https://lucide.dev) (CDN, `@latest`) |
| Database | MariaDB (via Frappe ORM) |

---

## Project Structure

```
urugano/
├── api.py                          # Whitelisted API endpoints
├── hooks.py                        # App config, route rules, fixtures
│
├── urugano/doctype/                # Frappe DocType definitions
│   ├── property/
│   ├── landlord/
│   ├── tenant/
│   ├── location/
│   ├── property_type/
│   ├── roommate_profile/
│   ├── amenity/
│   ├── amenity_item/
│   └── gallery/
│
├── templates/
│   ├── base.css                    # Design system (Tailwind theme + components)
│   ├── pages/
│   │   └── web.html                # Base layout (header, footer, scripts)
│   └── components/
│       ├── property_card.html      # property_card, property_card_compact macros
│       ├── roommate_card.html      # roommate_card macro (with built-in dialog)
│       ├── dialog.html             # dialog, dialog_trigger macros
│       └── amenity_icons.html      # property_amenities macro + field→icon map
│
├── www/                            # Web pages (route = directory path)
│   ├── my-home/                    # → /  (home page, via route rule)
│   ├── listings/                   # → /listings  and  /listings/detail/<name>
│   ├── roommates/                  # → /roommates  and  /roommates/apply
│   ├── login/                      # → /login
│   ├── logout/                     # → /logout
│   └── signup/                     # → /signup, /signup/guest_signup, /signup/landlord_signup
│
├── public/
│   ├── css/style.css               # Compiled Tailwind output (do not edit directly)
│   ├── img/                        # Legacy SVG icons (superseded by Lucide CDN)
│   └── js/csrf_setup.js            # CSRF token injection for fetch requests
│
└── fixtures/                       # Exportable seed data (synced via `bench migrate`)
```

---

## Getting Started

```bash
# Clone into frappe-bench apps folder
cd ~/frappe-bench
bench get-app urugano   # or: bench get-app https://github.com/…/urugano

# Install on a site
bench --site your-site.local install-app urugano

# Run migrations (creates tables, imports fixtures)
bench --site your-site.local migrate

# Start the dev server
bench start

# Rebuild CSS after editing base.css
bench build --app urugano
# or watch mode:
bench watch
```

---

## DocTypes

### Property
The core listing document. Fields relevant to templates:

| Field | Type | Notes |
|---|---|---|
| `title` | Data | Required |
| `property_type` | Link → Property Type | |
| `image` | Attach Image | Main photo |
| `location` | Link → Location | |
| `price` | Currency | Monthly rent in RWF |
| `landlord` | Link → Landlord | |
| `no_of_rooms` | Int | |
| `bathrooms` | Int | |
| `description` | Long Text | |
| `furnished` | Check | |
| `published` | Check | Controls web visibility |
| `featured` | Check | Appears on home page |
| `gallery` | Table → Gallery | Additional images |
| `amenities` | Table → Amenity Item | Legacy — prefer boolean fields |
| `wifi` … `house_cleaner` | Check (×20) | See [amenity map](#icons) |

### Landlord
| Field | Type |
|---|---|
| `name1` | Display name |
| `phone` | Phone number |
| `email` | Email |

### Roommate Profile
| Field | Notes |
|---|---|
| `name1` | Full name |
| `gender` | Male / Female / Other |
| `age` | Int |
| `preferred_location` | Text |
| `preferred_roommate` | Same gender / Any |
| `minimum_budget` | Currency (RWF) |
| `maximum_budget` | Currency (RWF) |
| `move_in_date` | Date |
| `additional_notes` | Long Text |

### Location
Stores `latitude` and `longitude` alongside a name — used for the Google Maps embed on the property detail page.

---

## Pages & Routing

Each page is a directory under `www/`. Frappe maps the directory path to the URL. A `index.py` provides context and `index.html` is the Jinja template.

| URL | Directory | Controller |
|---|---|---|
| `/` | `www/my-home/` | `my-home/index.py` |
| `/listings` | `www/listings/` | `listings/index.py` |
| `/listings/detail/<name>` | `www/listings/` | `listings/detail.py` |
| `/roommates` | `www/roommates/` | `roommates/index.py` |
| `/roommates/apply` | `www/roommates/apply/` | *(no py — static form)* |
| `/login` | `www/login/` | *(Frappe built-in)* |
| `/logout` | `www/logout/` | *(JS fetch to `/api/method/logout`)* |
| `/signup` | `www/signup/` | *(static)* |
| `/signup/guest_signup` | `www/signup/guest_signup/` | *(JS form)* |
| `/signup/landlord_signup` | `www/signup/landlord_signup/` | *(JS form)* |

Route rules (in `hooks.py`) handle the detail page slug and home alias:

```python
website_route_rules = [
    {"from_route": "/listings/detail/<docname>", "to_route": "listings/detail"},
    {"from_route": "/", "to_route": "home"},
]
```

---

## Python Controllers

Each `*.py` file exports a `get_context(context)` function. Attach variables to `context` to make them available in the template.

```python
# www/listings/detail.py
import frappe

def get_context(context):
    name = frappe.form_dict.docname          # from URL slug
    context.doc = frappe.get_doc("Property", name)
    context.landlord = frappe.get_doc("Landlord", context.doc.landlord)
    context.location = frappe.get_doc("Location", context.doc.location)
    context.properties = frappe.get_all("Property", fields=["*"])
    return context
```

In the template, use `{{ doc.title }}`, `{{ landlord.phone }}`, etc.

---

## API Endpoints

Endpoints are split across three files under `urugano/api/`:

```
urugano/api/
├── listings.py   → search_property_listings
├── roommates.py  → search_roommate_listings, apply_roommate
└── auth.py       → user_roles, create_guest_account, create_landlord_account
```

All functions are decorated with `@frappe.whitelist(allow_guest=True)` and accept **named parameters** — Frappe maps `frappe.call` args directly to them.

| Module | Function | Args |
|---|---|---|
| `listings` | `search_property_listings` | `location`, `property_type`, `max_price`, `furnished`, `number_of_rooms` |
| `roommates` | `search_roommate_listings` | `gender`, `location`, `min_budget`, `max_budget`, `move_in` |
| `roommates` | `apply_roommate` | `name`, `gender`, `location`, `age`, `roommate`, `min_budget`, `max_budget`, `move_in_date`, `notes` |
| `auth` | `user_roles` | *(none)* — returns `true` if current user has Landlord role |
| `auth` | `create_guest_account` | `email`, `first_name`, `last_name`, `password` |
| `auth` | `create_landlord_account` | `email`, `first_name`, `last_name`, `password` |

### Calling from the browser — use `frappe.call`

`frappe.call` is the standard Frappe client helper. It handles CSRF, serialisation, and surfaces server errors automatically. Always prefer it over raw `fetch` for whitelisted methods.

```js
// With async/await — destructure r.message directly
const { message: properties } = await frappe.call({
    method: 'urugano.api.listings.search_property_listings',
    args: { location: 'Kigali', max_price: '500000' }
});

// With callback
frappe.call({
    method: 'urugano.api.roommates.apply_roommate',
    args: { name: 'Alice', gender: 'Female', location: 'Remera', … },
    callback(r) {
        console.log(r.message);   // { status: 'success', name: 'RP-0001' }
    }
});
```

> The native `/api/method/login` endpoint (Frappe built-in) is called with `fetch` directly — it does not follow the whitelist convention.

### Adding a new endpoint

```python
# urugano/api/listings.py
@frappe.whitelist(allow_guest=True)
def my_endpoint(param_a=None, param_b=None):
    # frappe.call passes args as named parameters automatically
    return frappe.get_all("Property", filters={"location": param_a}, fields=["*"])
```

```js
const { message } = await frappe.call({
    method: 'urugano.api.listings.my_endpoint',
    args: { param_a: 'Kigali', param_b: 'value' }
});
```

---

## Template System

All pages extend the base layout:

```jinja
{% extends "urugano/templates/pages/web.html" %}
{% block title %}Page Title{% endblock %}

{% block page_content %}
  <!-- your HTML here -->
{% endblock %}

{% block js_content %}
<script>
  // page-specific JS
</script>
{% endblock %}
```

**`web.html`** provides:
- `<head>` with Inter font, compiled CSS, Lucide CDN, Alpine.js
- Fixed header with nav + auth dropdown (Alpine-powered)
- `<main>` wrapping `{% block page_content %}`
- Footer
- `lucide.createIcons()` call on `DOMContentLoaded`

---

## Reusable Components

Components are Jinja macros in `urugano/templates/components/`. Always import `with context` so macros can access `frappe.*`.

### property_card

```jinja
{% from "urugano/templates/components/property_card.html" import property_card, property_card_compact with context %}

{# Full card — for listing grids #}
{{ property_card(property) }}

{# Compact card — for sidebars (smaller image) #}
{{ property_card_compact(property) }}
```

Renders a linked card with image, badges, title, location, and price.

---

### roommate_card

```jinja
{% from "urugano/templates/components/roommate_card.html" import roommate_card with context %}
{{ roommate_card(roommate) }}
```

Renders an info card with a built-in **Contact** dialog. The dialog is unique per card (keyed on `roommate.name`).

---

### dialog

```jinja
{% from "urugano/templates/components/dialog.html" import dialog, dialog_trigger with context %}

{# Trigger — works anywhere on the page, no Alpine scope required #}
{{ dialog_trigger("my-dialog", "Open") }}
{{ dialog_trigger("my-dialog", "Open", class="btn-outline", type="button") }}

{# Dialog shell — use {% call %} to provide body content #}
{% call dialog("my-dialog", "Dialog Title") %}
  <p>Content here.</p>
  <div class="flex justify-end gap-3 mt-6">
    <button onclick="window.dispatchEvent(new CustomEvent('close-dialog', { detail: { id: 'my-dialog' } }))"
            class="btn-outline">Cancel</button>
    <button class="btn">Confirm</button>
  </div>
{% endcall %}
```

**Sizes:** `sm` / `md` (default) / `lg` / `xl` / `full`

**Open/close from JS:**
```js
window.dispatchEvent(new CustomEvent('open-dialog',  { detail: { id: 'my-dialog' } }))
window.dispatchEvent(new CustomEvent('close-dialog', { detail: { id: 'my-dialog' } }))
```

Pressing `Escape` or clicking the backdrop also closes the dialog.

---

### property_amenities

```jinja
{% from "urugano/templates/components/amenity_icons.html" import property_amenities with context %}
{{ property_amenities(doc) }}
```

Reads all 20 boolean amenity fields on the Property doc and renders a pill with a Lucide icon for each one that is checked. Renders nothing if none are set.

**Field → icon map** (defined in `amenity_icons.html`):

| Field | Icon |
|---|---|
| `furnished` | `sofa` |
| `wifi` | `wifi` |
| `air_conditioning` | `air-vent` |
| `tv` | `tv` |
| `microwave` | `microwave` |
| `washing_machine` | `washing-machine` |
| `refrigerator` | `refrigerator` |
| `gas_stove` | `flame` |
| `parking_space` | `square-parking` |
| `elevator` | `arrow-up-down` |
| `swimming_pool` | `waves-ladder` |
| `gym` | `dumbbell` |
| `balcony` | `fence` |
| `garden__yard` | `tree-pine` |
| `security_guard` | `shield-check` |
| `cctv` | `cctv` |
| `backup_generator` | `zap` |
| `solar_power` | `sun` |
| `pet_friendly` | `paw-print` |
| `house_cleaner` | `sparkles` |

---

## Design System

`urugano/templates/base.css` defines the entire design system as Tailwind v4 `@theme` tokens and `@layer components` classes. Edit this file, then run `bench build --app urugano`.

### CSS Custom Properties (brand colours)

```css
--color-brand         /* blue-600 — primary */
--color-brand-hover   /* blue-600 */
--color-brand-dark    /* blue-900 */
--color-brand-light   /* sky-100  — tinted backgrounds */
--color-brand-mid     /* blue-500 */
--color-success       /* green-300 */
--color-success-dark  /* green-700 */
--color-danger        /* red-500 */
--color-surface       /* white */
--color-surface-alt   /* gray-100 */
--color-border        /* gray-300 */
--color-muted         /* gray-500 */
```

Use as Tailwind utilities: `bg-brand`, `text-brand`, `border-brand-light`, etc.

### Component Classes

**Buttons**

| Class | Usage |
|---|---|
| `.btn` | Primary solid CTA |
| `.btn-outline` | Outlined secondary action |
| `.btn-ghost` | Low-emphasis (nav, dropdowns) |
| `.btn-sm` | Small primary |
| `.btn-danger` | Destructive action |

**Forms**

| Class | Usage |
|---|---|
| `.input` | Text input |
| `.select` | Select dropdown |
| `.textarea` | Multi-line input |
| `.label` | Field label |
| `.form-group` | Wrapper: `<div class="form-group"><label class="label">…</label><input class="input"></div>` |
| `.field-error` | Inline validation message |

**Cards**

| Class | Usage |
|---|---|
| `.card` | Base card shell |
| `.card-body` | Padded content area |
| `.card-hover` | Clickable card with hover lift |
| `.card-listing` | Property listing card |
| `.card-listing-body` | Listing card content area |

**Badges**

| Class | Usage |
|---|---|
| `.badge-primary` | Blue fill — "For Rent" |
| `.badge-secondary` | Light blue — property type, amenity chips |
| `.badge-muted` | Gray — neutral tags |
| `.badge-success` | Green — price, availability |
| `.badge-danger` | Red — urgent labels |

**Layout**

| Class | Usage |
|---|---|
| `.container-page` | `max-w-6xl mx-auto px-4` — use on every top-level section |
| `.section` | `py-12` vertical rhythm on white background |
| `.section-alt` | `py-12` on `bg-surface-alt` |
| `.section-title` | Section heading style |

---

## Icons

Icons are rendered via [Lucide](https://lucide.dev) loaded from CDN. `lucide.createIcons()` runs on `DOMContentLoaded` and converts all `<i data-lucide="…">` elements to inline SVGs.

```html
<i data-lucide="bed" class="w-5 h-5 text-brand"></i>
```

Because Lucide uses `stroke="currentColor"`, colour is controlled with Tailwind text utilities (`text-brand`, `text-muted`, etc.).

**Dynamic HTML** — if you inject HTML via JavaScript after page load, call `lucide.createIcons()` again:
```js
container.innerHTML = `<i data-lucide="star" class="w-4 h-4"></i>`;
lucide.createIcons();
```

**Alpine.js elements** — wrap `<i data-lucide>` in a container element when combining with `x-show`, so Alpine controls the wrapper and Lucide controls the icon:
```html
<span x-show="isOpen"><i data-lucide="x" class="w-5 h-5"></i></span>
```

Browse all available icons at [lucide.dev/icons](https://lucide.dev/icons).

---

## Adding a New Page

1. Create a directory under `www/`:
   ```
   urugano/www/my-page/
   ├── index.html
   └── index.py        # optional — only if you need server data
   ```

2. Write the controller:
   ```python
   # index.py
   import frappe

   def get_context(context):
       context.items = frappe.get_all("My DocType", fields=["*"])
       return context
   ```

3. Write the template:
   ```jinja
   {% extends "urugano/templates/pages/web.html" %}
   {% block title %}My Page — Urugano Realty{% endblock %}

   {% block page_content %}
   <section class="section">
       <div class="container-page">
           <h1 class="section-title">My Page</h1>
       </div>
   </section>
   {% endblock %}
   ```

4. The page is immediately available at `/my-page`. No registration needed.

---

## Adding a New API Endpoint

Add a function to `urugano/api.py`:

```python
@frappe.whitelist(allow_guest=True)     # remove allow_guest for auth-only endpoints
def my_endpoint():
    data = frappe.local.request.get_json()   # for POST
    # args = frappe.request.args             # for GET query params

    result = frappe.get_all("My DocType", filters={…}, fields=["*"])
    return result
```

Call from the browser:
```js
// GET
const res = await fetch('/api/method/urugano.api.my_endpoint?param=value');

// POST
const res = await fetch('/api/method/urugano.api.my_endpoint', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ key: 'value' }),
});
const { message } = await res.json();   // Frappe wraps return value in `message`
```
