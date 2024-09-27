import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """Samsung recently cancelled its in-person MWC 2021 event, instead, committing to an online-only format. The South Korean tech giant recently made it official, setting a time and date for the Samsung Galaxy MWC Virtual Event.

The event will be held on June 28 at 17:15 UTC (22:45 IST) and will be live-streamed on YouTube. In its release, Samsung says that it will introduce its “ever-expanding Galaxy device ecosystem”. Samsung also plans to present the latest technologies and innovation efforts in relation to the growing importance of smart device security.

Samsung will also showcase its vision for the future of smartwatches to provide new experiences for users and new opportunities for developers. Samsung also shared an image for the event with silhouettes of a smartwatch, a smartphone, a tablet and a laptop.
"""

def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    print(stopwords)

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)

  
    tokens = [token.text for token in doc]

    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    max_freq = max(word_freq.values())

    
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    
    sent_tokens = [sent for sent in doc.sents]

    sent_scores = {}  

    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores:
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    select_len = int(len(sent_tokens) * 0.3)
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)


    return summary, doc, len(rawdocs.split()), len(summary.split())


summary, original_text, len_orig_text, len_summary = summarizer(text)
#print(f"Summary: {summary}")
#print(f"Original Length: {len_orig_text}")
#print(f"Summary Length: {len_summary}")
