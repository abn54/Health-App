# Use of the supplied Kaggle resource — Part 3.1

Source: [Mental Health Conversational Data, elvis23](https://www.kaggle.com/datasets/elvis23/mental-health-conversational-data). Public preview inspected on October 8 and rechecked October 13, 2026.

## What was inspected

The preview shows `intents.json` with 80 intent entries. The first, a greeting entry, groups 12 input patterns and five responses under a tag. Its fields are `tag`, `patterns`, and `responses`. This review inspected the page description, displayed license label, file structure, and the greeting sample; it was not a whole-dataset audit.

## How the resource is used in this design

The intent/pattern/response organization informs the proposed model's mapping from differently phrased application questions to a small approved answer catalog. The following examples are authored for this coursework design. They are not copied dataset records or live-model results.

| Application intent | Fictional input variations | Approved answer topic |
| --- | --- | --- |
| `motion` | “Can I turn off the moving circle?” / “Is there a text-only option?” | Explain the cue selector; preserve the current pacing and remembered preference. |
| `storage` | “What gets saved?” / “Will my question stay after I close the page?” | Explain attempted local saving, actual save status, deletion, and live-provider context. |
| `controls` | “Can I stop halfway?” / “What does Pause do?” | Explain immediate End and pause/resume of the current phase. |

This is a design adaptation: varied wording maps to an intent; an approved catalog supplies the response. FastAPI will validate the model's selected ID. The response cannot invent therapeutic advice, change the exercise, or operate application controls.

The inspected greeting responses ask for personal context. Pause instead places optional questions beside a direct Start action, because the assignment asks us to consider reading, typing, and decision effort. This observation supports the interaction choice; it does not evaluate the clinical quality of the dataset.

## Limits and attribution

The page labels the data files as belonging to their original authors. No dataset file was downloaded, redistributed, used for training, or imported into the approved answer catalog. Provenance, consent, and clinical validity were not established by reviewing a public sample.

The dataset is an optional conversation resource. The instructor's R1–R4 / D1–D6 research table is a separate source. It was absent from the early pastes and supplied in full on October 21; see the [completed research mapping](research-findings.md).

## Concrete Part 3.2 adaptation

`backend/catalog.py` implements the authored `motion`, `storage`, and `controls` intent groups above, alongside pacing/scope/start/unsupported. Its deterministic mock groups are used for routine testing; the live Ollama selector receives the same approved app facts and chooses an ID. `backend/test_api.py` checks the stop/storage variants and bounds. The browser live check uses “Do I have to watch a moving shape?” as another authored motion variation. Saved messages identify mock, live, or fixed sources. This carries the inspected intent/pattern/response structure into actual application behavior without importing dataset answers, training on the dataset, or implying clinical validity. The resource does not replace the instructor's R/D table, now independently supplied and mapped.
