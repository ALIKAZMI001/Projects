# LLM Fine-tuning

Two end-to-end fine-tuning experiments, written as runnable notebooks (originally
run on Google Colab with a mounted Drive).

## 1. `FineTuningOnBert.ipynb` — BERT on GLUE/MRPC

Fine-tunes `bert-base-uncased` for **paraphrase detection** on the MRPC subset of
GLUE.

- Tokenises sentence pairs with `AutoTokenizer`, dynamic padding via
  `DataCollatorWithPadding`.
- `AutoModelForSequenceClassification` (2 labels) trained with Hugging Face
  `Trainer` + `TrainingArguments`, tracking accuracy.
- Saves the fine-tuned model and reloads it in a second section to run inference on
  new sentence pairs.

**What it demonstrates:** the canonical HF fine-tuning loop — dataset → tokenizer →
collator → Trainer → `save_pretrained` → reload → predict.

## 2. `FineTuningCricketModel.ipynb` — T5 cricket chatbot

Fine-tunes a **T5 seq2seq** model into a cricket-domain Q&A chatbot from a custom
JSON dataset.

- Dataset built from a JSON file into a Hugging Face `Dataset`.
- Text-to-text framing: the question goes in, the answer comes out.
- Trained with `Seq2SeqTrainer`, saved to `t5_cricket_chatbot/`, then reloaded for
  generation with `AutoModelForSeq2SeqLM`.

**What it demonstrates:** domain adaptation of a small seq2seq model, plus the
dataset-construction and generation code around it.

## Run

The notebooks install their own dependencies in the first cells:

```python
!pip install transformers datasets evaluate --upgrade
```

They expect Google Drive to be mounted for the dataset/model paths; change those to
local paths to run elsewhere. A GPU runtime is recommended.

## Stack

`transformers` · `datasets` · `evaluate` · `torch` · `scikit-learn`
