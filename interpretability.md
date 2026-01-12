# Peeking Inside the Black Box: How Transcoders Help Us Understand What Language Models Are Actually Thinking

Large language models have gotten frighteningly good at tasks we once thought required human intelligence. They write essays, solve math problems, translate languages, and even reason through complex questions. But here's the unsettling part: we don't really know *how* they do it.

When GPT-4 correctly answers "What is the capital of the state containing Dallas?", it outputs "Austin" almost instantly. But what happened in between? Did it first recognize Dallas as a city? Did it then figure out which state Dallas is in? Did it retrieve the capital from some internal knowledge store? We're essentially flying blind, trusting billion-parameter black boxes to make increasingly important decisions without understanding their internal logic.

This isn't just an academic curiosity. If we can't understand how these models think, we can't predict when they'll fail, we can't fix their biases, and we can't ensure they're safe as they become more powerful. This is the problem of **mechanistic interpretability**—understanding the actual algorithms and computations happening inside neural networks.

## The Problem: Dense, Entangled Representations

To understand why LLMs are so hard to interpret, you need to know what happens when you feed text into one.

When a language model processes the word "cat," it doesn't just store a simple label. Instead, it creates an **activation vector**—a list of maybe 4,096 numbers that represents everything the model "knows" about that token at that moment. In layer 3, this vector might encode basic features like "this is a noun" or "it's a living thing." By layer 10, it might encode more abstract concepts like "typically a pet" or "subject of this sentence."

The problem is that these vectors are **dense** and **entangled**. Dense means most of the 4,096 numbers are non-zero—there's information smeared across the entire vector. Entangled means multiple concepts are mixed together in the same dimensions. Dimension 237 might be partially about animals, partially about sentence subjects, and partially about something we can't even name.

Think of it like trying to understand a painting by analyzing the chemical composition of the paint. Sure, the information is technically there, but it's all mixed together in a way that makes individual concepts impossible to isolate.

This is where transcoders come in.

## Enter Transcoders: Unpacking the Mess

A transcoder is essentially a translation device. It takes those messy, dense activation vectors and converts them into something humans can actually understand: a **sparse representation** where only a handful of dimensions are active at once, and each dimension corresponds to a clear, interpretable concept.

The key insight is sparsity. If you force a representation to be sparse—where most dimensions are zero and only 5-20 are active—something magical happens. The model naturally learns to separate concepts into different dimensions. Instead of dimension 237 being a confusing mix of animals, subjects, and mystery features, you get:
- Dimension 8472: "mentions of animals"  
- Dimension 1293: "grammatical subjects"
- Dimension 6891: "past tense verbs"

It's like taking that mixed palette of paint and separating it back into individual tubes. Suddenly you can see exactly which colors—which concepts—the model is using.

## The Architecture: How Transcoders Work

At its core, a transcoder is a type of **sparse autoencoder**. Here's the structure:

You start with an activation vector from the language model—let's say it's 4,096 dimensions. The transcoder has two parts:

**The Encoder** takes that 4,096-dimensional vector and expands it into a much larger space—maybe 32,768 dimensions. This expansion is crucial. You need more dimensions to represent concepts sparsely. After the expansion, it applies a ReLU activation function, which naturally creates sparsity by outputting exactly zero for negative values.

**The Decoder** takes that sparse 32,768-dimensional representation and compresses it back down to the original 4,096 dimensions, trying to reconstruct the original activation as accurately as possible.

During training, the transcoder is trying to accomplish two competing goals:
1. Reconstruct the original activation accurately (minimize reconstruction error)
2. Use as few dimensions as possible (maximize sparsity)

The tension between these goals forces the transcoder to discover the most efficient sparse representation—and it turns out that the most efficient way to sparsely represent information is to dedicate each dimension to a coherent, reusable concept.

## Training: Teaching the Transcoder

Training a transcoder happens *after* you've already trained your language model. Here's the process:

First, you run a large corpus of text through your LLM—maybe millions of sentences—and collect activation vectors from a specific layer you want to understand. These become your training data.

Then you train the transcoder using a loss function that combines two terms:
- **Reconstruction loss**: How accurately can you recreate the original activation? (measured with mean squared error)
- **Sparsity penalty**: How many dimensions are you using? (measured with L1 regularization)

The L1 penalty is key. It adds up the absolute values of all activations and penalizes the model for using more dimensions. This creates constant pressure to zero out unnecessary dimensions.

There's a hyperparameter λ (lambda) that controls the tradeoff. Higher λ means sparser representations but potentially worse reconstruction. Lower λ means better reconstruction but less interpretable features. Finding the right balance is part of the art.

