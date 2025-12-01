import streamlit as st
import os
import sys
import asyncio

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.services.extractor import download_datasets
from backend.services.normalizer import normalize_transcripts
from backend.services.audio_handler import organize_audio
from backend.services.converter import extract_metadata, convert_to_jsonl
from backend.services.export import export_data

st.title("Qur'an Recitation Dataset Curator")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Process Data", "View Data"])

if page == "Process Data":
    st.header("Full Pipeline (Auto)")
    st.info(
        "**Run Full Pipeline**: Automatically downloads the Quran dataset from Kaggle, normalizes transcripts, organizes audio, extracts metadata, and converts to JSONL. No manual inputs needed."
    )
    if st.button("Run Full Pipeline"):
        with st.spinner("Running full pipeline..."):
            try:
                # Step 1: Download (assume Kaggle URL)
                sources = [
                    "https://www.kaggle.com/datasets/imrankhan197/the-quran-dataset"
                ]
                files = asyncio.run(download_datasets(sources))
                st.write(f"Downloaded: {files}")

                # Step 2: Normalize (auto-detect)
                raw_dir = "data/raw"
                if os.path.exists(raw_dir):
                    text_files = [
                        os.path.join(raw_dir, f)
                        for f in os.listdir(raw_dir)
                        if f.endswith((".txt", ".csv"))
                    ]
                    st.write(f"Found text files: {text_files}")
                    if text_files:
                        normalized = asyncio.run(normalize_transcripts(text_files))
                        st.write(f"Normalized: {normalized}")

                        # Check processed transcripts
                        processed_transcripts = "data/processed/transcripts"
                        if os.path.exists(processed_transcripts):
                            processed_files = os.listdir(processed_transcripts)
                            st.write(f"Processed transcripts: {processed_files}")

                        # Step 3: Organize Audio
                        organized_dir = asyncio.run(organize_audio(raw_dir))
                        st.write(f"Audio organized: {organized_dir}")

                        # Step 4: Extract Metadata
                        processed_audio = "data/processed/audio"
                        default_files = []
                        if os.path.exists(processed_audio):
                            default_files.extend(
                                [
                                    os.path.join(processed_audio, f)
                                    for f in os.listdir(processed_audio)
                                    if f.endswith(".wav")
                                ]
                            )
                        if os.path.exists(processed_transcripts):
                            default_files.extend(
                                [
                                    os.path.join(processed_transcripts, f)
                                    for f in os.listdir(processed_transcripts)
                                    if f.endswith((".txt", ".csv"))
                                ]
                            )
                        st.write(f"Files for metadata: {default_files}")
                        if default_files:
                            metadata_path = asyncio.run(extract_metadata(default_files))
                            st.write(f"Metadata extracted: {metadata_path}")

                            # Check metadata content
                            import json

                            if os.path.exists(metadata_path):
                                with open(metadata_path, "r", encoding="utf-8") as f:
                                    metadata = json.load(f)
                                st.write(f"Metadata entries: {len(metadata)}")

                            # Step 5: Convert to JSONL
                            jsonl_path = asyncio.run(
                                convert_to_jsonl(metadata_path, processed_audio)
                            )
                            st.write(f"JSONL created: {jsonl_path}")

                            st.success("Full pipeline completed!")
                        else:
                            st.error("No processed files found for metadata extraction")
                    else:
                        st.error("No text files found to normalize")
                else:
                    st.error("Raw data directory not found")
            except Exception as e:
                st.error(f"Pipeline failed: {e}")

    st.info(
        "**Manual Download**: Choose a predefined dataset or enter custom URLs to download. Supports Kaggle and general links. No auto-detection of new datasets; manually add URLs."
    )
    st.header("Manual Download")
    dataset_options = {
        "Quran Dataset (Kaggle)": "https://www.kaggle.com/datasets/imrankhan197/the-quran-dataset",
        "Custom URLs": "custom",
    }
    selected_dataset = st.selectbox(
        "Select Dataset", list(dataset_options.keys()), key="manual_dataset"
    )
    if selected_dataset == "Custom URLs":
        sources = st.text_area(
            "Enter dataset URLs (one per line)", "", key="manual_sources"
        )
    else:
        sources = dataset_options[selected_dataset]
        st.write(f"Selected: {sources}")

    if st.button("Download Datasets", key="manual_download"):
        if sources:
            if isinstance(sources, str) and not sources.startswith("http"):
                source_list = sources.split("\n")
            else:
                source_list = (
                    [sources] if isinstance(sources, str) else sources.split("\n")
                )
            try:
                files = asyncio.run(download_datasets(source_list))
                st.success("Datasets downloaded successfully!")
                st.json({"status": "success", "files": files})
            except Exception as e:
                st.error(f"Download failed: {e}")

    st.header("Manual Steps")
    # Normalize, Organize, etc. as before

