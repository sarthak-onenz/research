# Heuristics to Identify AI-Written Social Media Posts

## Part 1: Heuristics Identifiable Using Regex and String Matching

These patterns can be detected using simple pattern matching, regular expressions, and basic text analysis without requiring AI/ML models:

### Structural & Formatting Patterns

**Excessive Use of Em Dashes (—)**: Count occurrences of em dashes (—) relative to text length. ChatGPT (especially GPT-4) overuses em dashes to connect clauses. A ratio of more than 1 em dash per 100 words is suspicious.
- Regex: `—` or `\u2014`
- Pattern: Multiple em dashes in short text blocks

**Bullet Point and List Addiction**: Detect frequent use of bullet points, numbered lists, and emoji bullets (✅, 🚀, ❌, ✨, ⭐).
- Regex: `^[\s]*[•\-\*]\s`, `^\s*\d+\.\s`, `^[\s]*[✅❌🚀✨⭐️]\s`
- Pattern: Lists with emoji bullets, especially alternating ❌ (problems) and ✅ (solutions)

**One Sentence per Line "Broetry"**: Detect posts with excessive line breaks creating short, dramatic lines.
- Pattern: Lines with fewer than 10 words followed by line breaks
- Regex: Count ratio of newlines to total word count

**Formulaic Post Structure**: Identify problem → solution patterns with specific emoji sequences.
- Pattern: ❌ followed by text, then ✅ followed by text
- Regex: `❌.*?✅` or similar emoji sequence patterns

**Overuse of Headings with Colons**: Detect rigid title formats like "X: How to Do Y".
- Regex: `^.+:\s*(How to|Ways to|Tips to|Steps to)`
- Pattern: Multiple headings all following the same colon format

### Language & Phraseology Patterns

**Cliché Phrase Detection**: Search for common AI filler phrases.
- Exact matches: "It is worth noting that", "In conclusion", "I am pleased to announce", "Based on the information provided"
- Regex patterns for variations of these phrases

**ChatGPT's "Not X, but Y" Construction**: Detect the parallel contrast structure ChatGPT loves.
- Regex: `(not just|isn't just|not only).{1,50}(but|it's about|also)`
- Pattern: "X is not just about A — it's about B" constructions

**Excessive Transitional Words**: Count paragraph-starting transitions.
- Regex: `^(However|Additionally|Moreover|Furthermore|Nevertheless),\s`
- Pattern: High frequency of formal conjunctive adverbs at paragraph starts

**Unnecessary Clarifications**: Detect redundant phrases.
- Exact matches: "true fact", "in my personal opinion", "personally, I think"
- Regex: Common redundant constructions

**Fancy Vocabulary Overuse**: Count Latin-origin or overly formal words.
- Word lists: "utilize" vs "use", "ameliorate" vs "improve", "facilitate", "leverage", "paradigm"
- Pattern: Higher than normal frequency of formal synonyms

**Repetitive Phrasing**: Detect repeated phrases or near-duplicates.
- String matching: Identify sentences or phrases that appear multiple times
- Fuzzy matching for slight variations of the same idea

### Social Media-Specific Patterns

**Emoji Overload and Placement**: Count emoji frequency and positioning.
- Regex: Count all Unicode emoji characters
- Pattern: Emojis after every sentence, specific emoji sequences (🚀✨⭐️)
- Position detection: Emojis at line starts, ends, or as bullet points

**Clickbaity Openers**: Detect formulaic opening lines.
- Exact matches: "Exciting news:", "I wasn't going to share this, but", "Here's what I learned"
- Regex: Common attention-grabbing templates

**Generic Hashtags**: Identify broad, generic hashtag patterns.
- Pattern: Multiple generic hashtags like #AI #business #success #growth
- Regex: Count hashtags and identify overly broad ones

**Formulaic Call-to-Actions**: Detect standard engagement prompts.
- Exact matches: "Let's continue the conversation!", "What do you think?", "Agree or disagree?"

### Grammar and Punctuation Patterns

**Perfect Grammar (Too Clean)**: Analyze for absence of common human errors.
- Pattern: Zero spelling mistakes, perfect punctuation
- Check for common typos that are suspiciously absent

**Consistent Punctuation Style**: Detect overly consistent comma usage, apostrophes, etc.
- Pattern: Never mixing punctuation styles (always Oxford comma, consistent quote marks)

### Additional Regex-Detectable Patterns

**Overuse of Specific Words**: Count frequency of AI-favorite terms.
- Words: "landscape" (as in business landscape), "delve", "comprehensive", "holistic", "Furthermore", "Moreover", "Additionally", "Consequently"
- Pattern: Higher than normal frequency in casual contexts

**Numbered Step Patterns**: Detect formulaic step-by-step formats.
- Regex: `Step \d+:`, `\d+\.\s[A-Z].*:`, numbered processes

