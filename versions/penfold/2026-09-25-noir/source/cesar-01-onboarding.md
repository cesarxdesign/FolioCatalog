# Section 01, onboarding: Cesar's account, 2026-09-25 (verbatim)

33 steps was costing us. About 80% of all traffic driven by the website was lost at some point in the flow. Which imapcted our cost of acquisition, and overall growth rate. Two very important metrics in general, but specifically to our vigilant investors. Which was expected, so really, I began working on a revised onboarding, even before it got shipped.

The first issue was lack of a mobile version. A trade off I recomended since we didn't have the resources to make an app, and would be webbased for the foreseeable future: ship desktop first, it'll get us the milestones needed for the funding, and it'll look less weird for users having a pension site work on desktop but not mobile, rather than working on mobile, but not desktop. That'd risk looking like a scam or less serious startup, and my experience told me when it comes to money, trust is king.

The second issue was a bit trickier, and one I didn't fully antecipate (in the 7 days I had to work on it) which actually meant a bit of early tech debt, regarding our information arquitechture. The 33 step linear flow, created an account at the end of onboarding, which was marked by the creation of a pension. But linear was bad, and we had to make the flow modular, so that users could come back and finish it later, rather than simply dropping off, and either having to start over, or what the data showed was way more common: giving up completely. So I had to work with our engineering team of one, to decouple pension and account, and creating an account on just email and password. then we could have a modular onboarding with completion, and checks that would decide when to trigger a pension.

this plugged two huge holes in our funnel [check if this is technically correct, could lack of mobile be a "hole in the funnel"?]. but, came with costs as our engineering team of one now had to maintain twice the design.components

## Supersedes, on the page

- "those who quit did come back later, only to start again from step one": giving up completely was far more common than starting over.
- "an empty pension inside it, opened first": the account opened on email and password; checks decided when to trigger the pension.
