# Manifest schema reference (schemaVersion 1)

This is the canonical reference for `manifest.json`. The Boto app implements **strict additive evolution**: fields can be *added* across schema versions, but never *renamed* or *removed* without bumping `schemaVersion`. Old apps reading a new manifest must safely ignore unknown fields.

## Top-level shape

```jsonc
{
  "schemaVersion": 1,
  "manifestVersion": <int>,        // monotonically increasing
  "updatedAt": "<ISO 8601 UTC>",   // e.g. "2026-06-09T12:34:56Z"
  "baseImageURL": "<absolute URL>",
  "categories": [<Category>, …],
  "templates":  [<Template>, …]
}
```

### `manifestVersion`

The app stores the version of the manifest it last successfully processed. On every launch, after fetching, it compares:

- **New > cached** → adopt the new manifest, refresh images whose `version` changed.
- **New == cached** → no-op.
- **New < cached** → ignored (probably a rollback in progress; the app keeps its current state).

You must bump this on every commit that changes the manifest.

### `baseImageURL`

Prepended to relative `image` paths in templates. Trailing slash required. Allows hosting changes (e.g. moving from jsDelivr to Cloudflare Pages) without touching every template.

If a template's `image` field starts with `http://` or `https://`, it's treated as absolute and `baseImageURL` is ignored for that one.

## Category

```jsonc
{
  "id": "<lowercase-snake-id>",
  "displayName": "<UI label>",
  "tintHex": "#RRGGBB",
  "sortOrder": <int>
}
```

| Field         | Required | Notes                                                            |
|---------------|----------|------------------------------------------------------------------|
| `id`          | yes      | Stable forever. Must match what templates reference.             |
| `displayName` | yes      | Shown in the Templates tab section header.                        |
| `tintHex`     | yes      | 6-digit hex, no alpha. Drives the section dot color.             |
| `sortOrder`   | no       | Lower = higher up. Built-in categories sit at `0…99`. Remote categories should use `100+`. |

### Built-in category IDs (always available)

| ID          | Sort order |
|-------------|------------|
| `selfie`    | 10         |
| `portraits` | 20         |
| `nature`    | 30         |
| `product`   | 40         |
| `animals`   | 50         |

A template may reference any built-in ID — you don't need to re-declare these in the `categories` array.

## Template

```jsonc
{
  "id": "<lowercase_snake_id>",
  "version": <int>,
  "category": "<category-id>",
  "name": "<UI label>",
  "hint": "<one-line tip, optional>",
  "image": "<URL or relative path>",
  "capture":    <Capture>,
  "processing": <Processing>
}
```

| Field      | Required | Notes                                                             |
|------------|----------|-------------------------------------------------------------------|
| `id`       | yes      | Unique across all templates ever. Never reuse a removed id.       |
| `version`  | yes      | Bump per template when you change anything. Forces image refetch. |
| `category` | yes      | Must match a built-in id or a `categories[].id` you define.       |
| `name`     | yes      | ≤ 30 chars recommended.                                           |
| `hint`     | no       | ≤ 120 chars. Shown under the template in CameraView.              |
| `image`    | yes      | Either absolute URL or relative to `baseImageURL`.                |

## Capture

Controls the camera at shutter time. Mirrors `CaptureSettings` in the app.

```jsonc
{
  "cameraPosition": "back",       // "back" | "front"
  "exposure":        <Exposure>,
  "whiteBalanceKelvin": 5200,     // null = auto WB; else 2000…8000
  "tint": 0,                      // -150…150 (green ↔ magenta)
  "focus":           <Focus>,
  "wantsDepth": false             // request depth-capable camera
}
```

### `Exposure`

Auto mode (let the camera meter, push by EV bias):

```jsonc
{ "type": "auto", "biasEV": 0.3 }
```

Manual mode (locked ISO + shutter):

```jsonc
{ "type": "manual", "iso": 800, "shutter": 0.001 }
```

`shutter` is in seconds. Helpful conversions: `1/1000s = 0.001`, `1/250s = 0.004`, `1s = 1.0`, `0.5` is half a second.

### `Focus`

Continuous autofocus (default for most templates):

```jsonc
{ "type": "continuousAuto" }
```

Locked focus (set lens position once and hold):

```jsonc
{ "type": "locked", "lensPosition": 0.6 }
```

`lensPosition` is `0` (near) to `1` (infinity). For macro use `0.0–0.1`. For landscape use `1.0`.

## Processing

Applied to the captured photo. Mirrors `ProcessingRecipe`.

```jsonc
{
  "warmth": 0,             // -1 (cooler) … +1 (warmer)
  "saturation": 1.0,       // 0 = B&W, 1 = neutral, 2 = very saturated
  "contrast": 1.0,         // 0.5 = flat, 1 = neutral, 1.5 = punchy
  "softenHighlights": 0,   // 0…1, darkens hot areas
  "shadowLift": 0,         // 0…1, opens up dark areas
  "clarity": 0,            // 0…1, midtone "bite" / perceived sharpness
  "depthBlurRadius": 0,    // 0 = off, 4…16 = simulated wide-aperture blur
  "vignette": 0,           // 0…1, edge darkening
  "grain": 0               // 0…1, monochromatic film grain
}
```

Notes:

- `depthBlurRadius > 0` requires `capture.wantsDepth: true`, otherwise the effect is skipped silently.
- `saturation < 0.05` triggers the app's "monochrome" rendering hint (used by the gallery card).
- Values outside the safety ranges in the README will be clamped — better to commit values that already sit inside the range.

## Versioning rules

- **`manifestVersion`** — bump on every commit. Treat as monotonic.
- **`template.version`** — bump when you change anything about a single template (settings, name, image, hint). The image bump is critical: the app uses `<id>_v<version>` as the local image cache filename, so without a version bump users won't pick up your new artwork.
- **`schemaVersion`** — bump only when an existing field is renamed or removed. Adding fields is safe within the same schema version.
