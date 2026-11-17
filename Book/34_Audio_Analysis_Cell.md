# Chapter 34 - Audio Analysis Cell

Status: design contract. No implementation yet.

Last updated: 2026-09-03.

Decision owner: Kjetil. Drafted by Losen (Claude).

Machine-readable contract: `audio_analysis_cell_contract_v0.json`.

This chapter defines how HAVEN turns an audio file into knowledge without
turning a model's opinion into a fact. It exists because the first real request
was ordinary — *what does this song say, and what does it sound like* — and the
ordinary version of that request is where the dishonesty usually enters.

## 1. Core rule

**A measurement, an inference and an opinion are three different kinds of claim
and never share a field.**

Consider one piece of music. Three statements about it:

- 117.5 BPM
- uplifting
- sounds like a village brass band on a bright morning

The first is reproducible: hand the file and the tool version to a stranger and
they get 117.5 back. The second is a classifier assigning a label from some
vocabulary, with a confidence someone chose a threshold for. The third is a
language model writing a sentence.

Almost every audio pipeline flattens these into one object called `metadata`.
The consumer then cannot tell which is which, and the weakest claim inherits
the credibility of the strongest. That is the same failure Chapter 27 addresses
for text and Chapter 29 for arguments, and the same rule applies here: hide the
recipe, never the proof.

## 2. Provenance tiers

Every field in an emitted record carries a tier.

| Tier | What it is | Must carry | Confidence |
|---|---|---|---|
| `computed` | Deterministic DSP | tool, version, params | **never** |
| `inferred` | A model's label from a declared vocabulary | model, version, vocabulary | **required** |
| `model_opinion` | Free prose from a language model | model, version, prompt | **never** |
| `declared` | Owner-supplied or file tags, unverified | source | not applicable |

Two of these rules are counterintuitive and deliberate.

**A computed field never carries a confidence.** Attaching 0.94 to a duration
implies the duration might be something else. It might not. If a value is
uncertain, it is not computed; say which.

**An opinion never carries a confidence either.** A number on a sentence a
model wrote makes it look measured. It is not measured. It is a sentence.

## 3. Three layers

### 3.1 Signal — `computed`

`ffprobe`, `librosa`, `essentia`. Duration, codec, sample rate, channels,
tempo, key estimate, RMS and peak level, dynamics, spectral centroid, onset
density, segment boundaries.

This layer costs nothing, needs no provider, and is the only layer a third
party can check without trusting us. It should therefore always run, even when
the caller only asked for a transcript.

Three honesty requirements, each from a real way this layer misleads:

- **Tempo octave ambiguity.** Beat trackers routinely return half or double the
  perceived tempo. When the second autocorrelation peak is within 15 percent,
  emit `tempoOctaveAmbiguous` rather than a confident number.
- **Key is a correlation, not a reading.** Profile correlation confuses a major
  key with its relative minor. Always emit `keyCorrelation` alongside, and
  never present a key as settled below 0.8.
- **Ceiling limiting invalidates loudness comparison.** A peak at 0.0 dBFS means
  the file is squashed against the ceiling — common in generated audio. Emit
  `limitedAtCeiling` so nobody compares its loudness with anything.

### 3.2 Transcript — `inferred`

A transcript is model output. It never gets promoted to `computed`, however
precise its timestamps look; the alignment is computed *from* the model's
output and inherits its uncertainty.

Pipeline: optional source separation to isolate the vocal stem, speech-to-text
on the stem rather than the mix, optional diarization.

The separation step is not an optimisation. Speech-to-text models are trained
on speech, and singing is not speech. Running Whisper on a full mix with brass,
hand claps and whistling produces a transcript that looks fine and is wrong.
Separating the vocal first is what moves sung transcription from unusable to
usable, and the record states whether it was done.

An inaudible passage is emitted as `inaudible`. A guessed word inside quotation
marks is a fabricated quote, and the size of the guess does not change that.

