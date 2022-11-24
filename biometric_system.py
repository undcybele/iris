import argparse
import hashlib
from dataclasses import dataclass
from os import remove
from enum import Enum
import os
import sys

from model.iris_classifier_model import IrisClassifier
from model.user import User
from utils.file_utils import create_empty_dir
from utils.image import Image
from utils.preprocessing_exceptions import ImageProcessingException
from utils.preprocessing import normalize_iris
from users.user_utils import get_user_name


class Mode:
    IDENTIFY: str = "identify"

@dataclass
class ProgramResult:
    message: str
    code: int


class RunResults(Enum):
    PROCESSING_FAILURE = ProgramResult("Failed to process the image", 1)
    IDENTIFICATION_SUCCESS = ProgramResult("Successfully identified a user", 0)
    IDENTIFICATION_FAILURE = ProgramResult(
        "Could not identify a user - user was not found in the database", 1)
    VERIFICATION_SUCCESS = ProgramResult("Successfully verified a user", 0)
    VERIFICATION_FAILURE_USER_UNKNOWN = ProgramResult(
        "Failed to verify a user - user was not found in the database", 1)
    VERIFICATION_FAILURE_USER_MISMATCH = ProgramResult(
        "Failed to verify a user - user ID did not match the classification", 1
    )


def run_classification(image_path: str, mode: str, user_id: str,
                       model_checkpoint_file_path: str):
    image = Image(image_path=image_path)

    try:
        image.find_iris_and_pupil()
    except ImageProcessingException:
        return RunResults.PROCESSING_FAILURE

    iris = normalize_iris(image)
    iris.pupil = image.pupil
    iris.iris = image.iris

    # Save the normalized image to a temporary file for easier use with
    # the trained network
    create_empty_dir("tmp")
    iris_hash = hashlib.sha1(image_path.encode()).hexdigest()
    iris_path = f"tmp/{iris_hash}.jpg"
    iris.save(iris_path)

    # Load trained classifier
    classifier = IrisClassifier(load_from_checkpoint=True,
                                checkpoint_file=model_checkpoint_file_path)

    # Get the classifier's prediction
    predicted_class, probability = classifier.classify_single_image(iris_path)
    predicted_user = get_user_name(predicted_class)
    if mode == Mode.IDENTIFY:
        if predicted_class == User.UNKNOWN:
            run_result = RunResults.IDENTIFICATION_FAILURE
        else:
            print(f"This image portraits user {predicted_user} "
                  f"(Prediction probability: {probability:.2%})")
            run_result = RunResults.IDENTIFICATION_SUCCESS
    # Remove temporary files
    remove(iris_path)

    return run_result


def system_main(image):
    # parser = argparse.ArgumentParser(
    #     description="Biometric system."
    # )

    # parser.add_argument("image", type=str, help="Path to the image.")

    # parser.add_argument("mode",
    #                     type=str,
    #                     choices=[Mode.IDENTIFY, Mode.VERIFY],
    #                     help="Program mode. "
    #                          "If you want to identify a user based on an "
    #                          "image, choose 'identify'; "
    #                          "If you want to verify whether an image "
    #                          "portraits a particular user, choose 'verify' "
    #                          "and provide the user's ID in the next argument.")

    # parser.add_argument("-u", "--user",
    #                     type=str,
    #                     help="User's ID. Only used with mode 'verify'.")

    # parser.add_argument("-m", "--model",
    #                     type=str,
    #                     help="Path to the trained classifier model",
    #                     default="iris/iris_recognition_trained_model.pt")

    # args = parser.parse_args()

    result = run_classification(
        image_path=image,
        mode=Mode.IDENTIFY,
        user_id=0,
        model_checkpoint_file_path="iris/iris_recognition_trained_model.pt"
    )

    print(f"Program exited with code: "
          f"{result.value.code} - {result.value.message}")
    
    return(result.value.code)

