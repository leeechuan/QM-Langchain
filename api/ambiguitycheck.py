from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import SequentialChain, LLMChain
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/langchain/ambiguitycheck', methods=['POST'])
def check_ambiguity():
    
    # Load environment variables from .env
    load_dotenv()
    
    try:
        # Get the data from the request
        data = request.json

        # Process the data (replace this with your actual processing logic)
        result = process_data(data)

        # Return the result as JSON
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_data(data):
        # Replace this function with your actual processing logic
    
        llm = ChatOpenAI(openai_api_key = os.getenv("OPENAI_API_KEY"))

        template1 = "You are a Business Analyst, it is your job to understand business requirements and come up with user stories. \
                    Given these requirements, determine if this is enough information to continue with a constructing a user story or \
                    user flow. If there is ambiguity in the statements, come up with potential questions to clarify this. If there is\
                    no ambiguity, come up with a user flow made up of user stories that is ready for development':\n{statement}"
                    
        prompt1 = ChatPromptTemplate.from_template(template1)
        
        chain_1 = LLMChain(llm=llm,
                            prompt=prompt1,
                            output_key="review_ambiguity")
        
        seq_chain = SequentialChain(chains=[chain_1],
                            input_variables=['statement'],
                            output_variables=['review_ambiguity'],
                            verbose=True)

        results = seq_chain(data)
    
        return results['review_ambiguity']

if __name__ == '__main__':
    app.run(debug=True)