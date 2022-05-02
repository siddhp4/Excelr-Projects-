import streamlit as st
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pdfplumber
import text2emotion as te
nlp = spacy.load('en_core_web_sm')

def txt(file):
    with open('C:/Users/Computer/Documents/book-war-and-peace.txt', 'r') as file:
    txt = file.readlines()

chap_name = ""
content = {}

# parsing the opened file into a dictionary, where "key" = Chapter Name and "value" = Contents of chapter.
for line in txt :
    if "CHAPTER" in line:
#         print line,
        chap_name = line.strip()
        content[chap_name] = chap_name
    else:
        content[chap_name] = content[chap_name] + line


# for key, value in content.iteritems() :
#     print key, value

# Testing the parsing works as expected.
print (len(content))

print (content['CHAPTER I'])
return text

def callback():
    st.session_state.button_clicked =True
    
def summary(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation) and words whose length is less than 2 characters - removes <br/a> formating from data 
    for token in tokens:
        if re.search('[a-zA-Z]', token) and len(token) > 2 and token not in stop_words :
            filtered_tokens.append(token)
            print (type(df.ChapterContent[0]))

chapter_count = 0
for text in df['ChapterContent']:
    # Display the generated Chapterwise summary:
    print ('Summary:%s' % df['ChapterName'][chapter_count])
    summary = summarize(df.ChapterContent[chapter_count]) 
    print (summarize(df.ChapterContent[chapter_count]))
    print
    print ("Length of original text %d, length of summary %d characters." % (len(df['ChapterContent'][chapter_count]), len(summary)))
    print
    chapter_count = chapter_count + 1
    return sumy



def analysis(text):
    vader_analyzer = SentimentIntensityAnalyzer()

sentiments = []
for text in txt[:10]:
    for sent in nltk.sent_tokenize(text):
        print (sent)
        print(vader_analyzer.polarity_scores(sent))
        sent_dic = vader_analyzer.polarity_scores(sent)
        sent_dic["sentence"] = sent
        sentiments.append(sent_dic)

df_sentiments = pd.DataFrame.from_records(sentiments)

df_sentiments['label'] = 0
df_sentiments.loc[df_sentiments['compound'] > 0.2, 'label'] = 1
df_sentiments.loc[df_sentiments['compound'] < -0.2, 'label'] = -1
df_sentiments.head()

def main():
    st.title("Text Summarization")
    menu = ["Text File","PDF File"]
    choice = st.sidebar.selectbox("Select File Type",menu)
    
    if choice== "Text File" :
        st.subheader("Upload Text File")
        txt_file = st.file_uploader("Upload Text File",type=["txt"])
        if txt_file is not None:
            st.write(type(txt_file))
            file_details = {"filename":txt_file.name,
                            "filetype":txt_file.type,
                            "filesize":txt_file.size}
            
    elif choice == "PDF File" :
         st.subheader("Upload PDF File")
         txt_file = st.file_uploader("Upload PDF File",type=["pdf"])
         if txt_file is not None:
             st.write(type(txt_file))
             file_details = {"filename":txt_file.name,
                             "filetype":txt_file.type,
                             "filesize":txt_file.size}
    st.write("\n\n\n\n\n\n")
    col1, col2 = st.columns([.25,1])
    if txt_file is not None:        
        if txt_file.type == "application/pdf" :
            text= pdf(txt_file)
            
            if col1.button("Summary"):
                sumy= summary(text)
                st.text_area(label ="",value=sumy, height =300)
            if col2.button("Analysis"):
                analysis(text)
        elif txt_file.type == "text/plain" :
            text = txt(txt_file)
            if col1.button("Summary"):
                sumy= summary(text)
                st.text_area(label ="",value=sumy, height =300)
            if col2.button("Analysis"):
                analysis(text)
    else :
        pass        
     
    
            

if __name__ == '__main__':
    main()
           
    

