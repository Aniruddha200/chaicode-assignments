class tokenizer:
    def encoder(self, text: str):
        words = text.split()
        tokens = []
        for word in words:
            sub_tokens = []
            for char in word:
                sub_tokens.append(ord(char))
            tokens.append(sub_tokens)
        return tokens

    def decoder(self, token_list: list):
        decoded_text = ""
        for sub_tokens in token_list:
            for token in sub_tokens:
                decoded_text += chr(token)
            decoded_text += " "
        return decoded_text.strip()

if __name__ == "__main__":
    tokenizer = tokenizer()
    input_text = input("""This is a demo tokenizer, where basic text get converted into numbers by their ascii values.
    Text length is limited to 100.
    Enter text to encode: """)
    if len(input_text) > 100:
        print("Text length exceeds 100 characters.")
        exit(1)
    if not input_text:  # Check if input is empty
        print("No input provided.")
        exit(1)
    generated_tokens = tokenizer.encoder(input_text)
    print("encoded_tokens:", generated_tokens)
    output_text = tokenizer.decoder(generated_tokens)
    print("decoded text:", output_text)
    