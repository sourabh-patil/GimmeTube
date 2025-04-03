import base64
import yaml
import logging
from openai import OpenAI
# from openai.error import OpenAIError


class CallLlama32:
    """
    A class for interacting with the OpenAI LLaMA model for image and text modalities.
    
    Attributes:
        llama_model_name (str): The name of the model to use.
        openai_api_key (str): The API key for OpenAI client keep it as string value
        openai_api_base (str): The base URL for the llama model.
        client (OpenAI): The OpenAI client for interacting with the API.
        image_mode_max_tokens (int): Maximum tokens for image modality responses.
        image_mode_user_prompt (str): User prompt for image modality.
        text_mode_max_tokens (int): Maximum tokens for text modality responses.
        text_mode_system_prompt (str): System prompt for text modality.
    """

    def __init__(self, config_path):
        """
        Initializes the CallLlama32 class with configuration from a YAML file.

        Args:
            config_path (str): Path to the YAML configuration file.
        """
        self._setup_logger()
        
        try:
            with open(config_path, "r") as yaml_file:
                config = yaml.safe_load(yaml_file)
                
            self.llama_model_name = config['MODEL_DETAILS']['model_name']
            self.openai_api_key = "EMPTY"  
            self.openai_api_base = config['MODEL_DETAILS']['model_host_address']
            self.client = OpenAI(api_key=self.openai_api_key, base_url=self.openai_api_base)
            
            self.image_mode_max_tokens = config['IMAGE_MODALITY_PARAMS']['max_tokens']
            self.image_mode_user_prompt = config['IMAGE_MODALITY_PARAMS']['user_prompt']
            self.text_mode_max_tokens = config['TEXT_MODALITY_PARAMS']['max_tokens']
            self.text_mode_system_prompt = config['TEXT_MODALITY_PARAMS']['system_prompt']
            
            self.logger.info("Successfully initialized CallLlama32 instance.")
        except FileNotFoundError:
            self.logger.error(f"Configuration file {config_path} not found.")
            raise
        except KeyError as e:
            self.logger.error(f"Missing key in configuration: {e}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"Error reading YAML configuration: {e}")
            raise

    def _setup_logger(self):
        """Sets up the logger for the class with both console and file handlers."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        # File handler
        file_handler = logging.FileHandler('llama32.log')
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        # Adding handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def encode_image(self, image_path):
        """
        Encodes an image file to base64.

        Args:
            image_path (str): The file path to the image.

        Returns:
            str: The base64 encoded string of the image.
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            self.logger.info(f"Encoded image {image_path} successfully.")
            return encoded_image
        except FileNotFoundError:
            self.logger.error(f"Image file {image_path} not found.")
            raise
        except Exception as e:
            self.logger.error(f"Error encoding image: {e}")
            raise

    def get_image_details(self, image_path):
        """
        Sends an image and prompt to the model and retrieves details.

        Args:
            image_path (str): The file path to the image.

        Returns:
            str: The model's response content.
        """
        try:
            base64_image = self.encode_image(image_path)
            chat_response = self.client.chat.completions.create(
                model=self.llama_model_name,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.image_mode_user_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }],
                max_tokens=self.image_mode_max_tokens,
            )
            response_content = chat_response.choices[0].message.content
            self.logger.info("Image details retrieved successfully.")
            return response_content
        # except OpenAIError as e:
        #     self.logger.error(f"OpenAI API error: {e}")
        #     raise
        except Exception as e:
            self.logger.error(f"Error in get_image_details: {e}")
            raise

    def get_text_summary(self, content):
        """
        Sends a text prompt to the model and retrieves a summary.

        Args:
            content (str): The text content to summarize.

        Returns:
            str: The model's summary response.
        """
        try:
            chat_response = self.client.chat.completions.create(
                model=self.llama_model_name,
                messages=[
                    {"role": "system", "content": self.text_mode_system_prompt},
                    {"role": "user", "content": content}
                ],
                max_tokens=self.text_mode_max_tokens,
            )
            response_content = chat_response.choices[0].message.content
            self.logger.info("Text summary retrieved successfully.")
            return response_content
        # except OpenAIError as e:
        #     self.logger.error(f"OpenAI API error: {e}")
        #     raise
        except Exception as e:
            self.logger.error(f"Error in get_text_summary: {e}")
            raise


call_llama = CallLlama32(config_path='llama32_api_config.yaml')

# import glob

# input_paths = sorted(glob.glob('./output_frames/**'))

# for curr_path in input_paths:

#     print(curr_path)
#     curr_time_stamp = ":".join(curr_path.split('/')[-1].split('.')[0].split('_')[1:])
#     print(curr_time_stamp)
#     res = call_llama.get_image_details(image_path=curr_path)

#     curr_time_stamp = f"TIMESTAMP: {curr_time_stamp} \n\n"
#     res = curr_time_stamp + res

#     with open("match_summary.txt", "a") as file:
#         file.write(str(res) + "\n\n###\n\n")


timestamp_list = [{'end': '0:10:39.300000', 'start': '0:10:06.240000'}, {'end': '1:09:53.600000', 'start': '1:09:21.299000'}, {'end': '1:11:59.500000', 'start': '1:11:28.980000'}, {'end': '1:17:23.500000', 'start': '1:16:50.880000'}, {'end': '1:17:54.700000', 'start': '1:17:23.520000'}, {'end': '1:19:01.100000', 'start': '1:18:30.320000'}, {'end': '1:27:20.200000', 'start': '1:26:49.739000'}, {'end': '1:34:43.300000', 'start': '1:34:12.179000'}, {'end': '1:36:49.300000', 'start': '1:36:17.639000'}, {'end': '1:37:20.800000', 'start': '1:36:49.380000'}]


res = call_llama.get_text_summary(str(timestamp_list))

print(res)