# Politeness (P)

## Technical Definition
Politeness measures the use of etiquette, softeners, and respectful language to maintain social harmony. It ranges from abrasive, direct commands to high use of formal politeness markers.

## Prompt Engineering Guidelines
When evaluating for Politeness, look for:
- **1.0 (Polite):** Frequent use of "please," "thank you," and indirect requests (e.g., "Would you mind..."). High use of honorifics or formal addresses.
- **0.0 (Civil):** Clear, direct language without being rude.
- **-1.0 (Abrasive):** Use of direct, blunt commands. Absence of softeners. Potentially rude or dismissive phrasing.

**Evaluation Prompt snippet:**
"Rate the text from -1.0 to 1.0 on Politeness (P). 1.0 is extremely polite/formal. -1.0 is extremely abrasive/rude. 0.0 is civil/neutral."

## Evaluation Rubric
- **-1.0 (Abrasive/Hostile):** Blunt commands, lacks any social grace, potentially demeaning or rude.
- **-0.5 (Blunt):** Direct imperatives; lacks "please" or "thank you"; overly task-focused.
- **0.0 (Neutral/Civil):** Direct and professional; respectful but minimal social fluff.
- **0.5 (Courteous):** Uses basic etiquette ("please", "would you"), acknowledges the request.
- **1.0 (High Etiquette/Formal):** Uses honorifics, indirect phrasing ("would you mind"), deep concern for the user's feelings/burden.

## Scoring Examples
- **1.0 (High):** "Would you be so kind as to provide the document at your earliest convenience? Thank you so much for your assistance."
- **0.0 (Neutral):** "Please send the document when you have it. I need it for the report."
- **-1.0 (Low):** "Send me the document now. Don't make me ask again."
