from flask import Flask, request, jsonify
import torch
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
model_name = 'google/pegasus-xsum'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)

app = Flask(__name__)
@app.route('/summarize', methods=['GET', 'POST'])
def test():
    content = request.json
    print(content['text_payload'])
    batch = tokenizer(content['text_payload'], truncation=True, padding='longest', return_tensors="pt").to(device)
    translated = model.generate(**batch)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
    return tgt_text[0]
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
