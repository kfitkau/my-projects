import torch
from diffusers import StableDiffusionPipeline, DiffusionPipeline, StableDiffusionXLPipeline
import PIL.Image

# Class for handling Stable Diffusion models.
class StableDiffusion():
    def __init__(self, model_id: str, scheduler: str, seed: int, sampling_steps: int, cfg_scale: int, height: int, width: int, positive_prompt: str, negative_prompt: str):
        """
        Constructor for the StableDiffusion class.

        Args:
            model_id (str): Identifier for the Stable Diffusion model.
            scheduler (str): Identifier for the scheduler.
            seed (int): Random seed for reproducibility.
            sampling_steps (int): Number of steps for sampling during diffusion.
            cfg_scale (int): Configuration scale parameter.
            height (int): Height of the generated image.
            width (int): Width of the generated image.
            positive_prompt (str): Positive prompt for the diffusion process.
            negative_prompt (str): Negative prompt for the diffusion process.
        """
        self.set_model_id(model_id)
        self.set_scheduler(scheduler)
        self.__seed = seed
        self.__sampling_steps = sampling_steps
        self.__cfg_scale = cfg_scale
        self.__height = height
        self.__width = width
        self.__positive_prompt = positive_prompt
        self.__negative_prompt = negative_prompt

    #Setter method model id
    def set_model_id(self, model_id: str) -> None:
        """
        Set the model ID based on user input.

        Args:
            model_id: Identifier for the Stable Diffusion model.

        Returns:
            None
        """
        if model_id == "SD 1.5":
            self.__model_id = "runwayml/stable-diffusion-v1-5"
        elif model_id == "SD 2.1":
            self.__model_id = "stabilityai/stable-diffusion-2-1"
        else:
            self.__model_id = "stabilityai/stable-diffusion-xl-base-1.0"
    
    #Setter method scheduler
    def set_scheduler(self, scheduler: str) -> None:
        """
        Set the scheduler for the Stable Diffusion model.

        Args:
            scheduler: Identifier for the scheduler.

        Raises:
            ValueError: If the specified scheduler is not supported.

        Returns:
            None
        """
        scheduler_module = __import__("diffusers", fromlist=[scheduler])
        if hasattr(scheduler_module, scheduler):
            scheduler_class = getattr(scheduler_module, scheduler)
            self.__scheduler = scheduler_class().from_pretrained(self.__model_id, subfolder="scheduler")
        else:
            raise ValueError(f"Unsupported scheduler: {scheduler}")


    def start(self) -> PIL.Image.Image:
        """
        Start the Stable Diffusion process and generate an image.

        Returns:
            list: Generated image.
        """
        torch_type = torch.float16 if torch.cuda.is_available() else torch.float32
        if self.__model_id == "runwayml/stable-diffusion-v1-5":
            pipe = StableDiffusionPipeline.from_pretrained(self.__model_id, scheduler=self.__scheduler, torch_dtype=torch_type)
        elif self.__model_id == "stabilityai/stable-diffusion-2-1":
            pipe = DiffusionPipeline.from_pretrained(self.__model_id, scheduler=self.__scheduler, torch_dtype=torch_type)
        else:
            pipe = StableDiffusionXLPipeline.from_pretrained(self.__model_id, scheduler=self.__scheduler, torch_dtype=torch_type)

        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = pipe.to(device)
        generator = torch.Generator(device=device).manual_seed(self.__seed)
        image = pipe(self.__positive_prompt, negative_prompt=self.__negative_prompt, width=self.__width, height=self.__height, num_inference_steps=self.__sampling_steps, guidance_scale=self.__cfg_scale, generator=generator).images[0]
        return image