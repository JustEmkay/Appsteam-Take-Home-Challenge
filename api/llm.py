import ollama


class OllamaLLM:
    """
    Facilitates communication with Ollama language models for chat-based interactions.

    Attributes:
        model (str): The name of the Ollama model to use for communication.
        role (str): The role for the interaction (e.g., 'user', 'assistant').
    """

    def __init__(swayam,
                 model_name: str= None,
                 role = 'user'):
        """
        Initializes the Ollama language model for interaction.

        Args:
            model_name (str): Name of the language model. Defaults to None.
            role (str): Role of the model in the conversation. Defaults to 'user'.
        """        
        swayam.model= model_name
        swayam.role= role
        
    def ollamaStatus(swayam) -> dict:
        """
        Checks the availability of the Ollama service and retrieves a list of available models.

        Returns:
            dict: Contains the status and available models, or an error message if unsuccessful.
        """
        try:
            result = ollama.list()
            models = [r['model'] for r in result['models'] if r['model'] != 'moondream:latest']
            return {
                'status' : True,
                'models' : models,
            }
            
        except Exception as e:
            return {
                'status' : False,
                'msg' : f"Error : {e}",
            }
                  
    def ollamaRequest(swayam, user_query: str, prompt_template: str= None):
        """
        Sends a query to the Ollama model and retrieves the response.

        Args:
            user_query (str): The user's input query.
            prompt_template (str): A template to customize the system's response. Defaults to None.

        Returns:
            dict: Contains the status and response from the model, or an error message if unsuccessful.
        """
        if not swayam.model:
            result= swayam.ollamaStatus()
            return result
        
        
        try:
            response= ollama.chat(model= swayam.model,
                                  messages= [
                                      {
                                'role': 'system',
                                'content': prompt_template
                            },
                            {
                                'role' : swayam.role,
                                'content': user_query
                            }
                                  ])
            
            return {
                'status': True,
                'response': response 
            }
        
        except Exception as e:
            
            return {
                'status': False,
                'response': e
            }
        



# query: str= """ 11/01/2025, 09:28:32 AM

# Today, I am grateful for:

# The warm cup of coffee I had this morning that helped me start my day off right. The beautiful sunrise I saw on my way to work that reminded me of the beauty in nature. The supportive friends and family in my life who are always there for me when I need them. The fact that I have a job that allows me to support myself and pursue my passions. The opportunity to take a walk outside during my lunch break and soak up some sunshine and fresh air. """

# prompt: str= """
# Analyze the tone and language used in the following journal entry to infer the writter's
# sentiment. Identify the emotions expressed and determine whether the overall sentiment is postive, negative or neutral.
# """

# olm= OllamaLLM( model_name= "llama3.2:1b" )

# result= olm.ollamaRequest(user_query= query, prompt_template= prompt)
# print(result)