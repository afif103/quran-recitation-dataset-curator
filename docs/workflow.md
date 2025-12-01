# Workflow Guide

## Step 1: Research and Download Datasets
- Find Qur'an recitation datasets on HuggingFace (e.g., search for "quran recitation") and Kaggle.
- Use the frontend to enter URLs and download.

## Step 2: Normalize Transcripts
- Provide paths to transcript files.
- The system normalizes to Uthmani script, removes non-canonical variants.

## Step 3: Organize Audio
- Input raw audio directory.
- Files are organized into reciter/surah/ayah.wav structure.

## Step 4: Extract Metadata
- Input file paths.
- Extracts reciter, surah, ayah, duration, etc.

## Step 5: Convert to JSONL
- Uses metadata and audio paths to create dataset.jsonl.

## Deliverables
- dataset.jsonl: Unified training format
- sources.txt: List of sources
- Organized audio and transcripts
- metadata.json

## Assumptions
- Audio files named as reciter_surah_ayah.wav
- Transcripts in UTF-8
- Uthmani reference for validation (to be added)