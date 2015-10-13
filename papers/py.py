from subprocess import call
import os

l = os.path.join(os.path.dirname(__file__), '..', 'media/uploads/')
l = l+'TraceAnalyser.pdf'
call(['pdftotext',l])
print os.path.join(os.path.dirname(__file__), 'templates')
