# saiga-streamlit-ui
Run local Saiga LLM with Streamlit UI 

## HowTo

1. Download the [model](https://huggingface.co/IlyaGusev/saiga_mistral_7b_gguf/resolve/main/model-q8_0.gguf?download=true)
2. Change `MODEL_BASE_PATH` and `MODEL_NAMES` in `mistral_llamacpp_ui.py`
3. Install libs:
 
 ```
$ pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/metal
or
$ CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

pip install streamlit
```

4. Run:

```
streamlit run mistral_llamacpp_ui.py
```