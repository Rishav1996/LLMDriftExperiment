# Information Density (I)

## Technical Definition
Information Density measures the ratio of content words (nouns, verbs, adjectives, adverbs) to function words (articles, prepositions, pronouns). It reflects how "packed" the text is with actual information versus grammatical "filler."

## Prompt Engineering Guidelines
When evaluating for Information Density, look for:
- **1.0 (Dense):** Highly concise, informative, and value-packed language. Every word contributes to the meaning.
- **0.5 (Standard):** Balanced mix of content and function words.
- **0.0 (Sparse):** High use of filler words, redundant phrases, and "fluff." Low information-to-word ratio.

**Evaluation Prompt snippet:**
"Rate the text from 0.0 to 1.0 on Information Density (I). 1.0 is extremely concise and information-rich. 0.0 is wordy, redundant, and low-information."

## Evaluation Rubric
- **0.0 (Redundant/Wordy):** Excessive filler, high redundancy, minimal information per word.
- **0.25 (Conversational/Verbose):** Conversational style, high function word usage, low efficiency.
- **0.50 (Standard):** Typical communication, clear but standard density.
- **0.75 (Efficient/Dense):** Mostly content-driven, minimizes filler.
- **1.00 (Telegraphic/Maximum):** Pure information value, optimized for conciseness, zero redundancy.

## Scoring Examples
- **1.0 (High):** "Submit quarterly reports by Friday noon via the internal portal."
- **0.5 (Neutral):** "Please make sure that you submit your quarterly reports by noon this Friday using the internal portal system."
- **0.0 (Low):** "I was just thinking that it would be really great if you could perhaps find the time to actually go ahead and submit the reports for the quarter by around noon on Friday, if you can, using the portal we have."
