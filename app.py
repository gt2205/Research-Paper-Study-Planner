import pdfplumber
from groq import Groq
import os
def extract_text_from_pdf(pdf_file,api):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            content=page.extract_text() + "\n"
            client = Groq(api_key=api,)
            chat_completion=client.chat.completions.create(
            messages=[{"role": "system", "content": "Summarize the page and mainly keep the headings and topic names intact in the short summary."},
                      {"role": "user","content": "Summarize and mainly keep the heading and name of topics in summary:"+content,}],
            model="llama3-8b-8192",
            )
            text += chat_completion.choices[0].message.content
    return text


from groq import Groq
import os
def study_planner(days, file,api):
    if file is None:
        return "Please upload a valid timetable file."

    try:
        study_material = extract_text_from_pdf(file.name,api)

        client = Groq(api_key=api,)

        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "Provided a research paper,you have to output a study plan to cover the topics in the paper in provided number of days.Also at last give a motivational quote on studying."},
                      {"role": "user","content": "The research paper is:" +study_material+" Now prepare a study plan to cover this in "+days+" days.Give the plan topic wise and can also include some important prerequisites for the paper.Also give a motivational quote at last.",}],
            model="llama3-70b-8192",
            )
        study_plan = chat_completion.choices[0].message.content
        """pdf_path = text_to_pdf(study_plan)"""
        return study_plan
    except Exception as e:
        return f"An error occurred while processing the file: {str(e)}"


import gradio as gr
demo = gr.Interface(
    fn=study_planner,
    inputs=[gr.Textbox(label="Enter the number of days"), gr.File(label="Upload the research paper (PDF)"),gr.Textbox(label="Groq API Key")],
    outputs=gr.Textbox(label="Optimum study plan"),
    title="Research Paper Study Planner",
    description="Upload the research paper and input the number of days to get a study plan"
)

demo.launch(share="True")
