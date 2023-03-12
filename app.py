import gradio as gr
import re
import sys
import glob
import os
from io import StringIO
from openbb_terminal.forecast.whisper_model import transcribe_and_summarize


def get_video_id(url):

    video_id = re.findall(r"v=([\w]{11})", url)[0]
    old_stdin = sys.stdin
    # mkdir /home/user/.cache/whisper
    os.makedirs(f"/home/user/.cache/whisper", exist_ok=True)
    if not sys.stdin.isatty():
        y_strings = "\n".join(["y", "y", "y", "y", "y"])
        sys.stdin = StringIO(y_strings)
        transcribe_and_summarize(video=url, output_dir=video_id)
    else:
        return "Please enter a YouTube URL"
    sys.stdin = old_stdin
    print(f"Video ID: {video_id}")
    try:
        summary_file = glob.glob(f"{video_id}/*_summary.txt")[0]
    except Exception as e:
        # get latest file with *_summary.txt
        summary_file = max(glob.glob(f"**/*_summary.txt"), key=os.path.getctime)
    # file .srt file
    subtitle_file = None
    try:
        subtitle_file = glob.glob(f"{video_id}/*.vtt")[0]
    except Exception as e:
        # get latest file with .srt or .vtt
        subtitle_file = max(glob.glob(f"**/*.vtt"), key=os.path.getctime)

    if subtitle_file is None:
        try:
            subtitle_file = glob.glob(f"{video_id}/*.srt")[0]
        except Exception as e:
            subtitle_file = max(glob.glob(f"**/*.srt"), key=os.path.getctime)
    return summary_file, subtitle_file

input_text = gr.inputs.Textbox(label="Enter a YouTube URL")
output_text = [gr.outputs.Textbox(label="Summary File"), gr.outputs.Textbox(label="Subtitle File")]

gr.Interface(fn=get_video_id, inputs=input_text, outputs=output_text, title="YouTube Video ID Finder").launch()