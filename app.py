import gradio as gr
import re
import sys
import glob
from io import StringIO
from openbb_terminal.forecast.whisper_model import transcribe_and_summarize


def get_video_id(url):

    video_id = re.findall(r"v=([-\w]{11})", url)[0]
    old_stdin = sys.stdin
    if not sys.stdin.isatty():
        y_strings = "\n".join(["y", "y", "y", "y", "y"])
        sys.stdin = StringIO(y_strings)
        transcribe_and_summarize(video=url, output_dir=video_id)
    else:
        return "Please enter a YouTube URL"
    sys.stdin = old_stdin
    summary_file = glob.glob(f"{video_id}/*_summary.txt")[0]
    # file .srt file
    subtitle_file = glob.glob(f"{video_id}/*.srt")[0] or glob.glob(f"{video_id}/*.vtt")[0]
    return summary_file, subtitle_file

input_text = gr.inputs.Textbox(label="Enter a YouTube URL")
output_text = [gr.outputs.Textbox(label="Summary File"), gr.outputs.Textbox(label="Subtitle File")]

gr.Interface(fn=get_video_id, inputs=input_text, outputs=output_text, title="YouTube Video ID Finder").launch()