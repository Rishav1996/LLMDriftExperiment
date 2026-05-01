# Arousal (R)

## Technical Definition
Arousal (from the VAD model) measures the intensity or energy level of the text. It distinguishes between states of calm, dullness, or boredom versus states of excitement, rage, or high energy.

## Prompt Engineering Guidelines
When evaluating for Arousal, look for:
- **1.0 (Active):** High-energy verbs, exclamation points, and intense emotional words. Fast-paced or urgent tone.
- **0.0 (Neutral):** Moderate energy, steady pace.
- **-1.0 (Passive):** Low-energy, slow-paced, or "dull" language. Use of words like tired, calm, or bored.

**Evaluation Prompt snippet:**
"Rate the text from -1.0 to 1.0 on Arousal (R). 1.0 is high-energy/excitement/rage. -1.0 is low-energy/calm/dull."

## Evaluation Rubric
- **-1.0 (Passive/Dull):** Extremely lethargic, no movement, heavy use of words like "sleepy", "calm", "waiting".
- **-0.5 (Subdued):** Calm, steady, low-volume communication with little urgency.
- **0.0 (Neutral):** Standard energy, balanced pace, neither urgent nor boring.
- **0.5 (Animated):** Enthusiastic, moderately paced, engaging vocabulary.
- **1.0 (High-Intensity/Urgent):** High-energy, explosive punctuation, sense of immediate emergency or intense passion.

## Scoring Examples
- **1.0 (High):** "STOP! GET OUT NOW! I CAN'T BELIEVE YOU DID THIS! IT'S UNBELIEVABLE!"
- **0.5 (Mid-High):** "I am very excited to start this new project and I can't wait to see the results!"
- **-1.0 (Low):** "I'm just going to sit here and wait for the rain to stop. There's nothing else to do."
