# Boto Templates

Community-driven photo recipes for the [Boto Camera](https://github.com/varghese-ruben/BotoCamera) iOS app.

Every template is a small piece of JSON that tells Boto:
1. **How to set the camera at capture time** (exposure, white balance, focus, camera position…).
2. **How to grade the photo afterwards** (warmth, contrast, vignette, grain…).

The app fetches `manifest.json` from this repo at launch, caches it locally, and merges these recipes with the templates built into the app. Images are served via [jsDelivr](https://www.jsdelivr.com/), which is a free CDN in front of GitHub — fast and free.

---

## Submitting a new template

1. **Fork this repo.**
2. **Add your sample image** to `images/` (see [Image guidelines](#image-guidelines) below).
3. **Add an entry to `manifest.json`** under `templates: [...]` (see [Template schema](#template-schema)).
4. **Bump `manifestVersion`** at the top of `manifest.json` by one and set `updatedAt` to the current UTC time.
5. **Open a Pull Request.**

If your PR is merged, the Boto app will pick up the new template within an hour for every user, on next launch.

## Adding a new category

If your template doesn't fit any of the existing categories, add a new one:

1. Add an entry to `categories: [...]` in `manifest.json`.
2. Reference its `id` from your template's `category` field.

```jsonc
"categories": [
  {
    "id": "lo-fi",              // lowercase, dash-separated
    "displayName": "Lo-Fi",     // shown in the UI
    "tintHex": "#9B7B4A",       // accent color for the section
    "sortOrder": 200             // higher = further down the list
  }
]
```

## Image guidelines

- **Format:** `.jpg` (preferred) or `.png`.
- **Dimensions:** 1024×1024 square, or 4:3 / 3:2 landscape up to 1600px on the long edge.
- **File size:** under **300 KB**. Compress before committing — jsDelivr caches forever.
- **Path:** `images/tpl_<your_template_id>.jpg`.
- **Subject:** ideally a real photograph that *demonstrates the look* your template produces. Avoid screenshots or watermarks.

The app composes the final image URL as `baseImageURL + image`, so the example below resolves to:

```
https://cdn.jsdelivr.net/gh/varghese-ruben/boto-templates@main/images/tpl_cinematic_neon.jpg
```

## Template schema

```jsonc
{
  "id": "cinematic_neon",        // unique, lowercase, snake_case
  "version": 1,                   // bump when you change the template
  "category": "cinematic",        // category id (built-in or custom)
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

### Built-in category IDs

You can extend any of the categories built into the app by setting `"category"` to one of these:

| ID          | Display name |
|-------------|--------------|
| `selfie`    | Selfie       |
| `portraits` | Portraits    |
| `nature`    | Nature       |
| `product`   | Product      |
| `animals`   | Animals      |

## Updating an existing template

1. Edit its entry in `manifest.json`.
2. **Bump that template's `version`** by one — this forces the app to invalidate its cached sample image.
3. **Bump the top-level `manifestVersion`** by one.
4. Update `updatedAt`.
5. Open a PR.

## Safety rules the app enforces

Submissions go through a public review process, but the app also validates and clamps every numeric field before it touches the camera. Templates that fall outside these ranges are rejected silently:

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

## How releases reach users

There's no manual deploy — the app polls `manifest.json` from this repo through jsDelivr's CDN. Cache TTL on jsDelivr is ~12 hours for `@main`, so changes go live to all users within that window. For instant pushes, the app's Settings → "Refresh templates" forces a fresh fetch.

## License

The JSON in this repo is MIT licensed. Image submissions remain the copyright of their creators, who grant the Boto project a non-exclusive right to ship them as in-app sample artwork. By submitting a PR you confirm you have rights to the image you're contributing.
