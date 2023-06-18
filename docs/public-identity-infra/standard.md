# Public Modding Identity Infrastructure

## 1. Introduction

This document defines the infrastructure used to distribute code certificates to Minecraft mod developers and the policies surrounding this system.

### 1.1. Terminology

 The keywords "MUST", "MUST NOT", "SHOULD", and "MAY" in this document are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

## 2. Certificate Authorities

Certificate Authorities are organisations responsible for maintaining, delivering and invalidating code certificates.

### 2.1. Root Authorities

Root Authorities are Certificate Authorities that can be fully trusted by verifiers. They MAY deliver certificates directly and MAY sign other Certificate Authorities after verifying the new Certificate Authority is conforming to this document.

### 2.2. Authority Components

Certificate Authorities MUST provide the following component:
- Online Certificate Status Protocol server ([RFC 6960](https://www.rfc-editor.org/rfc/rfc6960))

Certificate Authorities SHOULD and Root Authorities MUST provide the following components:
- Time-Stamp Protocol server ([RFC 3161](https://www.rfc-editor.org/rfc/rfc3161))
- Certificate Transparency log ([RFC 6962](https://www.rfc-editor.org/rfc/rfc6962))

### 2.3. Certificate Safety

Certificate Authorities MUST NOT sign certificates directly using their primary certificate. Rather, one or multiple intermediary certificate valid for equal or less than one year MUST be used. The primary certificate MUST be stored offline and SHOULD be stored in a Hardware Security Module.

## 3. Certificate Structure

Certificate MUST use the X.509 format as defined by [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280). 

### 3.1. Subject Fields

#### 3.1.1. Common Name (CN)

The subject Common Name MUST be the subject real world name or a uniquely identifiable username. Under certain circumstances, the Common Name MAY be set to `Automation` if the Organization field is set.

#### 3.1.2. Organization (O)

The subject Organization CAN be the subject organisation under which that certificate is applicable. It MAY be set to `Developer` if not applicable.

#### 3.1.3. Distinguished Name (DN)

The subject Distinguished Name MUST be constructed according to [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280), using the `CN` and `O` fields.

#### 3.1.4. Other fields

The certificate MUST NOT contain other subject fields.

### 3.2. Issuer Fields

The Certificate Authorities MUST make sure to build an [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280) compliant, unique, distinguished name. The exact fields used are left unspecified by this document.

### 3.3. Certificate Uniqueness

There MUST only be a single valid certificate with the same Distinguished Name at the same time. Certificates with the same Common Name MUST belong to the same physical person.

### 3.4. Key Algorithms

Certificates must use the RSA algorithm of minimum length 2048 or the ECDSA algorithm of minimum length 256.

## 4. Issuing Policies

Certificate issuing MUST be done after manual review by a human. The subject is responsible for proving they are legitimate to obtain the certificate, through official documents or online presence, when applicable. The Certificate Authority is responsible for verifying the uniqueness of the certificate delivered, across all commonly trusted authorities.

### 4.1. Legal documents

A subject requesting a certificate with their full name MAY submit legal documents proving who they are.

### 4.2. Paid resources

A subject requesting a certificate with their username MAY submit various paid resources proving who they are. 

This includes, but not limited to:
- Minecraft accounts
- Internet domains

### 4.3. Social resources

A subject requesting a certificate with their username MAY submit various social, free, resources proving who they are.

This includes, but not limited to:
- Social media accounts: Discord, Reddit, Twitter, ...
- Email addresses

### 4.4. Issuing Thresholds

For a certificate to be issued, the subject MUST submit one of the following:

- One or more legal documents
- Two or more paid resources
- One paid resources and one or more social resources
- Three or more social resources

If a certificate with the same Common Name already exists, the subject MUST prove ownership of one of those certificates.

Certificate Authorities MAY add additional requirements.

### 4.5. Data retention

Upon deliverance, the Certificate Authority MUST NOT keep any provided resources or documents in clear text format. The Certificate Authority MUST keep a hash of a unique identifier of the resources or documents and share that hash with other Certificate Authorities through a public database (format TBD).

### 4.6. Data privacy

The Certificate Authority MUST NOT make any information other than subject fields explicitly provided by the subject public. The Certificate Authority MUST adhere to the best privacy practices according to the European Union General Data Protection Regulations.

### 4.7. Certificate Transparency

The Certificate Authority MUST publish the issued certificate to three or more Certificate Transparency logs. 

## 5. Revocation Policies

If software signed by a certificate is found to cause real world harm, the Certificate Authority MUST, within reasonable delays, add the certificate to their Certificate Revocation List and publish it through their Online Certificate Status Protocol server.
