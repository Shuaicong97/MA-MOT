from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize

ref1 = "Person walking in the open area is going outside of the frame in right side"
cand1 = "A person walking in the open area exits the frame on the right side."

ref2 = "Person is walking towards the right side"
cand2 = "A person walks toward the right side."

ref3 = "Person entering into frame from right side is walking in the open area"
cand3 = "A person entering the frame from the right side is walking in the open area."

ref4 = "Person entering into frame from right side is cycling in the open area"
cand4 = "A person cycling into the frame from the right side is moving through the open area."

ref5 = "Cycle entering into frame from right side is moving in the open area"
cand5 = "A bicycle enters the frame from the right side, moving through the open area."

tokens_ref1 = word_tokenize(ref1)
tokens_ref2 = word_tokenize(ref2)
tokens_ref3 = word_tokenize(ref3)
tokens_ref4 = word_tokenize(ref4)
tokens_ref5 = word_tokenize(ref5)
tokens_cand1 = word_tokenize(cand1)
tokens_cand2 = word_tokenize(cand2)
tokens_cand3 = word_tokenize(cand3)
tokens_cand4 = word_tokenize(cand4)
tokens_cand5 = word_tokenize(cand5)
print(tokens_ref1)

reference = [['A', 'child', 'starts', 'walking']]  # 参考句子
candidate = ['A', 'child', 'begins', 'to', 'walk']  # 生成句子

# reference = [['A', 'person', 'converses', 'with', 'people']]  # 参考句子
# candidate = ['A', 'person', 'chats', 'with', 'people']  # 生成句子
# score = sentence_bleu(reference, candidate)
# print(score)  # 输出BLEU得分

# Smoothing function to avoid zero scores for short sentences
smooth_fn = SmoothingFunction().method1

# Calculate BLEU score using lower n-gram order (e.g., unigram and bigram)
bleu_score_1gram_1 = sentence_bleu([tokens_ref1], tokens_cand1, weights=(1, 0, 0, 0), smoothing_function=smooth_fn)
bleu_score_2gram_1 = sentence_bleu([tokens_ref1], tokens_cand1, weights=(0.5, 0.5, 0, 0), smoothing_function=smooth_fn)
print(f"BLEU score with 1-gram: {bleu_score_1gram_1}")
print(f"BLEU score with 2-gram: {bleu_score_2gram_1}")
print('\n')

bleu_score_1gram_2 = sentence_bleu([tokens_ref4], tokens_cand4, weights=(1, 0, 0, 0), smoothing_function=smooth_fn)
bleu_score_2gram_2 = sentence_bleu([tokens_ref4], tokens_cand4, weights=(0.5, 0.5, 0, 0), smoothing_function=smooth_fn)
print(f"BLEU score with 1-gram: {bleu_score_1gram_2}")
print(f"BLEU score with 2-gram: {bleu_score_2gram_2}")
print('\n')