What emerges after training is remarkable. Without being explicitly told what concepts exist, the transcoder discovers interpretable features that the language model is actually computing. Researchers have found features for specific entities (like "Golden Gate Bridge"), grammatical patterns (like "plural nouns"), abstract concepts (like "sarcasm"), and even things like "text that appears to be base64 encoded."

## Understanding What Features Mean

Here's where things get interesting, and a bit manual. After training, you have a transcoder with, say, 32,768 dimensions. But dimension 8472 is just a number—it doesn't come with a label that says "French cities."

So how do we figure out what each dimension represents?

The process is empirical detective work. For each dimension, you:

1. **Collect activations**: Run lots of text through your model and record when this dimension activates strongly.

2. **Find maximally activating examples**: Sort all your examples by activation strength and look at the top ones.

For example, dimension 8472's top activations might be:
- "...visiting Toulouse this summer..."
- "...Nice is on the Mediterranean..."  
- "...Lyon's cuisine is famous..."
- "...the streets of Bordeaux..."

3. **Human interpretation**: A researcher looks at these and thinks, "Oh, these are all French cities!" That label—"French cities"—is just shorthand based on empirical observation.

4. **Validation**: Test whether it activates on *all* French cities and *only* on French cities. Check edge cases.

To scale this up, researchers use automation. They might feed the top activating examples to another LLM (like GPT-4) and ask, "What do these snippets have in common?" Or they use statistical methods to find distinguishing features.

The crucial point: the dimension doesn't "know" it represents French cities. We discovered that by observing its behavior. The sparsity constraint during training just happened to create features that correspond to human-interpretable concepts.

## Cross-Layer Transcoders: Tracking Information Flow

Standard transcoders tell you what features exist at a single layer. But they don't tell you how information flows through the network—how concepts transform as they're processed from layer to layer.

This is where **cross-layer transcoders** come in. Instead of mapping Layer 5 → Sparse features → Layer 5, they map Layer 5 → Sparse features → Layer 8.

The architecture is similar, but now you're training the transcoder to:
- Encode Layer 5 activations into sparse features
- Decode those features to *predict* Layer 8 activations

If your sparse features are meaningful, they should be able to predict what happens in later layers. What emerges are features that represent **computational steps** rather than just static patterns.

For example, you might discover a feature in Layer 3 that predicts "entity resolution" happening in Layer 7. Or a feature that tracks how "detecting a city name" in Layer 5 becomes "retrieving the associated country" in Layer 10.

Cross-layer transcoders reveal the algorithm the model implements, not just what it represents. They show you the causal chain of computations.

## Building Computational Graphs: The Real Magic

This is where everything comes together. Once you have interpretable sparse features, you can start building **computational circuits**—graphs that show exactly how the model computed its answer.

Let's say you ask the model: "The capital of the state containing Dallas is ___" and it answers "Austin." How did it get there?

The technique is called **activation patching** or **causal intervention**. Here's how it works:

1. **Run the prompt normally** and identify which sparse features activate at each layer:
   - Layer 5: "Dallas" feature activates
   - Layer 8: "Texas" feature activates
   - Layer 10: "US state capitals" feature activates
   - Layer 12: "Austin" feature activates

2. **Test causality by ablation**: Knock out the "Dallas" feature (set it to zero) and run the model again. Does it still output "Austin"? No! This means the "Dallas" feature is causally necessary.

3. **Test connections between features**: Knock out "Dallas" and check if "Texas" still activates. It doesn't! Draw an arrow: Dallas → Texas. Knock out "Texas" and check if "state capitals" still activates. It weakens significantly. Draw an arrow: Texas → state capitals.

4. **Build the graph iteratively**: Test every pair of features across layers. If ablating feature A reduces feature B, you've found a causal connection.

The result is a beautiful computational circuit showing:
```
"Dallas" (city recognition)
    ↓
"Texas" (geographic reasoning)
    ↓
"state capitals" (task understanding)
    ↓
"Austin" (fact retrieval)
```

This isn't speculation—it's empirical evidence of the algorithm the model is running.

Cross-layer transcoders make this easier because they directly reveal what computations transform concepts across layers, giving you a head start on finding the important connections.

## Why This Matters

Understanding these circuits has profound implications:

**Safety**: If we know which features activate when a model generates harmful content, we can potentially intervene or detect problems before they happen.

**Reliability**: We can identify when models are using flawed reasoning paths and correct them, rather than just hoping they work.

**Debugging**: When a model fails, we can trace exactly where in the circuit the computation went wrong.

**Alignment**: We can verify that models are actually optimizing for what we want them to optimize for, not some proxy.

**Scientific understanding**: We're reverse-engineering one of the most complex computational systems humans have ever created. The insights might tell us something fundamental about intelligence itself.

## Running the Experiment: Why DistilGPT-2?

If you want to try this yourself, you face a practical question: which model should you use?