### 3.3 Understanding — `inferred` or `model_opinion`

Mood, genre, instrumentation, arrangement.

Zero-shot taggers such as CLAP are preferred over trained taggers, for a reason
that is about honesty rather than accuracy: the caller supplies the label
vocabulary, so the taxonomy is explicit and owned rather than inherited from
whoever assembled someone else's training set. **A label without its vocabulary
is meaningless**, and the cell rejects one.

Prose from an audio-capable language model is `model_opinion` and is never
mined for structured fields. Extracting "cheerful" from a paragraph and filing
it as a mood tag launders an opinion into an inference.

No field in this layer is a property of the music. It is a property of a
model's response to the music, and the record says so.

## 4. The record

An analysis is addressed by the SHA-256 of the audio bytes. A re-encode is a
different subject, not a new version of the same one.

Every field has the same shape: value, tier, producer (tool or model, version,
params or prompt), confidence where the tier requires it, and a timestamp.

**A consumer may render a field only together with its tier.** A UI that shows
the value and hides the provenance is a contract violation, not a design
choice. This is the one rule that makes the rest worth having.

## 5. Agreement

Analysis is a service performed on the owner's material, so the external
template is narrow:

| Keypath | Grant | Semantics |
|---|---|---|
| `analysis` | `r---` | the typed record for one contentHash |
| `analyze` | `-w--` | action; audio must already be owner material |
| `vocabulary` | `r---` | label vocabularies this cell will tag against |

Never granted: the raw audio bytes, other entities' analyses, provider
credentials, or caller-chosen models and endpoints.

The `analyze` action refuses an externally supplied URL. A caller who can name
the bytes to be fetched can use the cell as a fetcher, and the cell would then
be sending arbitrary internet content to paid providers under the owner's
purpose.

## 6. Privacy

Audio is among the most revealing material a person holds, and it routinely
contains people who never agreed to be analysed.

- The record stores derived fields. It never stores the audio.
- A transcript of a recording with identifiable third parties is their data
  too. Diarization labels stay speaker-relative — `Speaker 1` — and this cell
  never resolves a speaker to a person.
- Every provider the bytes were sent to is named in the record. A provider call
  without a declared purpose covering it does not happen.
- Retention follows purpose. An analysis outlives neither the audio nor the
  purpose that justified it.

## 7. Operational notes

NanoGPT's direct upload stops at 3 MB; above that, use `audioUrl` or downmix
with `ffmpeg -ac 1 -b:a 64k` first. The record states which path was used,
because it affects transcript quality and a later reader deserves to know.

Provider pricing is per minute, so cost is fully predictable from
`durationSeconds` before any call. For long material, tell the owner the price
first.

## 8. Worked example

The first file this contract was written against: a 2:52 brass-band march,
generated audio, 192 kbit stereo MP3.

Layer 1 returned 117.5 BPM, key correlation 0.767 on B-flat major, peak at
0.0 dBFS, dynamics 13.0 dB, six segments. Under this contract that record says:
tempo computed with a stated ambiguity flag; key computed but **not settled**,
since 0.767 is below the threshold; loudness computed but flagged
`limitedAtCeiling`; and no mood field at all, because no vocabulary was
supplied and the cell refuses to invent one.

That is the whole point of the chapter. The honest record is less satisfying
than the one most tools would emit, and it is the one that will still be true
next year.

## 9. Open questions

1. Does an analysis inherit the audio's Agreement, or hold its own? Inheriting
   is simpler and keeps revocation aligned. Holding its own allows sharing a
   mood tag without sharing the recording.
2. Should `model_opinion` prose be stored at all, or generated on demand and
   never persisted? Storing it makes an unverifiable sentence durable, which is
   what the tiering exists to discourage.
3. Should cheap computed fields be re-derived on read rather than stored, since
   tool versions change and a stored value silently ages?
