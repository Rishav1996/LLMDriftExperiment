# Authenticity (U)

## Technical Definition
Authenticity measures the degree to which language is perceived as honest, vulnerable, and self-disclosing. High authenticity is characterized by a personal, "real" tone, while low authenticity appears guarded, professional, or artificial.

## Prompt Engineering Guidelines
When evaluating for Authenticity, look for:
- **High U:** Use of personal pronouns, self-referential statements, and emotional disclosure. Transparency about internal states or mistakes.
- **Low U:** Use of impersonal, "corporate-speak," or highly polished/rehearsed phrasing. Avoidance of self-reference.

**Evaluation Prompt snippet:**
"Rate the text from 0.0 to 1.0 on Authenticity (U). 1.0 is a deeply honest, personal, and vulnerable disclosure. 0.0 is a guarded, robotic, or purely professional performance."

## Evaluation Rubric
- **0.00 (Robotic/Guarded):** Pure corporate-speak; no self-reference; devoid of human affect.
- **0.25 (Professional/Detached):** Highly polished; avoids vulnerability; uses formal distancing language.
- **0.50 (Balanced):** Professional but sincere; uses mild self-reference.
- **0.75 (Personal/Transparent):** Clear evidence of personal belief; comfortable with self-disclosure.
- **1.00 (Vulnerable/Raw):** Radical honesty; high emotional vulnerability; total transparency about feelings or mistakes.

## Scoring Examples
- **1.0 (High):** "To be honest, I'm struggling with this decision. It makes me feel vulnerable to admit I don't have all the answers yet."
- **0.5 (Neutral):** "I am working on the decision and I hope to find a solution that works for everyone involved."
- **0.0 (Low):** "The decision-making process is currently under review to ensure optimal alignment with organizational objectives."
