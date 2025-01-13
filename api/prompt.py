

JS_PROMPT= """ 
Your task is to find sentiment emotions detected of the following jounal given by the user.
"""

JS_PROMPT1= """
    Your job is to Analyze the sentiment of the journal entires to detect emotinal and classify polarity.
    
    Tasks:
        1. Emotional Detection: Identify the emotions expressed in each journal entry, such as happiness, sadness, anger, frustration, or hope.
        
        2. Polarity Classification: Classify the overall sentiment of each journal entry as positive, negative, or neutral.
        
    Consider the following:
        * Language  tone and style.
        * Key phrases and sentence that convey emotion.
        * Contextual information, such as the writer's situation and goals.
    Provide a sentiment analysis report, including:
        * Emotion detection result for each journal entry.
        * Polarity classification result for each journal entry  (positive, negative, or neutral)
        * A brif explanation  supportion your analysis for each journal entry.
    """

# sentiment analysis prompt
SA_PROMPT= """

    Your job is to Analyze the sentiment of the journals and provide a brif note on emotional detection and Polarity Classification
    of the user. Don't write unnecessary things.
    
    Provide a sentiment analysis report, including:
    * Emotion detection result for each journal entry.
    * Polarity classification result for each journal entry using percentage  (positive, negative, or neutral)
    * A brif explanation  supportion your analysis for each journal entry.
"""