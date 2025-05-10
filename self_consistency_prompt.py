from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

#load env variables
load_dotenv()


def callLLM(usr_msg, sys_msg = "You are an AI assistant", model="qwen/qwen3-0.6b-04-28:free", isGenBestCall: bool = False) -> str:
# gets API Key from environment variable OPENAI_API_KEY
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=getenv("OPENROUTER_API_KEY"),
    )

    completion = client.chat.completions.create(
        model = model,
    # pass extra_body to access OpenRouter-only arguments.
        extra_headers={},
        extra_body={},
        messages=[
            {
                "role": "sys",
                "content": sys_msg,

                "role": "user",
                "content": usr_msg,
            },
        ],
    )
    result = completion.choices[0].message.content
    if isGenBestCall == False:
        print("\n\n Temp Result: \n")
        print(f"model is ${model}\n")
        print(f"response: \n ${result}")
    return result

def genBestResp(usr_msg: str, prev_outputs: list, sys_msg = """
                You are an experienced and excellent writer,
                your work is to analyse the crowd answers 
                and generate a new and elegent answer out of them
                """, model = "qwen/qwen3-0.6b-04-28:free")->str:
    if prev_outputs is None:
        return "No previous output found!!"
    new_usr_msg = "Question: " + usr_msg
    for i in range(0, len(prev_outputs)):
        new_usr_msg += f"\nOutput ${i}:" + prev_outputs[i]
    result = callLLM(usr_msg=new_usr_msg, sys_msg = sys_msg, model=model, isGenBestCall=True)
    return "\n" + usr_msg + "\n" + result
    
def main():
    usr_msg = "what is better an vocal vs reserve person?"
    sys_msg = "You are an ancient book with all the naughty, erotic and pervy knowledge of the world!"
    print("\n\n")
    print(sys_msg, "\n", usr_msg, end="\n")
    #pass the query to different models
    model1 = "microsoft/mai-ds-r1:free"
    output1 = callLLM(usr_msg=usr_msg, sys_msg= (sys_msg, None)[len(sys_msg) > 0], model=model1)
    model2 = "deepseek/deepseek-prover-v2:free"
    output2 = callLLM(usr_msg=usr_msg, sys_msg= (sys_msg, None)[len(sys_msg) > 0], model=model2)
    model3 = "meta-llama/llama-4-maverick:free"
    output3 = callLLM(usr_msg=usr_msg, sys_msg= (sys_msg, None)[len(sys_msg) > 0], model=model3)

    #gather the outputs
    outputList = [output1, output2, output3]

    #self-consistency prompt
    scp_sys_prompt = """
                You are an experienced and excellent writer,
                your work is to analyse the crowd answers 
                and generate a new, relevent and elegent answer out of them
                """
    #evalution and generation model
    eval_model = "deepseek/deepseek-r1-zero:free"

    #call and print best result
    final_result = genBestResp(usr_msg=usr_msg, prev_outputs=outputList, sys_msg=scp_sys_prompt, model=eval_model)
    print("\n\n Final Result: \n\n")
    print(final_result)

main()