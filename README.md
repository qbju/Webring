# ~ring

A simple GitHub Actions-powered web ring.

Sites join by opening an Issue. Actions validate the application, verify that the ring marker is installed on the submitted site, and add approved sites to members.json.

## Joining

Open a Join ~ring issue and fill in the template.

The submitted site must:
- use a valid HTTP(S) URL;
- actually serve the site;
- contain the ~ring verification marker;
- follow the issue template;
- have fewer than 3 existing registrations by the same GitHub account.

## Ring marker

Put this HTML on the site:

    <a href="https://github.com/qbju/Webring" data-webring="~ring">~ring</a>

## Monitoring

Every 6 hours, GitHub Actions checks every registered site. Three consecutive failed checks change the member status to inactive; one successful check restores it.

## Data

members.json is the registry consumed by ring clients.
