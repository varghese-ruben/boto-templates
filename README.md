# Boto Templates

Remote photo recipes for the [Boto Camera](https://github.com/varghese-ruben/BotoCamera) iOS app.

This repository is the **first-party content delivery channel** for Boto Camera. The app fetches `manifest.json` from this repo at launch (via [jsDelivr](https://www.jsdelivr.com/)), caches it locally, and merges these recipes with the templates built into the app binary. Everything here ships authored, reviewed, and maintained by the Boto Camera developer — there is no public submission process, no third-party content, and no user-generated content surfaced through this manifest.

If you've found this repo because you're curious how Boto's remote catalog works, read on. If you're hoping to submit a template, this isn't open to public contributions today.

---

## Why deliver templates remotely?

Bundling every template into the app would mean a full App Store update each time a recipe is tweaked or a new look is added. By serving templates from this repo, the app can:

- Pick up new looks without forcing users to update.
- Iterate on a recipe (warmth, contrast, grain, etc.) and ship the fix the same day.
- Keep the app binary small by streaming sample images on demand.

The remote catalog is **additive**: every template in the app is also bundled in some form, so the app remains fully usable offline using the built-in catalog.

---

## What lives in this repo

```
manifest.json     # the catalog the app reads
images/           # sample images referenced by each template
```

Every template is a small piece of JSON that tells Boto:

1. **How to set the camera at capture time** (exposure, white balance, focus, camera position…).
2. **How to grade the photo afterwards** (warmth, contrast, vignette, grain…).

See [Template schema](#template-schema) below for the wire format.

---

## How releases reach users

There's no manual deploy step — the app polls `manifest.json` from this repo through jsDelivr's CDN. Cache TTL on jsDelivr is ~12 hours for `@main`, so changes go live to all users within that window. For instant pushes, the app's **Settings → "Refresh templates"** forces a fresh fetch.

The app never uploads anything to this repo. The data flow is one-way: GitHub → jsDelivr → app cache → user.

---

## Template schema

```jsonc
{
  "id": "cinematic_neon",        // unique, lowercase, snake_case
  "version": 1,                   // bump when the template changes
  "category": "cinematic",        // category id (built-in or declared in this manifest)
  "name": "Neon Cinematic",       // shown on the card
  "hint": "Tungsten city signs…", // one-line shooting tip, optional
  "image": "images/tpl_cinematic_neon.jpg",

  "capture": {
    "cameraPosition": "back",     // "back" | "front"
    "exposure": {
      "type": "auto",             // "auto" | "manual"
      "biasEV": 0.0               //   auto: bias EV stops (-2…+2)
      // "iso": 800,               //   manual: ISO 50…3200
      // "shutter": 0.001          //   manual: seconds (1/1000 = 0.001)
    },
    "whiteBalanceKelvin": 3200,   // null for auto WB, otherwise 2000…8000
    "tint": 0,                    // -150…+150, green/magenta
    "focus": {
      "type": "continuousAuto"    // "continuousAuto" | "locked"
      // "lensPosition": 0.6       //   locked: 0=near … 1=infinity
    },
    "wantsDepth": false           // true if the look needs a depth-capable camera
  },

  "processing": {
    "warmth": 0,                  // -1…+1, color temperature push
    "saturation": 1.0,            // 0=B&W, 1=neutral, 2=very saturated
    "contrast": 1.0,              // 0.5=flat, 1=neutral, 1.5=punchy
    "softenHighlights": 0,        // 0…1, darkens hot highlights
    "shadowLift": 0,              // 0…1, opens up dark areas
    "clarity": 0,                 // 0…1, midtone "bite"
    "depthBlurRadius": 0,         // 0=off, 4…16 = simulated wide aperture
    "vignette": 0,                // 0…1, edge darkening
    "grain": 0                    // 0…1, monochromatic film grain
  }
}
```

### Categories

A template references a category by `id`. The app ships with these built-in categories:

| ID          | Display name |
|-------------|--------------|
| `selfie`    | Selfie       |
| `portraits` | Portraits    |
| `nature`    | Nature       |
| `product`   | Product      |
| `animals`   | Animals      |

New categories can be declared in `manifest.json` under `categories: [...]`:

```jsonc
"categories": [
  {
    "id": "lo-fi",
    "displayName": "Lo-Fi",
    "tintHex": "#9B7B4A",
    "sortOrder": 200
  }
]
```

---

## Image guidelines

- **Format:** `.jpg` (preferred) or `.png`.
- **Dimensions:** 1024×1024 square, or 4:3 / 3:2 landscape up to 1600px on the long edge.
- **File size:** under **300 KB**. jsDelivr caches forever, so commit the compressed file.
- **Path:** `images/tpl_<template_id>.jpg`.
- **Rights:** every sample image in this repo is original photography by the Boto Camera developer.

The app composes the final image URL as `baseImageURL + image`, so the example below resolves to:

```
https://cdn.jsdelivr.net/gh/varghese-ruben/boto-templates@main/images/tpl_cinematic_neon.jpg
```

---

## Updating an existing template

1. Edit its entry in `manifest.json`.
2. **Bump that template's `version`** by one — this forces the app to invalidate its cached sample image.
3. **Bump the top-level `manifestVersion`** by one.
4. Update `updatedAt` to the current UTC time.
5. Commit to `main` — jsDelivr will pick it up within the cache TTL.

## Adding a new template

1. Add the sample image to `images/` per [Image guidelines](#image-guidelines).
2. Append a new entry to `templates: [...]` in `manifest.json` per [Template schema](#template-schema).
3. Bump `manifestVersion` and update `updatedAt`.
4. Commit to `main`.

---

## Safety rules the app enforces

The app validates and clamps every numeric field before it touches the camera. Values that fall outside these ranges are clamped silently (not rejected), so a typo in this repo degrades gracefully rather than crashing the app:

| Field                 | Allowed range |
|-----------------------|---------------|
| `biasEV`              | `-3.0 … +3.0` |
| `iso` (manual)        | `25 … 12800`  |
| `shutter` (manual)    | `0.00025 … 30` (1/4000 s … 30 s) |
| `whiteBalanceKelvin`  | `2000 … 8000` (or `null` for auto) |
| `tint`                | `-150 … +150` |
| `lensPosition`        | `0 … 1`       |
| `warmth`              | `-1 … +1`     |
| `saturation`          | `0 … 2`       |
| `contrast`            | `0.5 … 2.0`   |
| `softenHighlights`, `shadowLift`, `clarity`, `vignette`, `grain` | `0 … 1` |
| `depthBlurRadius`     | `0 … 20`      |

Image URLs are also restricted to HTTPS — plain `http://` references in the manifest are dropped.

---

## Contributions

This repository is **not open to public template submissions** at this time. All templates are authored by the Boto Camera developer. Issues and pull requests targeting documentation fixes or bug reports are welcome; PRs proposing new templates or sample images will be closed.

If you'd like to suggest a look you'd love to see in the app, open an issue describing the scene, the mood, and the kind of light it works in.

---

## License

The JSON in this repo is MIT licensed. Sample images in `images/` are copyright their photographer (the Boto Camera developer) and are licensed for use only as in-app sample artwork within Boto Camera.
