# 1912 Open ONI title-calendar route resolution

Date: 8 September 2026  
Status: **METHOD RESOLVED / CURRENT INTERFACE ACCESS GAP**

Purpose: resolve the title-specific annual calendar URL mechanism needed for exhaustive 1912 newspaper issue inventories.

## Route mechanism resolved

The Open ONI calendar plugin source defines the title-specific year route as:

`^lccn/(?P<lccn>\w+)/issues/(?P<year>\d{4})$`

Therefore the intended annual title-calendar routes are:

- *Morning Enterprise* (`sn00063701`):
  `https://oregonnews.uoregon.edu/lccn/sn00063701/issues/1912`
- *Oregon City Enterprise* (`sn00063700`):
  `https://oregonnews.uoregon.edu/lccn/sn00063700/issues/1912`

Open ONI source reference:
- https://github.com/open-oni/plugin_calendar/blob/main/urls.py

This supersedes the earlier uncertainty about whether the year selector used a query parameter, POST form, or another hidden calendar mechanism.

## Current interface limitation

The current research web layer successfully opens the title's default `/issues/` calendar but rejects manually constructed annual URLs unless they have already appeared as an allowed navigable URL in the research session. Search indexing does not currently surface the exact `/issues/1912` pages.

Accordingly:

- the **route itself is resolved**;
- the 1912 title calendars are **not yet retrieved/certified through this interface**;
- do not infer issue survival from the theoretical daily/weekly publication schedule;
- continue building issue controls from actual dated archive pages and previous/next linkage;
- the exact annual calendar URLs are now a precise manual/browser route if the current tool layer remains unable to follow them.

## Research consequence

This is a methodology/access record only. It creates no new historical `E-###` or `S-###` claim and no year-status promotion.

## Next actions

1. Retry the exact annual routes in a browser/manual path that permits direct URL entry.
2. If retrieved, reconcile the annual calendar's actual surviving dates against the issue ledger already built from individual archive pages.
3. Continue issue-specific page/image counts and scan-level review independently; a calendar date proves an archived issue exists, not that every page has been visually reviewed.
4. Preserve any discrepancy between calendar issue dates, issue sequence links, and page masthead dates as an archive-quality flag rather than normalizing it away.
