# Penfold new · the story

**Spine v21, 2026-09-16. Final.** v20 renumbered into the final hierarchy. Frozen copy: `story-v21.md`. Facts
from `kb-penfold.md` (§ numbers). Titles in [brackets] are working names. This is his script.

**Numbering:** the page top (P), Act 0, Act 1, Act 2 and the Closer (C) at the top; sections numbered inside
each act; bullets numbered inside each section. Every address names one item: 0.2.3.1 is Act 0, section 2,
bullet 3, sub-item 1.

**What changed from v20**
1. Renumbered into the hierarchy above
2. The sub-act sits inside Act 1 as section 1.3, right after the twist that leads into it
3. Cross-references follow the new addresses (0.1.4, 0.2.3.1)

---

# P · THE PAGE

## P1 · Header
P1.1. Metrics and role, the same shape as every project page

## P2 · Hero
P2.1. [working title] Five days at the bank, down to minutes

## P3 · Lede
P3.1. **The ambition:** an app where you create a pension instantly, instead of going to the bank over
   several days §15

## P4 · The outcome, up front
P4.1. From nothing to 3,000 savers and £4M in the bank, in 12 months §8

---

# ACT 0 · [making the thing]

**The act:** the grind. Ship something real in a week, read what the data says, and rebuild onboarding
around it.

## 0.1 · [the week]
0.1.1. I joined, learned pensions from the co-founders, audited their proof of concept, and turned it into a
   real product people could sign up for, with real customers in time for the funding round. All in 7 days
   §2, §5, §8, §15
0.1.2. **What shipped:** the proof of concept became a live product, open to the public, that took someone
   from signing up to owning a pension. It shipped in the shape the week allowed: 33 steps, no time to make
   it shorter §4, §5
   0.1.2.1. **The quote,** right after the 33 steps: "If I had more time, I would have written a shorter
   letter." Credit: after Blaise Pascal
0.1.3. **Result:** real people signed up and became customers, a dozen in week one, and the funding round
   closed on the back of a product that was live and onboarding §8
0.1.4. **Visual:** the 33-step live flow

## 0.2 · [leave and come back]
0.2.1. **What the funnel showed:** people didn't finish, because onboarding was linear. Every step lost a few
   people, and session IDs showed they came back and landed on step 1. The CTO ran the funnel daily, drops
   went to stand-up, and I watched those sessions and rage clicks in FullStory §3, §5, §14, §15
0.2.2. **The insight** (make this stand out on the page): the account was the pension, so a returning user
   started from zero §3, §15
0.2.3. **Three fixes:**
   0.2.3.1. **Account and pension, decoupled:** account first (email and password), progress saved, the rest
   finished later, then a pot created or imported §15
   0.2.3.2. **Onboarding, modular:** five modules (three, then a fourth with an extra) that survive leaving,
   built from existing pieces to avoid breaking code §4, §5, §6, §15
   0.2.3.3. **Mobile, for a desktop-only product:** one component set for both platforms, mobile feeding
   desktop. Built once instead of twice: engineering load halved, shipping daily. A prioritization call,
   made knowingly: a few screens below my own bar, because shipping mattered more than polish §4, §5, §6, §8
0.2.4. **Result:** people who quit could come back and finish
0.2.5. **Visual:** a returning user landing on step 1, then the progress card at 25% complete, which shows
   the state was saved §7
0.2.6. **Visual callback:** the 33-step strip from 0.1.4 collapses into the five modules

## 0.3 · The twist that ends Act 0
0.3.1. It improved. And a pension still took five days to exist.

---

# ACT 1 · [the click]

**The act:** the first big lever. I cracked the instant pension.

## 1.1 · [a pension, instantly]
1.1.1. **Where the days went, and what I tried first** (text only): Gaudi and Seccl worked by hand, each step
   waiting up to 24, 48 or 72 hours on the previous one's ID, and legally the pension existed only once the
   last one came back. The constraints were technical, and I felt they could be worked around. Calling it
   a "pot" broke on the first top-up, because the money had nowhere legal to go. The partners couldn't be
   sped up §15
