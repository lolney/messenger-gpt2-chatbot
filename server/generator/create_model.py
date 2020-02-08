import gpt_2_simple as gpt2
import os

model_name = "117M"
if not os.path.isdir(os.path.join("models", model_name)):
    print(f"Downloading {model_name} model...")
    gpt2.download_gpt2(model_name=model_name)


training_filename = os.path.join("data", "training.txt")

sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              training_filename,
              model_name=model_name,
              steps=1000)   # steps is max number of training steps

gpt2.generate(sess)
