import dspy

class HuggingFaceLM(dspy.LM):
    def __init__(self, model, tokenizer, max_tokens=512):
        super().__init__(model_name=model.config._name_or_path)
        self.model = model
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens

    def __call__(self, prompt, **kwargs):
        # Tokenize the input prompt
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.max_tokens
        ).to(self.model.device)

        # Generate output
        outputs = self.model.generate(
            **inputs,
            max_length=kwargs.get("max_length", self.max_tokens),
            num_return_sequences=1,
            do_sample=kwargs.get("do_sample", True),
            temperature=kwargs.get("temperature", 0.7),
            top_p=kwargs.get("top_p", 0.9)
        )

        # Decode the output
        decoded = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return [dspy.Prediction(completion=text) for text in decoded]

# Instantiate the custom LM
hf_lm = HuggingFaceLM(model, tokenizer)

# Configure DSPy to use this LM
dspy.settings.configure(lm=hf_lm)
