from coser.locations.controllers.controller import LocationController

def test_locations_parser():
    con=LocationController()
    result=con.parse_original_coser("./test/assets/out_folder_locations/")


def test_promt_input():
    con=LocationController()
    result=con.generate_prompts_for_input_with_oai()
    print(result)

    
def test_promt_input_hugginface():
    con=LocationController()
    result=con.generate_prompts_for_input_with_hf()
    print(result)


def test_locations_generate_corpus():
    con=LocationController()
    result=con.generate_location_corpus()
    # print(result)
    print(len(result))
    result.to_csv("assets/datast_llm_locations.csv",index=False)