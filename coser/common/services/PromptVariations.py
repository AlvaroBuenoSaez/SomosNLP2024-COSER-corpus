from typing import List
from transformers import pipeline

from coser.common.configuration.config import load_config
from transformers import T5Tokenizer, T5ForConditionalGeneration


class PromptingService:


    def __init__(self,model,template_prompt) -> None:
        self._tokenizer = T5Tokenizer.from_pretrained(model)
        self._model = T5ForConditionalGeneration.from_pretrained(model)
        self.template_prompt=template_prompt
        pass


    def variate_prompts(self,prompts:List[str]):

        input_text=self.template_prompt.format(prompts)
        
        print("INPUT:",input_text)
        input_ids = self._tokenizer(input_text, return_tensors="pt").input_ids
        outputs = self._model.generate(input_ids,max_length=600)
        result=self._tokenizer.decode(outputs[0])
        print("OUT:",result)
        return result