**Question-Answer Self-Dialogue**: AI sometimes creates fake Q&A structures.
- Pattern: "You might ask..." followed by "The answer is..."
- Regex: Question words followed by structured answers

**Consistent Sentence Length**: Measure sentence length variation.
- Pattern: Suspiciously similar sentence lengths throughout

**Hidden Unicode Characters**: ChatGPT and other LLMs can inject invisible characters.
- Pattern: Zero Width Space (U+200B), Em-Dash variations, other invisible Unicode
- Regex: `[\u200B\u200C\u200D\uFEFF]` for zero-width characters
- Detection: Unusual Unicode characters that shouldn't appear in normal text

**Overuse of Superlatives and Intensifiers**: AI tends to use more dramatic language.
- Words: "incredibly", "extremely", "absolutely", "definitely", "certainly", "undoubtedly"
- Pattern: Higher frequency of certainty markers and intensifiers than natural speech

**Awkward Passive Voice Constructions**: AI often defaults to passive voice incorrectly.
- Regex: `(is|are|was|were|being|been)\s+\w+ed\b` (basic passive detection)
- Pattern: Unnatural passive voice where active would be more appropriate

**Repetitive Sentence Starters**: AI models often fall into repetitive opening patterns.
- Pattern: Multiple sentences starting with the same words ("The", "This", "It")
- Regex: Count sentence beginnings for unusual repetition patterns

**Overly Formal Contractions Avoidance**: AI avoids contractions in casual contexts.
- Pattern: Full forms where contractions would be natural ("do not" vs "don't")
- Regex: Count ratio of formal vs contracted forms

**Specific ChatGPT Phrase Patterns**: Known ChatGPT linguistic fingerprints.
- Exact phrases: "As an AI language model", "I don't have personal experience", "It's worth noting"
- Patterns: "In the context of", "In the realm of", "When it comes to"
- Regex: Exact string matches for known AI phrases

**Unnatural Punctuation Spacing**: AI sometimes has odd spacing around punctuation.
- Pattern: Inconsistent spaces around commas, periods, or other marks
- Regex: `\s{2,}`, unusual spacing patterns

**Overuse of Apologetic Language**: AI models tend to hedge and apologize excessively.
- Words: "Unfortunately", "Regrettably", "I apologize", "Sorry"
- Pattern: Higher frequency of apologetic terms in contexts where they're unnecessary

**Technical Term Misuse Patterns**: AI uses technical words incorrectly but consistently.
- Pattern: Specific technical terms used in wrong contexts
- String matching: Domain-specific terminology used inappropriately

**Formulaic Conclusion Patterns**: AI uses predictable ending structures.
- Phrases: "In summary", "To conclude", "In closing", "Overall"
- Pattern: Formulaic wrap-up language rather than natural endings

**Overuse of Qualifying Adverbs**: AI hedges with excessive qualifiers.
- Words: "typically", "generally", "usually", "often", "frequently", "commonly"
- Pattern: Higher than normal frequency of uncertainty markers

**Rule of Three Overuse**: ChatGPT absolutely loves the rule of three - structuring content in groups of three items.
- Pattern: Repeated use of three-item lists or constructions
- Regex: Detect patterns like "X, Y, and Z" structures appearing frequently
- Examples: "Just me, a thing, and a whimsical third thing"

**Repetitive Phrase Usage**: AI lacks typical human aversion to repetition and may repeat the same phrase multiple times.
- Pattern: Same phrase appearing 2+ times in short text
- String matching: Exact phrase repetition detection
- Example: Using "wild, right?" multiple times

**Common GPT Transition Phrases**: Specific transition patterns ChatGPT uses frequently.
- Phrases: "But here's the thing", "And [topic]? Wow", "So yeah", "Additionally,", "Furthermore,", "Moreover,"
- "But here's the thing" is one of the usual key turning points in these essays
- Regex: Exact string matches for these transition patterns

**Ellipsis Character Detection**: Check if ellipsis is three periods or a single ellipsis character.
- Pattern: Single ellipsis character (…) vs three periods (...)
- Regex: `\u2026` vs `\.{3}` - AI often uses the single Unicode ellipsis

**"Not Just X, But Y" Construction Overuse**: Extended version of the original pattern.
- Pattern: "not only... but also", "not just... but", "it's not about X, it's about Y"
- This construction appears as a common ChatGPT tell

**Empty Metaphors and Similes**: Detectable through specific weak comparative structures.
- Pattern: "like" followed by vague or meaningless comparisons
- Regex: `like.*?future.*?`, weak metaphorical constructions
- Metaphors that "feel empty" or are "disingenuous"

**Chaos/Control Word Obsession**: ChatGPT can't get enough of the concept of chaos.
- Words: "chaos", "control", "balance", "harmony"
- Pattern: Overuse of abstract conceptual words about order/disorder

