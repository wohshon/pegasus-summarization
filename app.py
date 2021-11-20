from flask import Flask, request, jsonify
import torch
from transformers import PegasusTokenizer, PegasusForConditionalGeneration, PegasusConfig
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# modelNames = ['google/pegasus-xsum','google/pegasus-multi_news','google/pegasus-cnn_dailymail','google/pegasus-newsroom','google/pegasus-wikihow']
# break up to 1 models per cloud run service due to the size of the models
# summarize-1 tag 
modelNames = ['google/pegasus-xsum']
# summarize-2, tag :multi_news
# modelNames = ['google/pegasus-multi_news']
# summarize-3 tag :cnn_dailymail
# modelNames = ['google/pegasus-cnn_dailymail']
# summarize-4 tag :newsroom
# modelNames = ['google/pegasus-newsroom']

# preload
models =[]
tokenizers = []
print(' preloading models.... will take a while')
for m in modelNames:
    print('#'+str(modelNames.index(m)))
    print('pre-loading '+m)
    tokenizer = PegasusTokenizer.from_pretrained(m)
    model = PegasusForConditionalGeneration.from_pretrained(m).to(device)
    models.append(model)
    tokenizers.append(tokenizer)
print('....done')
app = Flask(__name__)
@app.route('/summarize', methods=['GET', 'POST'])
def test():
    content = request.json
    print(content['text_payload'])
    print(content['model'])    
    model_name = content['model']
    model_indx = modelNames.index(model_name)
    print('index: '+str(model_indx))
    # tokenizer = PegasusTokenizer.from_pretrained(model_name)
    # model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
    tokenizer = tokenizers[model_indx]
    model = models[model_indx]
    batch = tokenizer(content['text_payload'], truncation=True, padding='longest', return_tensors="pt").to(device)
    translated = model.generate(**batch)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
    return tgt_text[0]
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)