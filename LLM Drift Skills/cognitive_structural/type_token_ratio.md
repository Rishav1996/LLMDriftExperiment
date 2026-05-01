# Type-Token Ratio (D)

## Technical Definition
Type-Token Ratio (TTR) is a measure of vocabulary diversity. It is calculated as the ratio of unique words (types) to the total number of words (tokens) in a text. High TTR indicates a sophisticated and varied vocabulary, while low TTR suggests repetitiveness.

## Prompt Engineering Guidelines
When evaluating for Type-Token Ratio, look for:
- **1.0 (Sophisticated):** Use of a wide variety of words. Avoidance of repeating the same adjectives or nouns. High lexical density.
- **0.5 (Standard):** Typical variety for conversational language.
- **0.0 (Repetitive):** Frequent repetition of the same words, phrases, or sentence structures. Limited vocabulary.

**Evaluation Prompt snippet:**
"Rate the text from 0.0 to 1.0 on Type-Token Ratio (D). 1.0 is highly sophisticated and diverse vocabulary. 0.0 is extremely repetitive and simple vocabulary."

## Evaluation Rubric
- **0.00 (Minimal/Repetitive):** Highly constrained vocabulary; constant recycling of basic words.
- **0.25 (Conversational/Simple):** Standard vocabulary, predictable word choices, some minor repetition.
- **0.50 (Balanced/Standard):** Varied usage of common words; professional level variety.
- **0.75 (Diverse):** Frequent use of synonyms, specific nouns, and unique adjectives.
- **1.00 (Sophisticated/Rich):** Exceptional lexical diversity; academic-grade variety and word precision.

## Scoring Examples
- **1.0 (High):** "The kaleidoscopic array of flora exhibited an ephemeral brilliance, captivating the observers with its multifaceted splendor."
- **0.5 (Neutral):** "There were many different kinds of flowers in the garden and they looked very beautiful to everyone who saw them."
- **0.0 (Low):** "The flowers were nice. The flowers were pretty. I liked the nice flowers. The flowers were very nice flowers."
