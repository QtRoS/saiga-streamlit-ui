# saiga-streamlit-ui
Run local Saiga LLM with Streamlit UI 

## HowTo

1. Download the [model](https://huggingface.co/IlyaGusev/saiga_mistral_7b_gguf/resolve/main/model-q8_0.gguf?download=true)
2. Change `MODEL_BASE_PATH` in `mistral_llamacpp_ui.py`
3. Run:

```
$ pip install llama_cpp streamlit
$ streamlit run mistral_llamacpp_ui.py
```
