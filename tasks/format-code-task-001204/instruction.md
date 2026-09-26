## Problem Statement

Hey, I'm hitting a weird issue with the Airtable integration in Formbricks. Whenever I add new questions to a survey that's already syncing to Airtable, the responses for those new questions just don't show up in the table — like the row gets written but those columns are empty or the whole insert seems off. If I manually add the columns in Airtable first and then submit, it works fine, so I'm guessing it's some kind of timing thing where it tries to write the record before Airtable has actually finished creating the new fields? Also somewhat related — a couple of times when something went wrong with the token, my entire Airtable integration just vanished from the settings and I had to reconnect from scratch, which was pretty annoying. Would love if it could be more robust about waiting for the schema to catch up, and not nuke my whole integration on a transient token error.

## Expected outcomes

- When syncing a survey response to Airtable, newly introduced survey questions should be represented in Airtable before the response row is written, so answers for those questions are not silently lost or written into an incomplete schema.
- Creating multiple missing Airtable fields during a response sync should be robust against Airtable field-creation rate limits rather than firing all field-creation requests in a way that can make the sync fail or race.
- If Airtable reports that a missing field could not be created, the response sync should fail with a clear field-creation error and should not continue to write the response row.
- If the target Airtable table cannot be found while preparing the sync, the response sync should fail with a clear table-not-found error and should not continue to write the response row.
- After missing fields are requested, the sync should wait until Airtable’s table schema reflects those fields before inserting the response row; if the fields never become available after reasonable retries, the sync should fail with a clear timeout-style error instead of writing prematurely.
- Airtable token retrieval failures should surface as a clear token retrieval error without deleting the saved Airtable integration configuration.

## Implementation notes

- Preserve the existing Airtable integration behavior for surveys whose Airtable table already contains all required fields.
- The exact internal structure, helper functions, retry mechanism, logging details, and validation location are up to the implementation, as long as the externally observable sync and token-handling behavior above is satisfied.
- Avoid adding behavior that requires users to manually recreate their Airtable integration after transient token or network failures.
