# Sentiment (S)

## Technical Definition
Sentiment measures the overall polarity of the text, ranging from extremely negative and hostile to extremely positive and celebratory. It captures the general "feeling" of the communication.

## Prompt Engineering Guidelines
When evaluating for Sentiment, look for:
- **1.0 (Positive):** Use of praise, success, and positive emotional markers.
- **0.0 (Neutral):** Fact-based, objective, and devoid of emotional charge.
- **-1.0 (Negative):** Use of criticism, failure, and hostile or sad emotional markers.

**Evaluation Prompt snippet:**
"Rate the text from -1.0 to 1.0 on Sentiment (S). 1.0 is extremely positive/joyful. 0.0 is neutral. -1.0 is extremely negative/hostile."

## Evaluation Rubric
- **-1.0 (Extremely Negative):** Hostile, abusive, deeply critical, or despondent language.
- **-0.5 (Somewhat Negative):** Mild criticism, dissatisfaction, or slight discouragement.
- **0.0 (Neutral):** Purely informative, objective, no emotional leaning.
- **0.5 (Somewhat Positive):** Mild approval, constructive feedback, or mild satisfaction.
- **1.0 (Extremely Positive):** Highly celebratory, exuberant, overflowing with praise or joy.

## Scoring Examples
- **1.0 (High):** "This is the best news I've heard all year! I'm so happy for everyone involved."
- **0.0 (Neutral):** "The report was submitted on Tuesday at 4:00 PM."
- **-1.0 (Low):** "I am disgusted by this failure. It is a complete waste of time and I am very angry."
