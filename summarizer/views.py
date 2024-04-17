from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .forms import DocumentForm
from PyPDF2 import PdfReader
from transformers import BartTokenizer, BartForConditionalGeneration
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

def summary_page(request):
    summary = request.GET.get('summary', '')
    return render(request, 'summarizer/summary.html', {'summary': summary})

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document_type = form.cleaned_data['document_type']
            document = request.FILES.get('document')

            
            if document_type == 'pdf' and document is not None:
                text = extract_text_from_pdf(document)
                if text:
                    summary = hugging_face_summarization(text)
                    return render(request, 'summarizer/summary.html', {'summary': summary})
                else:
                    return HttpResponse('Uploaded PDF is empty')
            elif document_type == 'youtube':
                youtube_url = form.cleaned_data['youtube_url']
                summary = summarize_youtube_video(youtube_url)
                if summary:
                    return render(request, 'summarizer/summary.html', {'summary': summary})
                else:
                    return HttpResponse('Failed to generate summary for the YouTube video')
            else:
                return HttpResponse('No file uploaded or invalid document type')
        else:
            return render(request, 'summarizer/upload.html', {'form': form})
    else:
        form = DocumentForm()
        return render(request, 'summarizer/upload.html', {'form': form})

class SummarizerView(View):
    def get(self, request):
        form = DocumentForm()
        return render(request, 'summarizer/upload.html', {'form': form})

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document_type = form.cleaned_data['document_type']
            document = request.FILES.get('document')
            if document_type == 'pdf' and document is not None:
                text = extract_text_from_pdf(document)
                if text:
                    summary = hugging_face_summarization(text)
                    return render(request, 'summarizer/summary.html', {'summary': summary})
                else:
                    return HttpResponse('Uploaded PDF is empty')
            elif document_type == 'youtube':
                youtube_url = form.cleaned_data['youtube_url']
                summary = summarize_youtube_video(youtube_url)
                if summary:
                    return render(request, 'summarizer/summary.html', {'summary': summary})
                else:
                    return HttpResponse('Failed to generate summary for the YouTube video')
            else:
                return HttpResponse('No file uploaded or invalid document type')
        else:
            return render(request, 'summarizer/upload.html', {'form': form})

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print("Error extracting text from PDF:", e)
        return None

def hugging_face_summarization(text):
    try:
        model_name = "facebook/bart-large-cnn"
        tokenizer = BartTokenizer.from_pretrained(model_name)
        model = BartForConditionalGeneration.from_pretrained(model_name)

        inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
        summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=2000, min_length=200, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        print("Error generating summary:", e)
        return None

def summarize_youtube_video(youtube_url):
    try:
        video_id = youtube_url.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        result = ' '.join([i['text'] for i in transcript])
        summary = hugging_face_summarization(result)
        return summary
    except Exception as e:
        print("Error summarizing YouTube video:", e)
        return None