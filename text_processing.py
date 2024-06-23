from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import pipeline

model = SentenceTransformer('cointegrated/rubert-tiny2')


def split_to_paragraphs(sentences, timecodes=None):
    """
    See: https://gist.github.com/avdosev/4f67d066806d9c32a4238ab24c4a8760
    """
    # Векторизуем, и склеиваем два массива в один
    X = model.encode(sentences)
    sx = list(zip(sentences, X))
    
    current = ''
    paragraphs = []

    for i in range(len(sx)):
        s, x = sx[i]

        if current:
            prefix = ' '
        elif timecodes is not None:
            prefix = timecode_to_text(timecodes[i].start_time) + '. '
        else:
            prefix = ''

        current += prefix + s.strip()

        if i+1 < len(sx):
            do_split_segment = cosine_similarity([x], [sx[i+1][1]]) < 0.53

            if timecodes is not None:
                time_diff = timecodes[i+1].start_time - timecodes[i].end_time
                do_split_segment |= time_diff > 3.0
            
            if do_split_segment:
                paragraphs.append(current)
                current = ''
            
    if current:
        paragraphs.append(current)
    
    return paragraphs


error_fixing_pipe = pipeline("text2text-generation", model="ai-forever/FRED-T5-1.7B-spell-distilled-100m")


def fix_errors(text):
    if len(text) < 1000:
        return error_fixing_pipe(text)[0]['generated_text'] 

    paragraphs = text.split('\n\n')

    fixed_paragraphs = []

    for paragpaph in paragraphs:
        if len(paragpaph) <= 1000:
            fixed = error_fixing_pipe(paragpaph)[0]['generated_text']
        else:
            fixed = paragpaph

        fixed_paragraphs.append(fixed)
    
    return '\n\n'.join(fixed_paragraphs)


def timecode_to_text(time: float):
    minutes = int(time // 60)
    seconds = int(time % 60)
    
    return f"{minutes:02}:{seconds:02}"
