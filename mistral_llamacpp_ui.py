
import streamlit as st
from llama_cpp import Llama


SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."
SYSTEM_TOKEN = 1587
USER_TOKEN = 2188
BOT_TOKEN = 12435
LINEBREAK_TOKEN = 13

ROLE_TOKENS = {
    "system": SYSTEM_TOKEN,
    "user": USER_TOKEN,
    "bot": BOT_TOKEN,
}

MODEL_BASE_PATH = "g:/Dev/llm/models"
MODEL_NAMES = ["saiga-mistral-q8_0.gguf"]


def get_message_tokens(model, role, content):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, ROLE_TOKENS[role])
    message_tokens.insert(2, LINEBREAK_TOKEN)
    message_tokens.append(model.token_eos())
    return message_tokens


st.sidebar.title("LLM Tester")
st.sidebar.markdown("### Options")
st.sidebar.markdown("*(defaults are fine)*")
n_ctx = st.sidebar.number_input("n_ctx", value=2000)
top_k =  st.sidebar.number_input("top_k", value=30)
top_p =  st.sidebar.number_input("top_p", value=0.9)
temperature =  st.sidebar.number_input("temperature", value=0.2) 
repeat_penalty =  st.sidebar.number_input("repeat_penalty", value=1.1)


# model_name = st.selectbox("Model name", MODEL_NAMES)
model_name = MODEL_NAMES[0]


@st.cache_resource  # (max_entries=1)
def load_model(model_name: str) -> tuple:
    full_path = f"{MODEL_BASE_PATH}/{model_name}" # TODO UGLY
    print(f"{full_path=}")

    model = Llama(model_path=full_path, n_ctx=n_ctx, n_parts=1,)
    print(f"Model {model_name} loaded: {model}")

    system_tokens = get_message_tokens(model, role="system", content=SYSTEM_PROMPT)
    model.eval(system_tokens)
    print("System tokens generated and evaluated")

    return model, system_tokens


model, system_tokens = load_model(model_name)
if not model:
    st.stop()


user_message = st.text_area("User:", height=200)
if not st.button("Run"):
    st.stop()

st.sidebar.markdown("### Info")
st.sidebar.markdown(f"Input length: **{len(user_message)}**")

# tokens = copy(system_tokens)
tokens = system_tokens.copy()
# print(f"{user_message=}")
message_tokens = get_message_tokens(model=model, role="user", content=user_message)
role_tokens = [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
tokens += message_tokens + role_tokens
# print(tokens)
full_prompt = model.detokenize(tokens).decode("utf-8", errors="ignore")
print(f"{full_prompt=}")
# print(model.tokenize(full_prompt))

st.markdown(f"**Answer**:")
container = st.empty()

with st.spinner('Model is generating answer...'):
    generated_text = ""
    generator = model.generate(tokens, top_k=top_k, top_p=top_p, temp=temperature, repeat_penalty=repeat_penalty)
    for token in generator:
        token_str = model.detokenize([token]).decode("utf-8", errors="ignore")
        tokens.append(token)
        generated_text += token_str
        if token == model.token_eos():
            break
        print(token_str, end="", flush=True)
        container.markdown(generated_text)
    print()

st.success("Done")