# Sources and provenance

Dataset and support references reviewed on October 8, 2026; the dataset preview and course-source availability rechecked October 13, 2026. Links below identify source material; they do not imply that the prototype has been evaluated by these organizations.

## Course brief

The student supplied the assignment text in this chat, including the four skill descriptions, study summary, timing rule, required stack, milestone instructions, and testing boundaries. Its course entry is [Module VI — Assignment 3](https://psu.instructure.com/courses/2484533/modules#context_module_6139769). The supplied text is the source used; authenticated Canvas content was not accessed.

The referenced R1–R4 / D1–D6 table is absent from the supplied text. Only the narrative's explicit R1 attention finding and D1 limitation are attributed by label. The remaining research mapping must be completed from the actual table, not reconstructed from general mental health knowledge.

The October 13 paste contains the same assignment body and still omits the table. Opening the supplied course link reached school device authentication; authenticated course content was not retrieved. No account identifier, authentication URL, token, or sign-in screenshot is included in the submitted evidence.

## Optional conversational dataset

The student supplied [Mental Health Conversational Data on Kaggle](https://www.kaggle.com/datasets/elvis23/mental-health-conversational-data). The assignment identifies it as an optional conversation resource. The initial text-only retrieval returned no body; a subsequent browser inspection successfully exposed the data card and file preview.

Verified in the browser on October 8, 2026:

- The preview lists one file, `intents.json`, with an `intents` array containing 80 items.
- The inspected first item uses `tag`, `patterns`, and `responses`. Its greeting category has 12 input examples and five proposed replies.
- The page's license label is “Data files © Original Authors.” No explicit permission to redistribute or train on the records was established by this review.

Only the greeting item was expanded and read. The other records, original provenance, consent, and clinical validity were not audited. No file was downloaded. The publisher's description proposes therapist-like chatbot use; that statement does not establish that the records are actual therapist transcripts or suitable therapeutic guidance.

Design takeaway: grouping varied inputs under an intent offers a concrete comparison for the prototype's approved-answer selection. The inspected greeting replies solicit personal context; this project keeps entry direct and its questions optional to limit effort. This is an interaction-design observation, not a clinical judgment about the dataset.

The current design does not ingest these records or use their replies as approved application content. A possible later use is to inform independently authored fictional out-of-scope questions, with reuse terms checked before copying any records. The prescribed skill and application catalog remain grounded in the assignment and project design. The instructor's R/D research table is still a separate missing source.

The [dataset design notes](dataset-design-notes.md) document the design adaptation: authored variations of application questions mapped to approved motion, storage, and control explanations. The file structure and first greeting entry were rechecked in the browser on October 13; this did not expand the review into a whole-file audit.

## Proposed support-panel references

- [988 Suicide & Crisis Lifeline](https://988lifeline.org/): primary reference for the U.S. call/text 988 options and [official chat destination](https://chat.988lifeline.org/), as linked by the official site. The chat service itself was not tested or contacted.
- [Find A Helpline](https://findahelpline.com/): directory with a country selector for locating other regional resources. The directory page was reviewed; individual listings and global service availability were not audited.

Proposed short panel content:

> This is a coursework prototype, not a crisis service. Nobody monitors this app.
>
> United States: call or text 988, or use the 988 Lifeline's chat.
>
> Other locations: choose your country at Find A Helpline.

Bundle the short text and destination links with the client. Phone and text links should retain readable numbers so the information is usable when a desktop cannot open them. Opening an external destination requires a user's action. Verify link destinations before later demonstrations without placing calls, sending messages, or entering a crisis-service queue.

These references support contact-information design only; they are not evidence for the effectiveness of the exercise or this prototype. No clinical research review or existing-app comparison was performed for this milestone.
