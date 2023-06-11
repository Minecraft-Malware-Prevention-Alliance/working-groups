# Public Identity Infrastructure

## Steps

- [ ] Find and agree on trust roots (Trust roots should be major stakeholders in the minecraft modded ecosystem)
- [ ] Establish guidelines on what is needed to consider an identity verified
- [ ] Write up a specification on how this infrastructure will work

## Current orginizations who have stepped up to be a trust root

- Modrinth
- GDLauncher

## Root Key Problem

We need preferably [HSMs](https://en.wikipedia.org/wiki/Hardware_security_module) for people who are operating a trust root, this increases the security of
the root key which if compromised, can cause a massive disaster.

## Trust Roots

Orginizations who have been decided to be a trust root should always be independent and if possible we should have atleast 4 trust roots.
This is to avoid a monopoly on who can issue keys. 

Its important for the trust roots to have a history of good security, and properly responding to security reports on-time.