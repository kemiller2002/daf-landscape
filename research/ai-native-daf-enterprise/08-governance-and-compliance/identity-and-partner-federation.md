# Identity, partner federation and MFA

**Owner requirement (2026-11-21):** login security must focus on integration with partners, the organizations that own the accounts, and must support MFA.

**Decision:** DD-021 in the [decision log](../DECISION-LOG.md).

**Executable policy:** [`../models/Daf.Enterprise/Identity.fs`](../models/Daf.Enterprise/Identity.fs), with 12 tests in [`IdentityTests.fs`](../models/Daf.Enterprise.Tests/IdentityTests.fs).

**Vendor fit:** [`../07-technology-architecture/vendor-api-assessment.md`](../07-technology-architecture/vendor-api-assessment.md), identity category.

This document extends [`security-architecture.md`](security-architecture.md). It does not replace it.

## 1. Who owns the account relationship

In the channel-led DAF market, the account relationship usually belongs to a **partner organization**:
- a wealth firm or broker-dealer, as in the RCF–Ren programmes for Edward Jones, Ameriprise and others (industry report §2.2);
- an RIA or advisor platform;
- an institutional sponsor using the platform under Model C.

The sponsor holds legal control of the assets (DD-003). The partner owns the *people*: its advisors, its staff and, often, the client relationship. Identity must therefore be **organization-centric**:

```
Sponsor tenant (legal control; policies)
 └─ Partner organization (owns program + client relationships; its own IdP)
     ├─ Partner users: advisors, partner admins, service staff   ← federated from the partner IdP
     ├─ Partner systems (portfolio, CRM, reporting)              ← OAuth clients, sender-constrained
     └─ Accounts in the partner's program
          └─ Donors (platform customer identity, or partner-federated where the partner authenticates clients)
               └─ Donor-side agents (delegated principals, DD-017)
```

## 2. Design principles

1. **Federate, don't duplicate.** Partner users log in with their own organization's identity provider (OIDC preferred, SAML 2.0 supported). The partner controls joiners and leavers through **SCIM 2.0** provisioning. When the partner disables a user, platform access ends at once: deprovisioning is checked first in `decide`.
2. **MFA everywhere it matters, phishing-resistant where it matters most.**
   - Viewing account data requires **AAL2** (NIST SP 800-63B).
   - High-value grant recommendations, delegation changes, partner user management, recovery-factor changes and staff privileged operations require **phishing-resistant** authentication (WebAuthn/passkeys or hardware keys) that is **fresh**: within 15 minutes [A].
3. **Trust a partner's MFA only by contract and by claim.** A partner's assertion counts toward MFA only if *both*:
   - (a) the partner has **contractually attested** its MFA policy (`MfaAttestedByContract`); and
   - (b) the assertion carries **`amr` values the platform accepts** (RFC 8176: `hwk`/`phr` for phishing-resistant, `mfa`/`otp` for AAL2).

   Otherwise a federated login is treated as single-factor, and the platform performs **step-up locally**. Tested: an untrusted partner's `hwk` claim is ignored.
4. **Step-up, not lockout.** If a session lacks the required assurance, the API returns an **RFC 9470 step-up challenge** (`insufficient_user_authentication` with `acr_values` and `max_age`). The client re-authenticates, at the partner IdP if it is trusted, otherwise locally.
5. **Relationship authorization is separate from assurance, and is checked first.** Strong MFA never grants access across organizations:
   - an advisor acts only on accounts **owned by their organization** *and* where the donor granted them a privilege;
   - partner admins manage their organization's users but **cannot touch donor accounts**;
   - advisors cannot change delegation or recovery; only the donor can.
6. **Machines get sender-constrained tokens.** Partner systems use OAuth 2.0 client credentials with **mTLS-bound tokens (RFC 8705) or DPoP (RFC 9449)**, `private_key_jwt` client authentication, organization-scoped data, and least-privilege scopes. Bearer-only tokens are refused (tested).
7. **Delegated actions carry the actor.** When a partner system acts *for* a user, it uses **token exchange (RFC 8693)**. The token records both the subject (the advisor) and the actor (the system), so audit shows who did what through which integration.
8. **Fine-grained authorization for money-adjacent requests.** Grant recommendations from partners use **Rich Authorization Requests (RFC 9396)** carrying account, amount and recipient. Where a partner offers the donor confirmation flow, it uses **CIBA** (OpenID Client-Initiated Backchannel Authentication) for out-of-band donor approval. The security baseline for partner APIs is the **FAPI 2.0 Security Profile**.
9. **Recovery is the weakest link and is treated as a sensitive action.**
   - Changing recovery factors needs fresh phishing-resistant authentication (tested; TOTP is refused).
   - Help-desk recovery triggers a cooling-off period before payout-relevant actions (CTL payee cooling-off pattern), plus a notice to prior channels.
