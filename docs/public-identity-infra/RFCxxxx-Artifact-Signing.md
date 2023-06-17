The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

-----

# Rationale
Signatures are a powerful tool, as they cryptographically allow associating an artifact to an identity, and ensure that it has not been tampered with.

Existing solutions, used on the Web, and for desktop application signing, have proved their efficiency, but are either too expensive, or not adapted to our usage.

This specification introduces the basis of a root of trust for the minecraft community, making it easier for anyone to distribute signed artifacts.

## Glossary
- **Certificate**: An electronic document, binding a key pair to an identity
- **CA** (or Certificate Authority): An organization that acts to validate identities, and bind them to cryptographic key pairs using **digital certificates**
- **TR** (or Trust root): An organization responsible for one of the **root certificates**
- **Artifact**: A final binary or file resulting from the development process. In our case, this would be modpacks or 
## Overview

## Section 1: Trust Roots

Trust roots, the top certificates of the chain, are held by trusted and known organizations.
The list of trust roots **SHALL** be kept in a public place, and clients are **RECOMMENDED** to trust the entirety of the trust roots. An exception **SHALL** be made in the event where a trust root cannot be trusted, at their discretion.

Trust roots all have root certificates (certificate without parents), that **MUST** be kept offline, in a secure location.

Their use is limited to the creation of intermediary certificates, used for the day-to-day operations, as they have a more limited blast radius, and lower lifetimes.

Intermediary certificates are **RECOMMENDED**[^1] to use a Trusted Platform Module, or a Hardware Security Module, so that the keys are protected from theft.

## Section 2: Certificate Authorities
To sign artifacts, a modder needs a certificate.
To prevent malware creators getting a code signing certificate, there needs to be some validation, to confirm the identity of the certificate seeker. A CA **MAY**, as of its discretion, choose a method of validation, as long as they match the following requirements:
- A validation option without IRL identity validation **MUST** be offered.
- Certificate issue **SHALL** be done with human verification on the CA side, except when the requirements to get a certificate already require human verification (like a validated identity somewhere else, or a contract signature)
- Certificate renewals & certificate re-issuing **SHALL** be subject to higher standards of validation, to protect as much as possible against supply chain issues.
- CAs **SHALL** offer a standardized API to check the certificate history for a given username / provider combo. The details of this API are out of scope for this document.
- CAs **SHALL** offer a standardized API/procedure to start a certificate request using a CSR and to get the certificate once issued. The rest of the certificate flow is left as an implementation detail for the CAs to implement.
- CAs **MUST** implement both CRL[^2] and OCSP[^3] to manage revocation of compromised certificates.

## Section 3: Modder integrations
After getting a certificate, artifacts that are built have to be signed. 

To help with that, here are some guidelines for build tools implementers[^4] :
- Use the provided trust root list, and embed it inside builds.
- Use the maximum number of available CAs
- Use the provided APIs for starting a certificate application
- Generate the key pair securely
	- Delegate the key generation to a known library (openssl for example)
	- Store the key securely, with support for the TPM where applicable, or with a password.
	- Try to educate the users about the need to protect their key as best as possible
		- Some documentation will be written for modders, to help with it.

## Section 4: Loaders & Launchers (User-facing applications)
Once an artifact is signed, the user must have protection against supply chain attacks, and signed malware, while not compromising on usability of applications.

Here are some guidelines for loaders & launchers[^4] :
- Use the provided trust root list, and embed it inside builds.
- Make use of OCSP[^3] where possible, or use CRLs.
- Try to use field-tested libraries and solutions to improve security.
- In case a signature is invalid, show a detailed error message, and refuse to launch
- In case a mod is not signed, show a warning, but leave launch possible if the user agrees to (using any method wanted).
- For applications that show lists of mods, encourage signing by putting visual indicators that the mods are signed, and the provenance of the mod (the author) is ensured (a checkmark is a wildly known indicator for that)
- 

[^1]: Intermediary certificates are not required to use a TPM/HSM to facilitate the creation of new authorities, to encourage decentralization.
[^2]: RFT5280: Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile https://datatracker.ietf.org/doc/html/rfc5280
[^3]: RFC6960: Online Certificate Status Protocol - OCSP https://datatracker.ietf.org/doc/html/rfc6960
[^4]: They are general guidelines to help with adoption. A separate document with a possible certification / badge can be added later.