The temptation is to go big—analyze GPT-4 or Claude to find the most impressive circuits. But there's a problem: you need to collect millions of activation vectors and train transcoders for hours or days. Bigger models mean longer experiments, more memory, and higher costs.

This is where **DistilGPT-2** shines. It's a distilled version of GPT-2 with 82 million parameters—small enough to experiment with on a single GPU, but large enough to have learned real factual knowledge.

DistilGPT-2 was trained on diverse internet text, including Wikipedia. It actually knows facts like "Dallas is in Texas" and "Austin is the capital of Texas." This means you can test factual reasoning circuits, not just grammar patterns.

The hidden dimension is 768, which is manageable. You can expand to 6,144 dimensions (8x expansion) for your sparse representation and train a transcoder in a few hours. Compare this to a model like GPT-4 where you don't even have access to the internal activations.

Other small models like TinyStories are great for learning the methodology, but they're trained on simple fictional narratives. They won't know that Dallas is in Texas. You need a model trained on factual data to discover factual reasoning circuits.

DistilGPT-2 hits the sweet spot: small enough to iterate quickly, large enough to be interesting, and accessible enough that anyone with a decent laptop can start exploring.

## The Full Pipeline

Here's what the complete process looks like:

**Phase 1**: Load your pre-trained DistilGPT-2 model. No need to train it yourself—just download it from HuggingFace.

**Phase 2**: Collect activations. Run thousands of text examples through the model and extract activation vectors from your target layer (maybe layer 4 or 5, somewhere in the middle). Save these vectors.

**Phase 3**: Train your transcoder on those saved activations. The transcoder learns to encode/decode them sparsely. This takes a few hours.

**Phase 4**: Interpret features. For each sparse dimension, find examples where it activates strongly and figure out what it represents. This is the detective work.

**Phase 5**: Build circuits. Use activation patching to test causal relationships between features and construct computational graphs for specific prompts.

The beauty is that most of the work happens after model training. You're not training a new LLM from scratch—you're analyzing an existing one.

## What You'll Discover

Even on a small model like DistilGPT-2, you'll find fascinating features:

You'll discover dimensions that activate for specific types of words (articles, prepositions, punctuation). You'll find dimensions for grammatical patterns (past tense, plural nouns, possessive forms). You'll find dimensions for semantic categories (US states, European cities, colors, animals).

And then you'll find weird ones. Dimensions that activate for Python code. Dimensions that activate when text is in all caps. Dimensions that seem to detect when the model is uncertain.

When you build circuits, you'll see how these features chain together. How the model recognizes "Dallas," infers "Texas," understands the task requires a capital city, and retrieves "Austin." You'll see the algorithm unfold step by step.

It's not perfect. Many dimensions will be hard to interpret. Some will be polysemantic (meaning multiple unrelated things). Some circuits will be incomplete. But you'll get glimpses of the computational machinery that seemed like pure magic before.

## The Frontier

This field is exploding right now. Anthropic recently released an analysis of Claude 3 Sonnet where they found millions of interpretable features using this technique. They discovered features for specific people (like "Golden Gate Bridge"), abstract concepts (like "secrecy"), and even features for bugs in code.

But we're still in the early stages. Most of what language models do remains mysterious. We can identify individual features and small circuits, but we don't understand how they compose into the full system. We can't yet predict what new capabilities will emerge or what failure modes are lurking in unexplored regions of the network.

The tools are getting better. Transcoders are just one technique in a growing toolkit that includes attention pattern analysis, logit lens methods, and causal tracing. Each gives us a different lens on the internal workings.

What's exciting is that you don't need to work at a big AI lab to contribute. The models are available, the techniques are published, and the compute requirements are modest. Anyone with curiosity and a GPU can start pulling back the curtain on these remarkable, mysterious systems.

## Why You Should Care

Even if you never run these experiments yourself, the implications touch everyone. Language models are being integrated into search engines, coding assistants, medical diagnosis tools, and legal analysis systems. They're helping make decisions that affect real lives.

Right now, we're trusting these systems without really understanding them. It's like building a bridge using a revolutionary new material without understanding its structural properties. Maybe it holds up fine. Or maybe there are failure modes we haven't discovered yet.

Mechanistic interpretability is our best hope for opening the black box. Transcoders and sparse autoencoders are showing us that these models aren't incomprehensible—they're just compressed. With the right tools, we can unpack them, understand them, and maybe even improve them.

The alternative is flying blind into an increasingly AI-driven future, hoping these systems work as intended without any way to verify it. I don't know about you, but I'd rather turn on the lights.

---

*In a follow-up post, I'll share the complete code to run this experiment yourself on DistilGPT-2, from activation collection through circuit discovery. You'll be able to peer inside a language model and see its thoughts unfold. Stay tuned.*
