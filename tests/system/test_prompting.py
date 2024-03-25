

from coser.common.services.PromptVariations import PromptingService


def test_prompting():
    service=PromptingService()
    print("OUTPUT",service.variate_prompts(["Where is the following text from?",
                                            "Tell me where is the procedence of the following text",
                                            "The next text is from somewhere in Spain. Tell me where."]))

def test_prompt_oai():
    service=PromptingService()
