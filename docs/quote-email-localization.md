# Quote email localization contract

The source-page language controls both the internal HIPStudio notification and the customer confirmation email.

- Supported languages: Hungarian (`hu`), English (`en`), German (`de`).
- Every key in `CUSTOMER_FIELDS` has an explicit human-readable label in all three languages.
- There is no technical underscore-to-space fallback for customer email labels.
- Empty submitted fields are omitted.
- Every non-empty customer field is echoed back in the customer confirmation.
- Internal routing, priority, complexity, ownership and triage metadata is never part of `CUSTOMER_FIELDS` and is not echoed to the customer.
- Customer confirmations state that the request was received and that HIPStudio will make contact shortly.
- Reply-To remains `info@hipstudio.hu`.

Regression coverage: `tools/test_quote_email_localization.py`.