elif page == "View Data":
    st.header("View and Filter Data")
    st.info(
        "**View Data**: Browse and filter processed files. Raw: downloaded originals; Transcripts: cleaned text; Audio: generated sounds; JSONL: AI-ready format."
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Raw Data", "Transcripts", "Audio", "JSONL"])

    with tab1:
        st.subheader("Raw Data Files")
        raw_dir = "data/raw"
        if os.path.exists(raw_dir):
            raw_files = [
                f
                for f in os.listdir(raw_dir)
                if os.path.isfile(os.path.join(raw_dir, f))
            ]
            if raw_files:
                filter_name = st.text_input("Filter by name", "", key="raw_filter")
                filtered_files = (
                    [f for f in raw_files if filter_name.lower() in f.lower()]
                    if filter_name
                    else raw_files
                )
                selected_raw = st.selectbox(
                    "Select raw file", filtered_files, key="raw_select"
                )
                if selected_raw:
                    file_path = os.path.join(raw_dir, selected_raw)
                    file_size = os.path.getsize(file_path)
                    st.write(f"File size: {file_size} bytes")
                    if selected_raw.endswith(".txt") or selected_raw.endswith(".csv"):
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()[:1000]  # First 1000 chars
                        st.text_area("File Content Preview", content, height=300)
                    else:
                        st.info("Binary file, cannot preview.")
            else:
                st.info("No raw files found.")
        else:
            st.info("Raw data directory not found.")

    with tab2:
        st.subheader("Processed Transcripts")
        transcript_dir = "data/processed/transcripts"
        if os.path.exists(transcript_dir):
            transcript_files = [
                f for f in os.listdir(transcript_dir) if f.endswith(".txt")
            ]
            if transcript_files:
                filter_name = st.text_input(
                    "Filter by name", "", key="transcript_filter"
                )
                filtered_files = (
                    [f for f in transcript_files if filter_name.lower() in f.lower()]
                    if filter_name
                    else transcript_files
                )
                selected_transcript = st.selectbox(
                    "Select transcript file", filtered_files, key="transcript_select"
                )
                if selected_transcript:
                    with open(
                        os.path.join(transcript_dir, selected_transcript),
                        "r",
                        encoding="utf-8",
                    ) as f:
                        content = f.read()
                    st.write(f"File size: {len(content)} characters")
                    if content:
                        st.text_area("Transcript Content", content[:1000], height=300)
                        if len(content) > 1000:
                            st.info("Showing first 1000 characters. File is larger.")
                    else:
                        st.warning("File is empty.")
            else:
                st.info("No processed transcripts found.")
        else:
            st.info("Processed transcripts directory not found.")

    with tab3:
        st.subheader("Generated Audio Files")
        audio_dir = "data/processed/audio"
        if os.path.exists(audio_dir):
            audio_files = [
                f
                for f in os.listdir(audio_dir)
                if f.endswith(".wav") or f.endswith(".mp3")
            ]
            if audio_files:
                filter_name = st.text_input("Filter by name", "", key="audio_filter")
                filtered_files = (
                    [f for f in audio_files if filter_name.lower() in f.lower()]
                    if filter_name
                    else audio_files
                )
                selected_audio = st.selectbox(
                    "Select audio file", filtered_files, key="audio_select"
                )
                if selected_audio:
                    audio_path = os.path.join(audio_dir, selected_audio)
                    st.audio(
                        audio_path,
                        format="audio/mp3",  # gTTS generates MP3
                    )
                    file_size = os.path.getsize(audio_path)
                    st.write(f"File size: {file_size} bytes")
                    # Try to get duration
                    try:
                        if selected_audio.endswith(".mp3"):
                            from mutagen.mp3 import MP3

                            audio = MP3(audio_path)
                            duration = audio.info.length
                        elif selected_audio.endswith(".wav"):
                            import wave

                            with wave.open(audio_path, "rb") as wav:
                                frames = wav.getnframes()
                                rate = wav.getframerate()
                                duration = frames / float(rate)
                        else:
                            duration = None
                        if duration:
                            st.write(f"Duration: {duration:.2f} seconds")
                        else:
                            st.write("Duration: Unable to determine")
                    except Exception as e:
                        st.write(f"Duration: Unable to determine ({e})")
            else:
                st.info("No audio files found.")
        else:
            st.info("Processed audio directory not found.")

    with tab4:
        st.subheader("JSONL Dataset Preview")
        jsonl_path = "data/processed/dataset.jsonl"
        if os.path.exists(jsonl_path):
            with open(jsonl_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            total_lines = len(lines)
            st.write(f"Total entries: {total_lines}")
            if total_lines > 0:
                try:
                    import json

                    first_entry = json.loads(lines[0])
                    st.json(first_entry)  # Show parsed JSON
                except json.JSONDecodeError:
                    st.text_area("JSONL Preview", lines[0][:500], height=300)
            else:
                st.info("No entries in JSONL.")
        else:
            st.info("JSONL file not found.")

st.header("Export Data")
st.info(
    "**Export Data**: Download all processed files (transcripts, audio, JSONL) as a ZIP for sharing or backup."
)
export_path = st.text_input("Export ZIP path", "quran_dataset.zip")
if st.button("Export Processed Data as ZIP"):
    zip_file = export_data(export_path)
    if zip_file and os.path.exists(zip_file):
        with open(zip_file, "rb") as f:
            st.download_button("Download ZIP", f, file_name=export_path)
        st.success(f"Data exported to {zip_file}")
    else:
        st.error("Export failed")
