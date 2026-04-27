from dotenv import load_dotenv
import os 

load_dotenv()

region = os.getenv("AWS_REGION")
model = os.getenv("BEDROCK_MODEL")
