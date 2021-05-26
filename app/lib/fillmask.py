import numpy as np
from transformers import BertTokenizerFast
from onnxruntime import ExecutionMode, InferenceSession, SessionOptions

from pathlib import Path

model_to_use = 'bert-base-cased'
MASK_STR = '[MASK]'

# Create the tokenizer.
tokenizer = BertTokenizerFast.from_pretrained(model_to_use)

# Create the InferenceSession.
options = SessionOptions()
options.intra_op_num_threads = 1
options.execution_mode = ExecutionMode.ORT_SEQUENTIAL
session = InferenceSession(
  f'{Path(__file__).parent.parent}/ml_model/{model_to_use}-quantized.onnx',
  options,
  providers=['CPUExecutionProvider']
)


def fill_mask_onnx(text: str, topn: int = 10) -> list:
  tokens = tokenizer(text, return_tensors='np')
  output = session.run(None, tokens.__dict__['data'])
  token_logits = output[0]

  # Get token indices of the masks.
  mask_token_indices = np.where(
    tokens['input_ids'] == tokenizer.mask_token_id)[1]

  # Get the top tokens for each mask.
  result = None
  for i in range(len(mask_token_indices)):
    mask_token_index = mask_token_indices[i:i+1]

    mask_token_logits = token_logits[0, mask_token_index, :]
    score = np.exp(mask_token_logits) / np.exp(
      mask_token_logits).sum(-1, keepdims=True)

    top_idx = (-score[0]).argsort()[:topn]
    top_values = score[0][top_idx]

    current = None
    for token, token_score in zip(top_idx.tolist(), top_values.tolist()):
      if current is not None:
        current = np.append(
            current, {'text': tokenizer.decode([token]), 'score': token_score})
      else:
        current = np.array(
            [{'text': tokenizer.decode([token]), 'score': token_score}])

    if result is not None:
      result = np.append(result, [current], axis=0)
    else:
      result = np.array([current])

  # Transpose and convert back to a regular list so that it can be serialized.
  return np.transpose(result).tolist()