10. **Staff:** SSO with phishing-resistant MFA only, and just-in-time privileged elevation. No standing production write access (CTL-031, CTL-033).

## 3. Assurance mapping (as implemented)

| Login method | AAL | Phishing-resistant | Notes |
|---|---|---|---|
| Platform passkey / WebAuthn | 2 | Yes | Synced passkeys count as AAL2 under 800-63B rev. 4. Device-bound hardware keys can be treated as AAL3 for staff if policy requires |
| Platform TOTP | 2 | No | Allowed for viewing and routine grants; refused for sensitive actions |
| Platform password only | 1 | No | Never reaches account data; step-up to AAL2 is required |
| Partner federated, trusted, `amr` ∋ `hwk`/`phr` | 2 | Yes | — |
| Partner federated, trusted, `amr` ∋ `mfa`/`otp` | 2 | No | — |
| Partner federated, untrusted or no accepted `amr` | 1 | No | The platform steps the user up locally |

## 4. Action requirements (as implemented)

| Action | Minimum | Phishing-resistant | Freshness |
|---|---|---|---|
| View account | AAL2 | — | — |
| Recommend grant ≤ $25k [A] | AAL2 | — | — |
| Recommend grant > $25k [A] | AAL2 | **Yes** | 15 min |
| Change delegation (advisor, agent) | AAL2 | **Yes** | 15 min |
| Manage partner users | AAL2 | **Yes** | 15 min |
| Change recovery factors | AAL2 | **Yes** | 15 min |
| Staff privileged operation (JIT only) | AAL2 | **Yes** | 15 min |

Thresholds are governed policy parameters with expiry (CTL-047), not code constants. The values above are design defaults.

## 5. Partner onboarding checklist

1. A **federation agreement** covering protocol, signing keys and rotation, the **MFA attestation** (which `amr` values the partner will assert, and when), incident notification, and SCIM joiner/leaver timing (for example, deprovision within one hour).
2. **Metadata exchange and test tenant.** Run the conformance tests below against the partner IdP.
3. **SCIM endpoint** configured, plus a group-to-role mapping (advisor, partner admin, service).
4. **Machine clients** registered with mTLS certificates or DPoP keys, and scopes approved per integration (for example, `positions:read` for a portfolio system and `recommendations:write` for a CRM).
5. **Webhook subscriptions** signed (HMAC or JWS) and organization-scoped.
6. **Go-live gate:** the security conformance suite passes. It covers federation, step-up, deprovisioning latency, cross-org denial and sender-constrained tokens.

## 6. Conformance tests a partner integration must pass

These mirror [`IdentityTests.fs`](../models/Daf.Enterprise.Tests/IdentityTests.fs). In production they run against the real IdP configuration.

1. A trusted phishing-resistant `amr` allows a high-value recommendation.
2. A trusted `otp` allows routine actions but steps up high-value ones.
3. An untrusted partner's MFA claims are ignored.
4. A password-only session never reads account data.
5. Stale authentication steps up sensitive actions.
6. TOTP cannot change recovery factors.
7. Cross-organization access is denied.
8. An advisor without donor consent is denied.
9. Advisors cannot change delegation, and partner admins cannot read accounts.
10. A SCIM-deprovisioned user is denied immediately.
11. Staff privileged operations need JIT plus phishing-resistant MFA.
12. Machine clients need sender-constrained tokens, own-organization accounts and granted scopes.

## 7. What this changes elsewhere

- **API catalog:** adds an `organizations`, `federation` and `scim` domain, plus a `sessions` / step-up challenge contract. See [`../04-enterprise-apis/api-completeness.md`](../04-enterprise-apis/api-completeness.md).
- **Security architecture:** the advisor row ("federated where possible") becomes **federated by default for partner-owned programmes**, with SCIM and MFA attestation.
- **Controls:** CTL-051 to CTL-054 (below) are added to [`controls.csv`](controls.csv).

| Control | Description |
|---|---|
| CTL-051 | Partner MFA attestation and `amr` acceptance |
| CTL-052 | SCIM deprovisioning latency monitor |
| CTL-053 | Sender-constrained tokens for partner machine clients |
| CTL-054 | Recovery-factor change protection |
