# ~ring

> A small web ring for independent websites.

~ring connects personal sites and small web projects into one ring.

Public site: https://tildering.pages.dev/

## Join ~ring

### 1. Add the ring widget

Add this to a page on your site:

```html
<nav id="~ring"></nav>
<script src="https://tildering.pages.dev/widget.js" data-webring="~ring"></script>
```

The default widget provides **Prev / Random / Next** navigation between active ~ring members.

### Widget styles

You can choose a different navigation style with `data-webring-style`:

```html
<!-- Default: ← Prev · Random · Next → -->
<script src="https://tildering.pages.dev/widget.js" data-webring="~ring" data-webring-style="text"></script>

<!-- Button style -->
<script src="https://tildering.pages.dev/widget.js" data-webring="~ring" data-webring-style="buttons"></script>

<!-- Vertical style -->
<script src="https://tildering.pages.dev/widget.js" data-webring="~ring" data-webring-style="stacked"></script>
```

You can also show the official ~ring logo above the navigation:

```html
<script src="https://tildering.pages.dev/widget.js"
  data-webring="~ring"
  data-webring-style="buttons"
  data-webring-logo="true"></script>
```

Available styles are `text`, `buttons`, and `stacked`. The logo option is independent, so it can be combined with any style.

### 2. Open an application

Open a **Join ~ring** issue and fill in every field in the template.

Your application must:

- use a valid HTTP(S) site URL;
- point to a publicly reachable site;
- have the ~ring widget marker installed;
- follow the issue template;
- be submitted from a GitHub account with fewer than 3 existing ~ring registrations.

Applications are checked automatically by GitHub Actions.

### 3. Wait for verification

The bot checks:

1. the application format;
2. your GitHub account's existing registrations;
3. whether the submitted URL is reachable;
4. whether the ~ring marker is actually present.

If everything passes, your site is added to both `members.json` and the public `docs/members.json`.

## Participant template

You can copy this section when adding ~ring to your own site's README:

```md
## ~ring

This site is part of [~ring](https://tildering.pages.dev/), a web ring connecting independent websites.

<nav id="~ring"></nav>
<script src="https://tildering.pages.dev/widget.js" data-webring="~ring"></script>
```

## Cloudflare Pages

The public ~ring website is deployed at https://tildering.pages.dev/.

The Pages site serves the public registry and `widget.js`. GitHub Actions keeps `docs/members.json` synchronized with the source registry.

## Monitoring

Registered sites are checked automatically every 6 hours.

A site that fails 3 consecutive checks is marked `inactive`. If a later check succeeds, it is restored to `active`.

## Registry

The current member registry is:

- `members.json` — source-of-truth registry used by automation.
- `docs/members.json` — public registry served by Cloudflare Pages.

## License

See the repository license.
