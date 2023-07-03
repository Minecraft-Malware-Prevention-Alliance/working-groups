# Simplified Signatures and Identity

> **Note**
> For full transparency, I am a maintainer for Prism Launcher. However, this proposal is not on the behalf of Prism, nor reflects the opinions of my fellow maintainers. These ideas are solely my own

## Problems with the current implementation

- Giving root trust to many organizations increases the risk of compromisation and misuse of keys

  - As said in the current spec, a root key being compromised would be a "massive disaster." By giving so many different groups an equally trusted key, the chances of one being compromised increases drastically.

- Required infrascture may create a roadblock as other "major stakeholders" come up

  - Recommendations for trust roots such as HSMs, as well as the possibility of needing to run infracture for things such as proper OSCP and timestamping could also be a major problem. Many projects - especially FOSS projects which usually receive less funding than say, a coporation - could have difficulties in supporting said infrastructure. This could in turn lead to less "major stakeholders" being able to particpate.

- Proper review of mods should not be dependent on groups who are not active in or have expereience with reviewing and distributing mods

  - I think this may be the biggest issue here. Though not stated, I can assume that as each trust root would have a valid key to sign mods with, they would have the responsibility to both review and sign some mods.
  - "Major stakeholders" for example includes launchers, which frankly have little to do with how mods are primarily distributed, as that is handled by services such as Curseforge and Modrinth.
  - Many projects already have issues with continuous contributions (there have been many examples of this recently, some discussed very publicly)
    - This could lead to inactive keys where mods are rarely reviewed or signed, making their trust virtually a security risk
    - Note: I am not trying to undermine work contributors do. I just don't see a future where many projects will have the capacity to review mods at the same scale as services such as Modrinth and Curseforge.

- The system is overly complicated

  - Having multiple trust roots, each one managing their own infrastructure and having their own signatures would be a mess to explain to a lot of mod developers, especially newer ones
  - To me, this feels more like PGP than an actual root of trust (especially with how we need to verify each root trust as is)...and we all know how well understanding PGP goes for most people. I think [this](https://latacora.micro.blog/2019/07/16/the-pgp-problem.html) blog post can give a good summary of on some issues with the complexity of Web of Trust models.

- Too much control is vested in this organization
  - Signatures are meant to prove something came from a specific person. There is no reason as to why mod developers should need to get a key from third parties to be able to show to users that their mod came from them.

## Proposed Solutions

- Mod platforms continue to be the ones reviewing and approving of mods

  - This has already been going on for years now; and as I said before, I don't think spreading this responsibility out to organizations without experience is a good idea.
  - This would reduce the attack surface of the group by lowering the amount of keys
  - Mod platforms can manage their own individual signing infrastructure, easily allowing for alternatives to come up without worrying about becoming a "major stakeholder" to be able to provide users with a way to confirm uploaded mods came from their authors

- [Minisign](https://jedisct1.github.io/minisign/)
  - Minisign (and similar software, I am only using minisgn as an example here) can provide simple signatures for mods, allowing for a much more streamlined explanation of the model (which could convince more mod developers to actually implement this)
  - If paired with my previous solution, this could allow for mod distributors to allow **developers** (I think this is important here as developers should be in full control of verifying the authenticiy of _their_ mods, not a third party) to upload public keys, which are then used server side to verify uploaded content as from the author
  - This would further push the point that signatures are not meant to be a sign of safety, but rather that they came from the mod creator.
  - A similar model to this would be GitHub's commit signature integration.

## Drawbacks of this proposal

- Mods would be going unreviewed when signed

  - If we want signatures to also mean "this mod is safe," then this is a major issue. However, as said before, I think this is completely out of scope for signatures and could easily be taken advantage of - especially with trust roots that have less thorough reviewing policies (this would most likely happen in the current proposal, also mentioned before)

- More trust would be placed into Modrinth/Curseforge
  - I like the idea of having a community entity, one with both coporations and community projects. However, given that this is limited to mod signing, I don't see why this is very applicable here. Modrinth and Curseforge are already trusted enough to be the primary distributor of mods that a vast majority of users use, and have been for a long time. I don't think it would be much further to allow them to verify the signatures of developers
