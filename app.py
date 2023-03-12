import gradio as gr
import re
import glob
from openbb_terminal.forecast.whisper_model import transcribe_and_summarize

def get_video_id(url):
    video_id = re.findall(r"v=([-\w]{11})", url)[0]
    # make folder to store output files
    # extract video ID from URL using regular expression
    transcribe_and_summarize(video=url, output_dir=video_id)
    # return files from video_id folder
    # find file with video_id/*_summary.txt
    summary_file = glob.glob(f"{video_id}/*_summary.txt")[0]
    # file .srt file
    subtitle_file = glob.glob(f"{video_id}/*.srt")[0] or glob.glob(f"{video_id}/*.vtt")[0]
    return summary_file, subtitle_file

input_text = gr.inputs.Textbox(label="Enter a YouTube URL")
output_text = [gr.outputs.Textbox(label="Summary File"), gr.outputs.Textbox(label="Subtitle File")]

gr.Interface(fn=get_video_id, inputs=input_text, outputs=output_text, title="YouTube Video ID Finder").launch()