1.1.2. **The click:** the IDs always came back, with zero failures, and engineering confirmed a wrong
   reference gets flagged and replaced on the same record. So: provisional references, with the real user
   details, sent to every partner at once as soon as the information module was done. A ledger replaced
   each one as the real reference arrived §15
1.1.3. **Result:** a pension the moment onboarding ended, every reference reconciled within the week, zero
   failures. The act lands: five days, to instant §15
1.1.4. **Visual:** the partner sequence before and after, and the end of onboarding, from "Hold on while we
   run some checks" to a pension that exists §5, §15

## 1.2 · The twist
1.2.1. Onboarding worked, the app did the job, and pensions were instant. And still there was no flood. 100
   signups a month §5, §8

## 1.3 · Sub-act · [closer to the users]

**The sub-act:** the grind before the flip. So we started looking. A craft beat: small moves, the machine,
and Joe T.

1.3.1. I dove deeper into the user base: FullStory, the funnel, Customer Support, a beta program §5, §13
1.3.2. **Interlude, the machine** (a centered text block, a break in the page's flow, introducing an idea of
   its own):
   1.3.2.1. **The loop:** every Friday, Customer Support and I went through the week's top tickets. Support
   was the gold mine §5, §13
   1.3.2.2. **The beta program:** recruited from sessions and tickets, with one beta user in the Friday chat
   each week §5
1.3.3. **"What if I die?":** Joe T.'s joke on a Friday chat. None of my flows had considered death, and the
   real process was a manual email carrying four data points §3, §13
1.3.4. **Shipped in a day:** one screen, three inputs plus the name already on file, a one-line spec, on
   Tech-Debt-Friday, because every component already existed. I called Joe back: "Thanks to your
   suggestion, everyone can now nominate a beneficiary. Cheers!" Trust added, manual nominations gone for
   Customer Support, and proof of a mature system and a solid team §6, §8, §11, §13
1.3.5. **Closing line:** Joe T. was happy. We weren't §13

---

# ACT 2 · [the flip]

**The act:** we flipped who we sold to, and there they were. Then it was handling the rush and doubling
down on what was working.

## 2.1 · [the flip]
2.1.1. **The problem:** we were selling to the wrong people. People without a pension didn't feel they
   needed one §1, §3, §15
2.1.2. **My call, proposed in a meeting:** sell to people who already have pensions, the pots scattered
   across past employers §6, §15
2.1.3. **The change:** the message, and the Facebook targeting and spend. Around November and December
   2019 §15
2.1.4. **The website and the ads, a quick pass:** a visual crutch for the change, carrying little of the
   story. My work, outside my discipline. October and November 2019 led with "The bad news: You may already
   be losing up to £228.95 daily"; by 9 December it led with "Find and combine" §15
2.1.5. **It worked, and Combine became the flagship** §8
2.1.6. **Combine, the callback to 0.2.3.1:** already built, since import had been there from the start at
   MVP stage, one of the three main actions on the dashboard, with "Find my other pensions" from the beta.
   Now it paid off, and I made it a bigger priority: the Combine form evolved, and transaction history
   v0+n added notifications for Combine events §15
2.1.7. **Visual:** the pot import. One Combine screen, then the Combine notification, the most colorful of
   each: the page's eye candy §7
2.1.8. **Transaction history, designed backwards:** v0, then v0+n built up like Lego, then Final, where a
   combined pot lands. It shows things happening §5, §13

---

# C · CLOSER

## C1 · [my results]
C1.1. Signups from 100 to 600 a month, each arriving with a pot. Signup value rose with volume, and
   acquisition costs fell §6, §8, §14
C1.2. **Year one:** a dozen users in week one grew to 3,000 savers and £4M under management, on plan §8

## C2 · [present day]
C2.1. The foundation held. Penfold now manages over £1B and was voted Best Pension 2026 §12
