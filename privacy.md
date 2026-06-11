# Privacy Policy

_Last updated: 11 June 2026_

Boto Camera ("Boto", "the app", "we") is built and operated by an independent developer. This Privacy Policy explains, in plain language, what information the app touches and what we do with it.

The short version: **we collect nothing.** Boto stores your photos and preferences on your device only, and never sends any information about you to us or to a third party.

## What Boto accesses on your device

Boto only requests the iOS permissions that are strictly necessary for the features you use:

- **Camera.** Required to compose and capture photos with the active template's exposure, focus, and color settings applied live. Boto does not access the camera in the background and never records video or audio.
- **Photo Library (Add Only).** Optional. When you grant this, captured photos are also saved to your iOS Photos library so you can share them or keep them alongside your other shots. Boto cannot read or modify photos already in your library — only add new ones it has just captured. You can revoke this access at any time in iOS Settings.

## What Boto collects from you

**Nothing.** Boto does not have user accounts, does not collect, transmit, share, or sell any personal information, and does not maintain a server-side database of users.

We do not use any analytics SDKs, advertising SDKs, crash reporters, or any third-party tracking libraries.

## What stays on your device

Everything Boto creates is stored locally on your iPhone:

- Captured photos (originals and processed versions) live in the app's private Documents folder. They are also added to your iOS Photos library if you granted that permission.
- Templates you create yourself are saved as a JSON file in the app's private Documents folder.
- Two app preferences ("Save originals", "Show grid") are stored in standard iOS user defaults.
- A list of announcement message identifiers you've dismissed is stored in iOS user defaults so the same message doesn't reappear after you've closed it.

None of this is transmitted off your device. Uninstalling Boto removes all of it.

## Network requests Boto makes

Boto makes outbound HTTPS requests to a public content delivery network (CDN) — currently `cdn.jsdelivr.net` — to fetch two things:

1. A **public template catalog** (`manifest.json`) that lists available photo templates. This file is the same for every user.
2. **Template sample images** referenced by the catalog. These are JPG/PNG files cached locally so they don't need to be re-downloaded.
3. (Occasionally) an **optional announcement image** if a publisher announcement is active.

These requests carry no identifiers, no query parameters about you, no request body, and no custom headers. The CDN sees the IP address that is inherent in any HTTP request — Boto does not log, retain, link, or otherwise use this. The CDN's own data practices are governed by its operator (jsDelivr); refer to their privacy policy for details.

We do not provide any way for a remote announcement to track who saw or dismissed it.

## Children

Boto is not directed at children under 13 and does not knowingly collect data from anyone. The app's features are general-purpose photo capture.

## Third parties

We do not share, sell, or license any data to third parties — because we don't have any data about you in the first place.

## Changes to this policy

If we ever change how Boto works in a way that affects this policy, we will update this page and the "Last updated" date above. Material changes will also be surfaced in-app via the announcement system.

## Contact

Questions, concerns, or requests related to this policy: Raise a request [here.](https://forms.gle/huZt7ssiDjeF3QoB7)

We do our best to respond within a few business days.
