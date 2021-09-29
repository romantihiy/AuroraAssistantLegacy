import gpt_2_simple as gpt2
from datetime import datetime

def generate(path_to_run, text):
  sess = gpt2.start_tf_sess()
  model = gpt2.load_gpt2(sess, run_name=path_to_run)
  return gpt2.generate(sess, length=600, temperature=0.7, prefix='Error: ' + text + 'Answer' , nsamples=2)

