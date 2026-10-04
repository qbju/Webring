# ~ring

> A small web ring for independent websites.

~ring connects personal sites and small web projects into one ring.

## Join ~ring

### 1. Add the ring link

Add this to a page on your site:

```html
<a href="https://github.com/qbju/Webring" data-webring="~ring">~ring</a>
```

The link must be present on the actual site before you submit your application.

### 2. Open an application

Open a **Join ~ring** issue and fill in every field in the template.

Your application must:

- use a valid HTTP(S) site URL;
- point to a publicly reachable site;
- have the ~ring marker installed;
- follow the issue template;
- be submitted from a GitHub account with fewer than 3 existing ~ring registrations.

Applications are checked automatically by GitHub Actions.

### 3. Wait for verification

The bot checks:

1. the application format;
2. your GitHub account's existing registrations;
3. whether the submitted URL is reachable;
4. whether the ~ring marker is actually present.

If everything passes, your site is added to `members.json`.

## Participant template

You can copy this section when adding ~ring to your own site's README:

```md
## ~ring

This site is part of [~ring](https://github.com/qbju/Webring), a web ring connecting independent websites.

<a href="https://github.com/qbju/Webring" data-webring="~ring">~ring</a>
```

## GitHub Pages

The public ~ring website is published separately from the registry and automation.

The Pages site reads `members.json` and can provide navigation between registered sites.

## Monitoring

Registered sites are checked automatically every 6 hours.

A site that fails 3 consecutive checks is marked `inactive`. If a later check succeeds, it is restored to `active`.

## Registry

The current member registry is:

- `members.json` — machine-readable list of registered sites.

## License

See the repository license.