**Fake Relatability Phrases**: AI trying too hard to sound human.
- Phrases: "How do you do, fellow kids" style attempts
- Pattern: "You know that feeling when...", "We've all been there", "That moment when"
- Comes off as awkward attempts at human connection

**Granular Time References**: Overly specific but generic time descriptions.
- Pattern: "that soft morning light", "crisp evening air", vague but specific temporal details
- String matching: Generic sensory time descriptions

**"So" Paragraph Beginnings**: Predictable "So" paragraphs near the end.
- Pattern: Paragraphs starting with "So" especially in conclusions
- Regex: `^So\s` at paragraph beginnings

**Filler Question Constructions**: Rhetorical questions that add no value.
- Pattern: "What does this mean?", "Why does this matter?", "How do we fix this?"
- Often followed immediately by the answer

**Overuse of Quotation Marks for Emphasis**: AI uses quotes incorrectly for emphasis rather than actual quotations.
- Pattern: Single words in quotes that aren't actual quotes
- Regex: `"[^"]{1,15}"` - short quoted phrases that aren't citations

**Corporate Presentation Language**: Language that feels like "masturbatory Silicon Valley product launch presentation".
- Phrases: "leverage synergies", "paradigm shift", "game changer", "revolutionary"
- Pattern: Buzzword density higher than normal conversation

## Part 2: Heuristics Requiring GenAI or Advanced Analysis

These patterns require semantic understanding, context analysis, or AI models to detect effectively:

### Content & Meaning Analysis

**Lack of Personal Voice or Fingerprint**: Detecting unique writing style requires semantic analysis of personality markers, humor patterns, and individual quirks that can't be captured by simple pattern matching.

**Emotionally Tone-Deaf Content**: Understanding when enthusiasm is inappropriate for the topic or when emotional responses don't match the context requires contextual AI analysis.

**Generic or Shallow Content**: Determining content depth and meaningfulness requires understanding subject matter and context beyond simple pattern matching.

**Lack of Personal Anecdotes**: Distinguishing between generic examples and genuine personal experiences requires understanding narrative structure and authenticity markers.

### Tone and Style Analysis

**Overly Consistent "Monotone" Tone**: Detecting emotional variation and natural human voice modulation requires sentiment analysis and tonal understanding.

**Too "Neat" and Polished**: Understanding natural human writing flow versus mechanical transitions requires stylistic analysis.

**Avoidance of Strong Opinions**: Detecting hedging behavior and opinion strength requires sentiment and stance analysis.

**Unnatural Formality Levels**: Understanding appropriate register for context requires sociolinguistic analysis.

### Semantic and Contextual Analysis

**Unrelatable or Odd Examples**: Evaluating whether analogies and examples fit contextually requires domain knowledge and semantic understanding.

**Missing Context or Logical Gaps**: Detecting coherence issues and logical flow problems requires understanding argument structure.

**Factual Errors Stated Confidently**: Requires fact-checking against knowledge bases and understanding confidence levels.

**Off-Topic Responses**: Understanding whether content matches the intended topic requires semantic similarity analysis.

### Advanced Linguistic Patterns

**Lack of Contractions and Informal Language**: While contractable phrases can be detected with regex, understanding when informality is expected requires contextual analysis.

**Unnatural Conversation Flow**: In comment threads or dialogues, detecting unnatural response patterns requires conversation analysis.

**Cultural and Contextual Appropriateness**: Understanding whether language choices fit the cultural context requires cultural knowledge models.

**Subtle Semantic Repetition**: While exact repetition can be caught with string matching, detecting when the same idea is expressed in different words requires semantic similarity analysis.

### Model-Specific Behavioral Patterns

**ChatGPT's Hedging Behavior**: Understanding patterns of uncertainty expression and risk-averse language requires understanding model behavior.

**Balanced Viewpoint Tendency**: Detecting artificial "on one hand, on the other hand" structures requires understanding argumentation patterns.

**Response to Controversial Topics**: Understanding how AI models handle sensitive topics differently from humans requires content analysis.

## Implementation Notes for Part 1 (Regex/String Matching)

When implementing these heuristics in Python:

1. **Create scoring functions** for each pattern (0-1 scores work well)
2. **Use weighted combinations** - some patterns are stronger indicators than others
3. **Consider text length** - normalize counts by document length
4. **Build pattern libraries** - maintain lists of common AI phrases, emoji patterns, etc.
5. **Use fuzzy matching** for slight variations of common phrases
6. **Count ratios** rather than absolute numbers (em-dashes per 100 words, etc.)
7. **Look for pattern clusters** - multiple weak signals together make a strong case

The regex/string matching approach will catch the most obvious AI-generated content, while the more sophisticated patterns in Part 2 require semantic analysis to detect effectively.
